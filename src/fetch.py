from __future__ import annotations

import json
import os
import subprocess
import sys


def fetch_all_comments(
    video_id: str,
    max_comments: int = 5000,
    cookiefile: str | None = None,
) -> dict:
    url = f"https://www.youtube.com/watch?v={video_id}"

    cmd = [
        sys.executable or "python3",
        "-m", "yt_dlp",
        "--write-comments",
        "--no-download",
        "--no-warnings",
        "--dump-json",
        "--ignore-errors",
        "--ignore-no-formats-error",
    ]

    if cookiefile and os.path.exists(cookiefile):
        cmd.extend(["--cookies", cookiefile])

    cmd.append(url)

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

    if result.returncode != 0 and not result.stdout:
        print(f"yt-dlp error: {result.stderr[:500]}", file=sys.stderr)
        return {"video_title": video_id, "comments": {}}

    try:
        info = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        return {"video_title": video_id, "comments": {}}

    video_title = info.get("title", video_id)
    raw_comments = info.get("comments") or []

    comments: dict[str, dict] = {}
    for c in raw_comments:
        if max_comments and len(comments) >= max_comments:
            break
        cid = c.get("id")
        if not cid:
            continue
        comments[cid] = {
            "author": c.get("author", ""),
            "text": c.get("text", ""),
            "timestamp": c.get("timestamp"),
            "like_count": c.get("like_count", 0),
            "is_reply": c.get("parent", "root") != "root",
            "parent_id": None if c.get("parent") == "root" else c.get("parent"),
        }

    return {"video_title": video_title, "comments": comments}
