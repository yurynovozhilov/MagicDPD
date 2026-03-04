#!/usr/bin/env python3
"""
Finds VK posts in Hugo that have no external URLs in the body, then checks the
raw VK dump for link/video-player attachments and appends them to the post file.

Matching strategy: match Hugo .md files directly to raw VK dump by
(date_prefix, first_line_of_text). This avoids the unified_posts.json ID
mismatch issue (internal IDs ≠ VK API IDs for newer posts).

Uses only stdlib — no third-party packages needed.
"""
import json
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW_VK = ROOT / "vk" / "magicdpd_raw_dump.json"
SITE_POSTS = ROOT / "site" / "content" / "posts"

URL_RE = re.compile(r"https?://\S+")
FRONT_MATTER_RE = re.compile(r"^---\n.*?\n---\n", re.DOTALL)


def extract_body(md_text: str) -> str:
    m = FRONT_MATTER_RE.match(md_text)
    return md_text[m.end():] if m else md_text


def body_has_urls(md_text: str) -> bool:
    return bool(URL_RE.search(extract_body(md_text)))


def normalize(text: str) -> str:
    """Lowercase + collapse whitespace."""
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def first_body_line(md_text: str) -> str:
    body = extract_body(md_text)
    for line in body.splitlines():
        s = line.strip()
        if s:
            return s
    return ""


def get_links_from_raw(raw_post: dict) -> list[str]:
    """Extract actionable URLs from raw VK post attachments."""
    urls: list[str] = []
    for att in raw_post.get("attachments", []):
        t = att.get("type")
        if t == "link":
            url = att.get("link", {}).get("url", "")
            if url:
                urls.append(url)
        elif t == "video":
            # VK stores YouTube/Vimeo embed URL in the "player" field
            player = att.get("video", {}).get("player", "")
            if player:
                urls.append(player)
    return urls


def format_link_line(url: str, raw_post: dict) -> str:
    """Return markdown link with title from attachment metadata if available."""
    for att in raw_post.get("attachments", []):
        t = att.get("type")
        if t == "link" and att.get("link", {}).get("url") == url:
            title = att["link"].get("title", "").strip()
            if title:
                return f"[{title}]({url})"
        elif t == "video" and att.get("video", {}).get("player", "") == url:
            title = att["video"].get("title", "").strip()
            if title:
                return f"[{title}]({url})"
    return url


def raw_first_line(raw_post: dict) -> str:
    text = raw_post.get("text", "") or ""
    for line in text.splitlines():
        s = line.strip()
        if s:
            return s
    return ""


def main() -> None:
    print("Loading raw VK dump…")
    with open(RAW_VK, encoding="utf-8") as f:
        raw_posts: list[dict] = json.load(f)

    # Build index: (date_prefix, norm_first_line[:100]) → list of raw posts
    print("Building (date, text) index of raw VK posts…")
    raw_index: dict[tuple[str, str], list[dict]] = {}
    for rp in raw_posts:
        dt = datetime.fromtimestamp(rp["date"], tz=timezone.utc)
        date_prefix = dt.date().isoformat()
        fline = normalize(raw_first_line(rp))[:100]
        if not fline:
            continue
        raw_index.setdefault((date_prefix, fline), []).append(rp)

    print(f"Indexed {len(raw_index)} unique (date, text) pairs from {len(raw_posts)} raw posts.")

    print(f"\nScanning {SITE_POSTS} for VK posts without external links…")
    md_files = sorted(SITE_POSTS.glob("*.md"))

    fixed = 0
    skipped_no_match = 0
    skipped_ambiguous = 0
    skipped_no_links_in_raw = 0

    for md_path in md_files:
        text = md_path.read_text(encoding="utf-8")
        if "source: vk" not in text:
            continue
        if body_has_urls(text):
            continue

        date_prefix = md_path.name[:10]
        fline = normalize(first_body_line(text))[:100]
        if not fline:
            skipped_no_match += 1
            continue

        candidates = raw_index.get((date_prefix, fline), [])

        if not candidates:
            skipped_no_match += 1
            continue

        if len(candidates) > 1:
            # Multiple raw posts with same date + first line — skip to avoid wrong match
            skipped_ambiguous += 1
            continue

        raw_post = candidates[0]
        found_urls = get_links_from_raw(raw_post)
        if not found_urls:
            skipped_no_links_in_raw += 1
            continue

        link_lines = "\n".join(format_link_line(u, raw_post) for u in found_urls)
        new_text = text.rstrip("\n") + "\n\n" + link_lines + "\n"
        md_path.write_text(new_text, encoding="utf-8")
        print(f"  FIXED {md_path.name}: +{len(found_urls)} link(s)")
        for u in found_urls:
            print(f"    {u[:100]}")
        fixed += 1

    print(
        f"\nDone. Fixed: {fixed} | "
        f"No raw match: {skipped_no_match} | "
        f"Ambiguous (multiple raw posts): {skipped_ambiguous} | "
        f"Raw has no extractable links: {skipped_no_links_in_raw}"
    )


if __name__ == "__main__":
    main()
