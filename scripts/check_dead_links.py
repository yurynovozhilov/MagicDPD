#!/usr/bin/env python3
"""Find dead links in MagicDPD blog posts and replace with Web Archive versions.

Subcommands:
  extract  - Extract all external links from posts
  check    - Check link availability (HTTP HEAD/GET, YouTube oembed)
  archive  - Query Wayback Machine for dead links
  update   - Patch posts with archive URLs
"""

import argparse
import asyncio
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import aiohttp
import yaml
from tqdm import tqdm

POSTS_DIR = Path(__file__).parent.parent / "site" / "content" / "posts"
SCRIPTS_DIR = Path(__file__).parent

LINKS_INDEX = SCRIPTS_DIR / "links_index.json"
LINKS_STATUS = SCRIPTS_DIR / "links_status.json"
ARCHIVE_RESULTS = SCRIPTS_DIR / "archive_results.json"

SKIP_DOMAINS = {"magicdpd.ru", "www.magicdpd.ru", "localhost", "127.0.0.1"}

# Regex for markdown links: [text](url)
MD_LINK_RE = re.compile(r'\[([^\]]*)\]\((https?://[^)]+)\)')
# Regex for raw URLs not inside markdown link syntax
RAW_URL_RE = re.compile(r'(?<!\()(https?://[^\s\)<>"]+)')

YOUTUBE_DOMAINS = {"youtube.com", "www.youtube.com", "youtu.be", "m.youtube.com"}


def load_json(path):
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def parse_front_matter(text):
    """Parse YAML front matter from markdown file."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fm_text = text[3:end].strip()
    body = text[end + 4:].lstrip("\n")
    try:
        fm = yaml.safe_load(fm_text)
    except yaml.YAMLError:
        fm = {}
    return fm or {}, body


def is_external(url):
    try:
        host = urlparse(url).hostname
        if not host:
            return False
        return host not in SKIP_DOMAINS
    except Exception:
        return False


def extract_links():
    """Extract all external links from posts."""
    index = {}  # url -> [{file, line, format, text}]
    files = sorted(POSTS_DIR.glob("*.md"))

    for fpath in tqdm(files, desc="Extracting links"):
        text = fpath.read_text(encoding="utf-8")
        fm, body = parse_front_matter(text)
        rel_path = str(fpath.relative_to(POSTS_DIR.parent.parent))

        # Extract from link_previews in front matter
        previews = fm.get("link_previews") or []
        for lp in previews:
            url = lp.get("url", "")
            if url and is_external(url):
                index.setdefault(url, []).append({
                    "file": rel_path,
                    "line": 0,
                    "format": "link_preview",
                    "text": lp.get("title", ""),
                })

        # Extract from body
        lines = text.split("\n")
        in_front_matter = False
        for i, line in enumerate(lines, 1):
            if i == 1 and line.strip() == "---":
                in_front_matter = True
                continue
            if in_front_matter:
                if line.strip() == "---":
                    in_front_matter = False
                continue

            # Markdown links
            for m in MD_LINK_RE.finditer(line):
                url = m.group(2)
                if is_external(url):
                    index.setdefault(url, []).append({
                        "file": rel_path,
                        "line": i,
                        "format": "markdown",
                        "text": m.group(1),
                    })

            # Raw URLs (not already captured as markdown links)
            md_spans = [(m.start(2), m.end(2)) for m in MD_LINK_RE.finditer(line)]
            for m in RAW_URL_RE.finditer(line):
                start, end = m.start(), m.end()
                # Skip if this URL is inside a markdown link's URL part
                if any(ms <= start and end <= me for ms, me in md_spans):
                    continue
                # Skip if preceded by ]( — it's a markdown link URL
                prefix = line[:start]
                if prefix.endswith("]("):
                    continue
                url = m.group(0)
                if is_external(url):
                    index.setdefault(url, []).append({
                        "file": rel_path,
                        "line": i,
                        "format": "raw",
                        "text": "",
                    })

    save_json(LINKS_INDEX, index)
    unique = len(index)
    total = sum(len(v) for v in index.values())
    print(f"Extracted {unique} unique URLs ({total} total occurrences) from {len(files)} posts")
    print(f"Saved to {LINKS_INDEX}")


def is_youtube_url(url):
    try:
        host = urlparse(url).hostname
        return host in YOUTUBE_DOMAINS
    except Exception:
        return False


async def check_single_url(session, url, semaphore, rate_limiter):
    """Check a single URL. Returns (url, {status, code, error})."""
    async with semaphore:
        await rate_limiter.acquire()
        try:
            # YouTube: use oembed API
            if is_youtube_url(url):
                oembed_url = f"https://www.youtube.com/oembed?url={url}&format=json"
                async with session.get(oembed_url, timeout=aiohttp.ClientTimeout(total=10),
                                       allow_redirects=True) as resp:
                    if resp.status == 200:
                        return url, {"status": "alive", "code": 200, "error": None}
                    else:
                        return url, {"status": "dead", "code": resp.status, "error": "YouTube oembed returned non-200"}

            # Regular URLs: HEAD first, fallback to GET on 405
            try:
                async with session.head(url, timeout=aiohttp.ClientTimeout(total=10),
                                        allow_redirects=True) as resp:
                    code = resp.status
                    if code == 405:
                        raise aiohttp.ClientResponseError(
                            request_info=resp.request_info,
                            history=resp.history,
                            status=405
                        )
                    if code in (404, 410, 403):
                        return url, {"status": "dead", "code": code, "error": None}
                    return url, {"status": "alive", "code": code, "error": None}
            except (aiohttp.ClientResponseError,) as e:
                if getattr(e, 'status', 0) == 405:
                    async with session.get(url, timeout=aiohttp.ClientTimeout(total=10),
                                           allow_redirects=True) as resp:
                        code = resp.status
                        if code in (404, 410, 403):
                            return url, {"status": "dead", "code": code, "error": None}
                        return url, {"status": "alive", "code": code, "error": None}
                raise

        except asyncio.TimeoutError:
            return url, {"status": "dead", "code": None, "error": "timeout"}
        except aiohttp.ClientConnectorError as e:
            return url, {"status": "dead", "code": None, "error": f"connection_error: {e}"}
        except aiohttp.ClientError as e:
            return url, {"status": "dead", "code": None, "error": str(e)}
        except Exception as e:
            return url, {"status": "dead", "code": None, "error": str(e)}


class RateLimiter:
    """Simple token-bucket rate limiter."""
    def __init__(self, rate):
        self.rate = rate
        self.interval = 1.0 / rate
        self.last = 0

    async def acquire(self):
        now = time.monotonic()
        wait = self.last + self.interval - now
        if wait > 0:
            await asyncio.sleep(wait)
        self.last = time.monotonic()


async def check_links(limit=None):
    """Check all extracted links for availability."""
    index = load_json(LINKS_INDEX)
    if not index:
        print("No links index found. Run 'extract' first.")
        return

    status = load_json(LINKS_STATUS)
    urls = [u for u in index if u not in status]

    if limit:
        urls = urls[:limit]

    if not urls:
        print("All URLs already checked.")
        return

    print(f"Checking {len(urls)} URLs ({len(status)} already done)...")

    semaphore = asyncio.Semaphore(20)
    rate_limiter = RateLimiter(5)

    connector = aiohttp.TCPConnector(limit=20, ssl=False)
    async with aiohttp.ClientSession(
        connector=connector,
        headers={"User-Agent": "Mozilla/5.0 (compatible; MagicDPD-LinkChecker/1.0)"}
    ) as session:
        tasks = [check_single_url(session, url, semaphore, rate_limiter) for url in urls]

        done_count = 0
        dead_count = 0
        with tqdm(total=len(tasks), desc="Checking links") as pbar:
            for coro in asyncio.as_completed(tasks):
                url, result = await coro
                status[url] = result
                done_count += 1
                if result["status"] == "dead":
                    dead_count += 1
                pbar.update(1)

                # Save periodically
                if done_count % 100 == 0:
                    save_json(LINKS_STATUS, status)

    save_json(LINKS_STATUS, status)
    total_dead = sum(1 for v in status.values() if v["status"] == "dead")
    print(f"Done. {dead_count} dead out of {len(urls)} checked this run.")
    print(f"Total: {total_dead} dead out of {len(status)} checked overall.")
    print(f"Saved to {LINKS_STATUS}")


async def query_wayback(session, url, semaphore, rate_limiter):
    """Query Wayback Machine for a single URL."""
    async with semaphore:
        await rate_limiter.acquire()
        try:
            api_url = f"https://archive.org/wayback/available?url={url}"
            async with session.get(api_url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status != 200:
                    return url, None
                data = await resp.json()
                snapshot = data.get("archived_snapshots", {}).get("closest")
                if snapshot and snapshot.get("available"):
                    return url, snapshot["url"]
                return url, None
        except Exception:
            return url, None


async def search_archive():
    """Query Wayback Machine for all dead links."""
    status = load_json(LINKS_STATUS)
    if not status:
        print("No link status found. Run 'check' first.")
        return

    archive = load_json(ARCHIVE_RESULTS)
    dead_urls = [u for u, v in status.items() if v["status"] == "dead" and u not in archive]

    if not dead_urls:
        print("All dead URLs already queried.")
        return

    print(f"Querying Wayback Machine for {len(dead_urls)} dead URLs ({len(archive)} already done)...")

    semaphore = asyncio.Semaphore(10)
    rate_limiter = RateLimiter(3)

    connector = aiohttp.TCPConnector(limit=10)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [query_wayback(session, url, semaphore, rate_limiter) for url in dead_urls]

        found = 0
        with tqdm(total=len(tasks), desc="Querying Wayback") as pbar:
            for i, coro in enumerate(asyncio.as_completed(tasks)):
                url, archive_url = await coro
                archive[url] = archive_url
                if archive_url:
                    found += 1
                pbar.update(1)

                if (i + 1) % 50 == 0:
                    save_json(ARCHIVE_RESULTS, archive)

    save_json(ARCHIVE_RESULTS, archive)
    total_found = sum(1 for v in archive.values() if v)
    print(f"Found {found} archive URLs this run.")
    print(f"Total: {total_found} archived out of {len(archive)} dead URLs.")
    print(f"Saved to {ARCHIVE_RESULTS}")


def update_posts(dry_run=False):
    """Patch posts with archive URLs for dead links."""
    index = load_json(LINKS_INDEX)
    archive = load_json(ARCHIVE_RESULTS)

    if not index or not archive:
        print("Missing data. Run 'extract', 'check', and 'archive' first.")
        return

    # Build map: dead_url -> archive_url (only those with archives)
    replacements = {url: arch_url for url, arch_url in archive.items() if arch_url}
    if not replacements:
        print("No archive URLs found. Nothing to update.")
        return

    # Group by file, deduplicate by URL per file
    file_urls = {}
    for url, occurrences in index.items():
        if url not in replacements:
            continue
        for occ in occurrences:
            fkey = occ["file"]
            if fkey not in file_urls:
                file_urls[fkey] = {}
            # Keep one entry per URL per file; prefer markdown > raw > link_preview
            fmt_priority = {"markdown": 0, "raw": 1, "link_preview": 2}
            existing = file_urls[fkey].get(url)
            if existing is None or fmt_priority.get(occ["format"], 9) < fmt_priority.get(existing["format"], 9):
                file_urls[fkey][url] = {
                    "url": url,
                    "archive_url": replacements[url],
                    "format": occ["format"],
                    "text": occ["text"],
                }

    print(f"Updating {len(file_urls)} files with {len(replacements)} dead link replacements...")

    updated_count = 0
    base_dir = POSTS_DIR.parent.parent

    for rel_path, url_map in tqdm(file_urls.items(), desc="Updating posts"):
        fpath = base_dir / rel_path
        if not fpath.exists():
            continue

        text = fpath.read_text(encoding="utf-8")
        original = text

        # Split into front matter and body to handle them separately
        fm_text = ""
        body = text
        if text.startswith("---"):
            end = text.find("\n---", 3)
            if end != -1:
                fm_text = text[:end + 4]
                body = text[end + 4:]

        for url, entry in url_map.items():
            archive_url = entry["archive_url"]

            # 1. Update link_preview in front matter (always, if present)
            if f"url: {url}" in fm_text:
                fm_text = fm_text.replace(
                    f"url: {url}",
                    f"url: {archive_url}\n  original_url: {url}",
                    1,
                )

            # 2. Replace markdown links in body: [text](url)
            md_pattern = re.compile(
                r'\[([^\]]*)\]\(' + re.escape(url) + r'\)'
            )
            archive_url_captured = archive_url  # capture for closure
            def md_repl(m, _archive_url=archive_url_captured):
                orig = m.group(0)
                return (
                    f"~~{orig}~~ → [Сохранённая версия]({_archive_url})\n\n"
                    f"*Оригинальная ссылка больше не доступна*"
                )
            body = md_pattern.sub(md_repl, body)

            # 3. Replace remaining raw URLs in body (not inside markdown links or already replaced)
            # Use negative lookbehind for ( and ~~ to avoid double-replacement
            escaped = re.escape(url)
            raw_pattern = re.compile(r'(?<![~(])' + escaped + r'(?![)~])')
            raw_replacement = (
                f"~~{url}~~ → [Сохранённая версия]({archive_url})\n\n"
                f"*Оригинальная ссылка больше не доступна*"
            )
            body = raw_pattern.sub(raw_replacement, body)

        text = fm_text + body
        if text != original:
            if dry_run:
                print(f"  Would update: {rel_path}")
            else:
                fpath.write_text(text, encoding="utf-8")
            updated_count += 1

    action = "Would update" if dry_run else "Updated"
    print(f"{action} {updated_count} files.")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("extract", help="Extract all external links from posts")

    check_p = sub.add_parser("check", help="Check link availability")
    check_p.add_argument("--limit", type=int, help="Limit number of URLs to check")

    sub.add_parser("archive", help="Query Wayback Machine for dead links")

    update_p = sub.add_parser("update", help="Patch posts with archive URLs")
    update_p.add_argument("--dry-run", action="store_true", help="Show what would be changed without modifying files")

    args = parser.parse_args()

    if args.command == "extract":
        extract_links()
    elif args.command == "check":
        asyncio.run(check_links(limit=args.limit))
    elif args.command == "archive":
        asyncio.run(search_archive())
    elif args.command == "update":
        update_posts(dry_run=args.dry_run)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
