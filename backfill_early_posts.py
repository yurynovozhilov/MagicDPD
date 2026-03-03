#!/usr/bin/env python3
"""Add VK posts from unified_posts.json that are missing from site/content/posts/.
Only creates new files — never overwrites existing ones.
"""
import json
import sys

from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "unified_posts.json"
SITE_POSTS = ROOT / "site" / "content" / "posts"

from generate_site_from_unified import (
    build_post,
    write_post_file,
    derive_slug,
    _build_media_index,
    _build_images_index,
)


def existing_dates() -> set[str]:
    """Return set of YYYY-MM-DD prefixes already present in site/content/posts/."""
    return {p.name[:10] for p in SITE_POSTS.glob("*.md")}


def main():
    if not DATA_PATH.exists():
        print(f"Error: {DATA_PATH} not found.")
        sys.exit(1)

    with open(DATA_PATH, encoding="utf-8") as f:
        posts = json.load(f)

    cutoff_str = None
    if len(sys.argv) > 1:
        cutoff_str = sys.argv[1]

    cutoff: datetime | None = None
    if cutoff_str:
        try:
            cutoff = datetime.fromisoformat(cutoff_str)
        except ValueError:
            print(f"Invalid cutoff date: {cutoff_str}. Use ISO format e.g. 2016-07-03")
            sys.exit(1)

    print("Building file indexes...")
    media_index = _build_media_index()
    images_index = _build_images_index()

    existing = existing_dates()
    print(f"Existing posts in site/content/posts/: {len(existing)} dates")

    added = 0
    skipped_exists = 0
    skipped_no_data = 0

    for post in posts:
        post_data = build_post(post, media_index, images_index)
        if not post_data:
            skipped_no_data += 1
            continue

        post_date: datetime = post_data["date"]

        if cutoff and post_date.replace(tzinfo=None) >= cutoff.replace(tzinfo=None):
            continue

        filename = f"{post_date:%Y-%m-%d}-{post_data['slug']}.md"
        path = SITE_POSTS / filename

        if path.exists():
            skipped_exists += 1
            continue

        write_post_file(post_data)
        print(f"  + {filename}")
        added += 1

    print(f"\nDone: {added} new post(s) added, {skipped_exists} skipped (already exist).")


if __name__ == "__main__":
    main()
