#!/usr/bin/env python3
"""Refresh low-quality cached previews without scanning every post from scratch."""

from __future__ import annotations

import argparse
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fetch_link_previews import fetch_preview, load_cache, save_cache
from link_preview_utils import cache_lookup_keys, extract_urls_from_body, is_useful_preview_url, preview_needs_refresh


def tracked_urls() -> set[str]:
    result = subprocess.run(
        ["git", "ls-files", "site/content/posts"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    urls: set[str] = set()
    for line in result.stdout.splitlines():
        if not line.endswith(".md"):
            continue
        text = (ROOT / line).read_text(encoding="utf-8")
        if text.startswith("---\n"):
            end = text.find("\n---\n", 4)
            if end != -1:
                text = text[end + 5 :]
        for url in extract_urls_from_body(text):
            if is_useful_preview_url(url):
                urls.add(url)
    return urls


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--workers", type=int, default=12)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    cache = load_cache()
    tracked = tracked_urls()
    targets = []
    for url, preview in cache.items():
        if url in tracked and isinstance(preview, dict) and preview_needs_refresh(preview, url):
            targets.append(url)

    targets = sorted(set(targets))
    if args.limit > 0:
        targets = targets[: args.limit]

    print(f"Targets: {len(targets)}")
    if args.dry_run:
        for url in targets[:50]:
            print(url)
        return

    updated = 0
    with ThreadPoolExecutor(max_workers=max(args.workers, 1)) as executor:
        futures = {executor.submit(fetch_preview, url): url for url in targets}
        for future in as_completed(futures):
            url = futures[future]
            result = future.result()
            if not isinstance(result, dict):
                continue
            cache[url] = result
            for key in cache_lookup_keys(result.get("url", "")):
                cache[key] = result
            updated += 1

    save_cache(cache)
    print(f"Updated: {updated}")


if __name__ == "__main__":
    main()
