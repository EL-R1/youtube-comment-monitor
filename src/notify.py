from __future__ import annotations

import requests

MAX_CHARS = 1900
MAX_TEXT = 200


def _split_messages(lines: list[str]) -> list[str]:
    chunks = []
    current = ""
    for line in lines:
        candidate = f"{current}\n{line}" if current else line
        if len(candidate) > MAX_CHARS:
            if current:
                chunks.append(current)
            current = line
        else:
            current = candidate
    if current:
        chunks.append(current)
    return chunks


def notify_changes(
    webhook_url: str,
    deleted: list[dict],
    modified: list[dict],
    video_title: str = "",
    video_id: str = "",
) -> None:
    if not deleted and not modified:
        return

    lines = [
        f"**[{video_title}](<https://youtu.be/{video_id}>)**"
        f" — {len(deleted)} supprimé(s), {len(modified)} modifié(s)",
        "",
    ]

    for c in deleted:
        text = c.get("text", "")[:MAX_TEXT]
        lines.append(f"🗑️ **@{c.get('author', '?')}** : {text or '(vide)'}")

    if modified:
        if deleted:
            lines.append("")
        for c in modified:
            old_text = c.get("old_text", "")[:MAX_TEXT]
            link = f"https://www.youtube.com/watch?v={video_id}&lc={c.get('id', '')}"
            lines.append(f"✏️ **@{c.get('author', '?')}** : {old_text} → [Voir](<{link}>)")

    for chunk in _split_messages(lines):
        requests.post(webhook_url, json={"content": chunk}, timeout=15)
