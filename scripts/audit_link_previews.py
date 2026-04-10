#!/usr/bin/env python3
"""Audit tracked posts for missing and low-quality link previews."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

import frontmatter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from link_preview_utils import (
    best_cached_preview,
    build_link_previews_from_cache,
    extract_urls_from_body,
    is_useful_preview_url,
    preview_has_content,
    preview_host,
    should_skip_preview_url,
)
CACHE_FILE = ROOT / "link_previews_cache.json"


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
    parser.add_argument("--examples", type=int, default=15)
    args = parser.parse_args()

    cache = {}
    if CACHE_FILE.exists():
        cache = json.loads(CACHE_FILE.read_text(encoding="utf-8"))

    stats = Counter()
    fixable_domains = Counter()
    blocked_domains = Counter()
    uncached_domains = Counter()
    low_quality_domains = Counter()
    examples: dict[str, list[tuple[str, list[str] | str]]] = {
        "fixable": [],
        "blocked": [],
        "uncached": [],
        "low_quality": [],
    }

    for md_path in tracked_post_files():
        post = frontmatter.loads(md_path.read_text(encoding="utf-8"))
        raw_urls = extract_urls_from_body(post.content)
        blocked = [url for url in raw_urls if should_skip_preview_url(url)]
        urls = [url for url in raw_urls if is_useful_preview_url(url)]
        previews = post.metadata.get("link_previews") or []

        stats["total_posts"] += 1
        if urls:
            stats["posts_with_candidate_urls"] += 1
        if previews:
            stats["posts_with_frontmatter_previews"] += 1

        if previews:
            first = previews[0]
            title = (first.get("title") or "").strip()
            if title == "- YouTube":
                stats["posts_with_low_quality_youtube_title"] += 1
                low_quality_domains[preview_host(first.get("url", ""))] += 1
                if len(examples["low_quality"]) < args.examples:
                    examples["low_quality"].append((md_path.name, first.get("url", "")))

        if not urls or previews:
            continue

        cached_previews = build_link_previews_from_cache(post.content, cache)
        if cached_previews:
            stats["missing_but_fixable_from_cache"] += 1
            for preview in cached_previews:
                fixable_domains[preview_host(preview.get("url", ""))] += 1
            if len(examples["fixable"]) < args.examples:
                examples["fixable"].append((md_path.name, [p.get("url", "") for p in cached_previews[:3]]))
            continue

        if blocked:
            stats["missing_blocked_by_rule"] += 1
            for url in blocked:
                blocked_domains[preview_host(url)] += 1
            if len(examples["blocked"]) < args.examples:
                examples["blocked"].append((md_path.name, blocked[:3]))
            continue

        uncached = [url for url in urls if not best_cached_preview(url, cache)]
        if uncached:
            stats["missing_without_cache_entry"] += 1
            for url in uncached:
                uncached_domains[preview_host(url)] += 1
            if len(examples["uncached"]) < args.examples:
                examples["uncached"].append((md_path.name, uncached[:3]))

    print("STATS")
    for key in sorted(stats):
        print(f"{key}: {stats[key]}")

    print("\nFIXABLE_TOP_DOMAINS")
    for host, count in fixable_domains.most_common(20):
        print(count, host)

    print("\nBLOCKED_TOP_DOMAINS")
    for host, count in blocked_domains.most_common(20):
        print(count, host)

    print("\nUNCACHED_TOP_DOMAINS")
    for host, count in uncached_domains.most_common(20):
        print(count, host)

    print("\nLOW_QUALITY_TOP_DOMAINS")
    for host, count in low_quality_domains.most_common(20):
        print(count, host)

    for label in ("fixable", "blocked", "uncached", "low_quality"):
        print(f"\nEXAMPLES_{label.upper()}")
        for example in examples[label]:
            print(example)


if __name__ == "__main__":
    main()
