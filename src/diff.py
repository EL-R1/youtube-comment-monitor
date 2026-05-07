from __future__ import annotations


def compute_diff(
    old_comments: dict[str, dict],
    new_comments: dict[str, dict],
) -> tuple[list[dict], list[dict], list[dict]]:
    old_ids = set(old_comments)
    new_ids = set(new_comments)

    added_ids = new_ids - old_ids
    deleted_ids = old_ids - new_ids
    common_ids = old_ids & new_ids

    added = [new_comments[cid] | {"id": cid} for cid in added_ids]

    deleted = [old_comments[cid] | {"id": cid} for cid in deleted_ids]

    modified = []
    for cid in common_ids:
        old = old_comments[cid]
        new = new_comments[cid]
        if old["text"] != new["text"]:
            modified.append({
                "id": cid,
                "author": new["author"],
                "old_text": old["text"],
                "new_text": new["text"],
            })

    return added, deleted, modified
