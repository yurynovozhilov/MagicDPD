#!/usr/bin/env python3
"""Import VK posts older than the oldest unified post into unified_posts.json.

Reads vk/magicdpd_raw_dump.json, converts posts with date < CUTOFF to the
unified format, merges them into unified_posts.json (no duplicates by VK id),
sorts everything by date, then calls backfill_early_posts to generate blog files.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW_VK = ROOT / "vk" / "magicdpd_raw_dump.json"
UNIFIED = ROOT / "unified_posts.json"


def vk_timestamp_to_iso(ts: int) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


def convert_photo(att: dict, post_id: int) -> dict:
    photo = att.get("photo", {})
    sizes = [
        {"type": s.get("type"), "width": s.get("width"), "height": s.get("height")}
        for s in photo.get("sizes", [])
    ]
    return {
        "type": "photo",
        "id": photo.get("id"),
        "sizes": sizes,
        "post_id": post_id,
        "url": max(photo.get("sizes", [{}]), key=lambda s: s.get("width", 0) * s.get("height", 0)).get("url"),
    }


def convert_attachments(raw_post: dict) -> tuple[list[dict], list[str]]:
    media = []
    links = []
    post_id = raw_post.get("id")
    for att in raw_post.get("attachments", []):
        t = att.get("type")
        if t == "photo":
            media.append(convert_photo(att, post_id))
        elif t == "link":
            link = att.get("link", {})
            url = link.get("url", "")
            if url:
                links.append(url)
            media.append({
                "type": "webpage",
                "site_name": link.get("caption"),
                "title": link.get("title"),
                "description": link.get("description"),
                "url": url,
            })
        elif t == "video":
            video = att.get("video", {})
            media.append({
                "type": "video",
                "id": video.get("id"),
                "title": video.get("title"),
            })
        elif t == "doc":
            doc = att.get("doc", {})
            media.append({
                "type": "doc",
                "id": doc.get("id"),
                "title": doc.get("title"),
                "url": doc.get("url"),
            })
        else:
            media.append({"type": t})
    return media, links


def raw_to_unified(raw_post: dict) -> dict:
    media, links = convert_attachments(raw_post)
    return {
        "id": raw_post["id"],
        "date": vk_timestamp_to_iso(raw_post["date"]),
        "text": raw_post.get("text", ""),
        "views": raw_post.get("views", {}).get("count") if raw_post.get("views") else None,
        "forwards": raw_post.get("reposts", {}).get("count") if raw_post.get("reposts") else None,
        "replies": raw_post.get("comments", {}).get("count") if raw_post.get("comments") else None,
        "reply_to": None,
        "post_author": None,
        "via_bot": None,
        "pinned": raw_post.get("is_pinned", False) or None,
        "grouped_id": None,
        "links": links,
        "media": media,
        "forwarded_from": None,
        "source": "vk",
    }


def main():
    if not RAW_VK.exists():
        print(f"Error: {RAW_VK} not found.")
        sys.exit(1)

    with open(RAW_VK, encoding="utf-8") as f:
        raw_posts = json.load(f)

    with open(UNIFIED, encoding="utf-8") as f:
        unified = json.load(f)

    # Determine cutoff: oldest date already in unified_posts.json
    existing_dates = [
        datetime.fromisoformat(p["date"].replace("Z", "+00:00"))
        for p in unified if p.get("date")
    ]
    cutoff = min(existing_dates)
    print(f"Oldest post in unified_posts.json: {cutoff.isoformat()}")

    # Existing unified entries before cutoff (deduplicate by ISO date string, 1-second precision)
    existing_before_cutoff = {
        p["date"]
        for p in unified
        if p.get("date", "") < cutoff.isoformat()
    }

    # Filter raw VK posts: older than cutoff and not already present by exact timestamp
    old_raw = [
        p for p in raw_posts
        if datetime.fromtimestamp(p["date"], tz=timezone.utc) < cutoff
        and vk_timestamp_to_iso(p["date"]) not in existing_before_cutoff
    ]

    print(f"New VK posts to import (before {cutoff.date()}): {len(old_raw)}")

    if not old_raw:
        print("Nothing to import.")
        return

    new_entries = [raw_to_unified(p) for p in old_raw]

    # Merge and sort by date
    all_posts = unified + new_entries
    all_posts.sort(key=lambda p: p.get("date", ""))

    with open(UNIFIED, "w", encoding="utf-8") as f:
        json.dump(all_posts, f, ensure_ascii=False, indent=2)

    print(f"unified_posts.json updated: {len(unified)} → {len(all_posts)} posts")

    # Generate blog files for the new posts
    print("\nGenerating blog files...")
    import subprocess
    result = subprocess.run(
        [sys.executable, str(ROOT / "backfill_early_posts.py")],
        cwd=ROOT,
    )
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
