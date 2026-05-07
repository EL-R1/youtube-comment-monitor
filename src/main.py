from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone

from . import config
from .diff import compute_diff
from .fetch import fetch_all_comments
from .notify import notify_changes


def load_snapshot() -> dict | None:
    if not os.path.exists(config.SNAPSHOT_PATH):
        return None
    with open(config.SNAPSHOT_PATH) as f:
        return json.load(f)


def save_snapshot(data: dict) -> None:
    os.makedirs(os.path.dirname(config.SNAPSHOT_PATH), exist_ok=True)
    with open(config.SNAPSHOT_PATH, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main() -> None:
    video_id = config.VIDEO_ID
    if not video_id:
        print("ERROR: VIDEO_ID is not set", file=sys.stderr)
        sys.exit(1)

    print(f"Fetching comments for video {video_id}...")
    result = fetch_all_comments(
        video_id,
        max_comments=config.MAX_COMMENTS,
        cookiefile=config.COOKIES_FILE,
    )
    new_comments = result["comments"]
    video_title = result["video_title"]
    print(f"  → {len(new_comments)} comments fetched")

    old_snapshot = load_snapshot()
    old_comments = old_snapshot.get("comments", {}) if old_snapshot else {}

    if not old_comments:
        print("No previous snapshot — saving initial state (no notification)")
        save_snapshot({
            "video_title": video_title,
            "video_id": video_id,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "comments": new_comments,
        })
        return

    added, deleted, modified = compute_diff(old_comments, new_comments)
    print(f"  → {len(added)} ajoutés, {len(deleted)} supprimés, {len(modified)} modifiés")

    webhook = config.DISCORD_WEBHOOK_URL
    notify_modified = config.NOTIFY_MODIFIED

    if not notify_modified and modified:
        print(f"  → notification des modifiés désactivée")

    if (deleted or (notify_modified and modified)) and webhook:
        print("Sending Discord notification...")
        notify_changes(
            webhook_url=webhook,
            deleted=deleted,
            modified=modified if notify_modified else [],
            video_title=video_title,
            video_id=video_id,
        )

    save_snapshot({
        "video_title": video_title,
        "video_id": video_id,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "comments": new_comments,
    })
    print("Snapshot saved")


if __name__ == "__main__":
    main()
