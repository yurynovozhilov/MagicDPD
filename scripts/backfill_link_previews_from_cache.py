#!/usr/bin/env python3
"""Write cached link previews into tracked post markdown files."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import frontmatter

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "site" / "content" / "posts"
CACHE_FILE = ROOT / "link_previews_cache.json"
sys.path.insert(0, str(ROOT))

from link_preview_utils import build_link_previews_from_cache


def tracked_post_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "site/content/posts"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    files = []
    for line in result.stdout.splitlines():
        if line.endswith(".md"):
            files.append(ROOT / line)
    return sorted(files)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    cache = {}
    if CACHE_FILE.exists():
        cache = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    updated = 0
    added = 0
    removed = 0

    for md_path in tracked_post_files():
        raw = md_path.read_text(encoding="utf-8")
        post = frontmatter.loads(raw)

        previews = build_link_previews_from_cache(post.content, cache)
        existing = post.metadata.get("link_previews") or []

        if previews:
            if existing == previews:
                continue
            post.metadata["link_previews"] = previews
            if existing:
                updated += 1
            else:
                added += 1
        else:
            if "link_previews" not in post.metadata:
                continue
            del post.metadata["link_previews"]
            removed += 1

        if not args.dry_run:
            md_path.write_text(frontmatter.dumps(post) + "\n", encoding="utf-8")

    print(
        f"Done. added={added} updated={updated} removed={removed} total_changed={added + updated + removed}"
    )


if __name__ == "__main__":
    main()
