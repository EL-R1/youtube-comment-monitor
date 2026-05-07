from __future__ import annotations

import requests

COLOR_RED = 0xED4245
COLOR_ORANGE = 0xFEE75C
EMBED_LIMIT = 10


def _send_webhook(webhook_url: str, embeds: list[dict]) -> None:
    for i in range(0, len(embeds), EMBED_LIMIT):
        batch = embeds[i : i + EMBED_LIMIT]
        payload = {"embeds": batch}
        resp = requests.post(webhook_url, json=payload, timeout=15)
        resp.raise_for_status()


def _build_deleted_embed(comment: dict) -> dict:
    text = comment.get("text", "")[:1000]
    return {
        "title": "Commentaire supprimé",
        "color": COLOR_RED,
        "fields": [
            {"name": "Auteur", "value": comment.get("author", "Inconnu"), "inline": True},
            {"name": "Likes", "value": str(comment.get("like_count", 0)), "inline": True},
            {"name": "Commentaire", "value": text or "(vide)"},
        ],
        "footer": {"text": f"ID: {comment.get('id', '?')}"},
    }


def _build_modified_embed(comment: dict) -> dict:
    old_text = comment.get("old_text", "")[:500]
    new_text = comment.get("new_text", "")[:500]
    return {
        "title": "Commentaire modifié",
        "color": COLOR_ORANGE,
        "fields": [
            {"name": "Auteur", "value": comment.get("author", "Inconnu"), "inline": True},
            {"name": "Ancien", "value": old_text or "(vide)"},
            {"name": "Nouveau", "value": new_text or "(vide)"},
        ],
        "footer": {"text": f"ID: {comment.get('id', '?')}"},
    }


def notify_changes(
    webhook_url: str,
    deleted: list[dict],
    modified: list[dict],
    video_title: str = "",
    video_id: str = "",
) -> None:
    if not deleted and not modified:
        return

    video_label = video_title or f"https://youtu.be/{video_id}"
    embeds: list[dict] = []

    for c in deleted:
        embeds.append(_build_deleted_embed(c))

    for c in modified:
        embeds.append(_build_modified_embed(c))

    summary = {
        "content": (
            f"**{video_label}** — "
            f"{len(deleted)} supprimé(s), {len(modified)} modifié(s)"
        ),
    }
    requests.post(webhook_url, json=summary, timeout=15)

    _send_webhook(webhook_url, embeds)
