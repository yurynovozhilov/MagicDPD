#!/usr/bin/env python3
"""Convert Wayback dump JSON into Markdown posts for the Jekyll site."""
from __future__ import annotations

import json
import re
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "wayback_dump.json"
SITE_POSTS = ROOT / "site" / "_posts"

DATE_RE = re.compile(r"\b\d{2}\.\d{2}\.\d{4}\b")
SHARE_TOKENS = {"facebook", "twitter", "вконтакте", "google+", "pinterest"}
META_TOKENS = {
    "автор",
    "опубликовано",
    "формат",
    "лента",
    "к записи",
    "к запись",
    "комментарий",
    "комментария",
    "комментариев",
    "добавить комментарий",
    "от",
    "|",
}
SKIP_PATH_PARTS = (
    "/category/",
    "/tag/",
    "/wp-",
    "/author/",
    "/feed",
    "/page/",
    "/wp-json",
    "/comments",
)
SKIP_EXTENSIONS = (".xml", ".txt", ".ico", ".png", ".jpg", ".gif")
SKIP_IMAGE_PATTERNS = ("gravatar", "avatar", "/logo", "cropped-", "-150x150", "lazy_placeholder")
RUS_TO_LAT = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "e",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": "y",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "h",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "sch",
    "ъ": "",
    "ы": "y",
    "ь": "",
    "э": "e",
    "ю": "yu",
    "я": "ya",
}


def load_entries() -> list[dict]:
    if not DATA_PATH.exists():
        raise SystemExit(f"Wayback dump not found: {DATA_PATH}")
    return json.loads(DATA_PATH.read_text())


def normalize_title(raw: str) -> str:
    if not raw:
        return ""
    title = re.sub(r"\s+—\s+MagicDPD.*$", "", raw).strip()
    return title


def transliterate(text: str) -> str:
    text = unquote(text or "").strip("/")
    if not text:
        return ""
    token = text.split("/")[-1]
    token = token.replace(" ", "-")
    buffer: list[str] = []
    for char in token.lower():
        if char in RUS_TO_LAT:
            buffer.append(RUS_TO_LAT[char])
            continue
        if char.isalnum():
            buffer.append(char)
            continue
        if char in {"-", "_"}:
            buffer.append("-")
            continue
        normalized = unicodedata.normalize("NFKD", char).encode("ascii", "ignore").decode()
        if normalized:
            buffer.append(normalized)
        else:
            buffer.append("-")
    slug = re.sub(r"-+", "-", "".join(buffer)).strip("-")
    return slug


def derive_slug(entry: dict, fallback_id: int) -> str:
    parsed = urlparse(entry.get("original_url", ""))
    slug = transliterate(parsed.path)
    if not slug:
        slug = f"post-{fallback_id}"
    return slug


def text_lines(entry: dict) -> list[str]:
    lines = [line.strip() for line in entry.get("text", "").splitlines()]
    return [line for line in lines if line]


def extract_author(lines: list[str]) -> str:
    for idx, line in enumerate(lines):
        if line.lower().startswith("автор"):
            for nxt in lines[idx + 1 : idx + 4]:
                if nxt and not DATE_RE.fullmatch(nxt) and nxt.lower() not in META_TOKENS:
                    return nxt
    for idx, line in enumerate(lines):
        if line.lower().startswith("by "):
            return line[3:].strip()
    return "GlukRazor"


def extract_date(entry: dict, lines: list[str]) -> datetime:
    for idx, line in enumerate(lines):
        if "опублик" in line.lower():
            for nxt in lines[idx + 1 : idx + 6]:
                if nxt and DATE_RE.fullmatch(nxt):
                    return datetime.strptime(nxt, "%d.%m.%Y")
    for line in lines:
        if DATE_RE.fullmatch(line):
            return datetime.strptime(line, "%d.%m.%Y")
    return datetime.fromisoformat(entry["archive_date"])


def should_skip(entry: dict) -> bool:
    url = entry.get("original_url", "")
    text = entry.get("text", "")
    if not text or len(text.strip()) < 50:
        return True
    parsed = urlparse(url)
    path = parsed.path or "/"
    if path in ("/", ""):
        return True
    if any(part in path for part in SKIP_PATH_PARTS):
        return True
    if any(path.endswith(ext) for ext in SKIP_EXTENSIONS):
        return True
    return False


def trim_leading_metadata(lines: list[str], title: str) -> list[str]:
    trimmed: list[str] = []
    skipping = True
    for line in lines:
        low = line.lower()
        if skipping:
            if (
                low in META_TOKENS
                or low.startswith("автор")
                or low.startswith("опублик")
                or low.startswith("к записи")
                or "комментар" in low
                or low.startswith("добавить")
                or low.startswith("от")
                or low in {"glukrazor", "лента", "|"}
                or DATE_RE.fullmatch(line)
                or (title and line == title)
            ):
                continue
            skipping = False
        if low.startswith("к записи"):
            continue
        if low.startswith("метки"):
            break
        if low in SHARE_TOKENS:
            break
        trimmed.append(line)
    while trimmed and (
        trimmed[-1].lower() in META_TOKENS
        or trimmed[-1].lower() in SHARE_TOKENS
        or DATE_RE.fullmatch(trimmed[-1])
        or (title and trimmed[-1] == title)
    ):
        trimmed.pop()
    return trimmed


def lines_to_markdown(lines: Iterable[str]) -> str:
    paragraphs: list[str] = []
    for line in lines:
        if line.startswith("http://") or line.startswith("https://"):
            paragraphs.append(f"[{line}]({line})")
        else:
            paragraphs.append(line)
    return "\n\n".join(paragraphs)


def extract_tags(entry: dict, raw_lines: list[str]) -> list[str]:
    tags = []
    for link in entry.get("links", []):
        url = link.get("url", "")
        if "/tag/" in url:
            text = (link.get("text") or "").strip()
            if text:
                tags.append(text)
    if tags:
        return sorted(set(tags), key=lambda t: t.lower())

    collecting = False
    for line in raw_lines:
        low = line.lower()
        if low.startswith("метки"):
            collecting = True
            continue
        if collecting:
            if low in SHARE_TOKENS or low in META_TOKENS or DATE_RE.fullmatch(line):
                break
            cleaned = line.replace(",", "").strip()
            if cleaned:
                tags.append(cleaned)
    return sorted(set(tags), key=lambda t: t.lower())


def extract_images(entry: dict) -> list[dict]:
    images = []
    seen = set()
    for image in entry.get("images", []):
        url = image.get("wayback_src") or image.get("src")
        if not url:
            continue
        domain_hit = any(pattern in url for pattern in SKIP_IMAGE_PATTERNS)
        if domain_hit:
            continue
        if url in seen:
            continue
        seen.add(url)
        alt = (image.get("alt") or "").strip()
        images.append({"url": url, "alt": alt})
        if len(images) >= 12:
            break
    return images


def guess_title_from_lines(lines: list[str]) -> str:
    for idx, line in enumerate(lines):
        low = line.lower()
        if low.startswith("к записи"):
            candidate = line.split("к записи", 1)[1].strip(" :—-–")
            if candidate:
                return candidate
            if idx + 1 < len(lines):
                nxt = lines[idx + 1].strip()
                if nxt:
                    return nxt
        if low.startswith("title:"):
            candidate = line.split(":", 1)[1].strip()
            if candidate:
                return candidate
    for line in lines:
        low = line.lower()
        if (
            line
            and low not in META_TOKENS
            and not DATE_RE.fullmatch(line)
            and low not in SHARE_TOKENS
            and not low.startswith("автор")
            and not low.startswith("опублик")
            and not low.startswith("добавить")
            and not low.startswith("к запись")
            and line not in {"GlukRazor", "Лента", "|"}
        ):
            return line
    return ""


def build_post(entry: dict, index: int) -> dict | None:
    if should_skip(entry):
        return None
    raw_lines = text_lines(entry)
    title = normalize_title(entry.get("title", ""))
    if not title or title.lower() == "magicdpd":
        title = guess_title_from_lines(raw_lines)
    title = title or "Без названия"
    author = extract_author(raw_lines)
    date = extract_date(entry, raw_lines)
    content_lines = trim_leading_metadata(raw_lines, title)
    if not content_lines and title:
        content_lines = [title]
    if not content_lines:
        return None
    body = lines_to_markdown(content_lines)
    tags = extract_tags(entry, raw_lines)
    images = extract_images(entry)

    return {
        "title": title,
        "author": author,
        "date": date,
        "slug": derive_slug(entry, index),
        "body": body,
        "tags": tags,
        "images": images,
        "original_url": entry.get("original_url"),
        "wayback_url": entry.get("wayback_url"),
    }


def write_post_file(post: dict) -> Path:
    def yaml_quote(value: str) -> str:
        safe = (value or "").replace("\\", "\\\\").replace('"', '\\"')
        return f'"{safe}"'

    SITE_POSTS.mkdir(parents=True, exist_ok=True)
    filename = f"{post['date']:%Y-%m-%d}-{post['slug']}.md"
    path = SITE_POSTS / filename
    front_matter = [
        "---",
        "layout: post",
        f"title: {yaml_quote(post['title'])}",
        f"date: {post['date'].isoformat()}",
        f"author: {yaml_quote(post['author'])}",
    ]
    if post.get("original_url"):
        front_matter.append(f"original_url: {yaml_quote(post['original_url'])}")
    if post.get("wayback_url"):
        front_matter.append(f"wayback_url: {yaml_quote(post['wayback_url'])}")
    if post.get("tags"):
        front_matter.append("tags:")
        for tag in post["tags"]:
            front_matter.append(f"  - {yaml_quote(tag)}")
    if post.get("images"):
        front_matter.append("images:")
        for image in post["images"]:
            url = image["url"]
            alt = image.get("alt", "")
            front_matter.append(f"  - url: {yaml_quote(url)}")
            if alt:
                front_matter.append(f"    alt: {yaml_quote(alt)}")
    front_matter.append("---")
    front_matter.append("\n")
    path.write_text("\n".join(front_matter) + post["body"] + "\n", encoding="utf-8")
    return path


def main() -> None:
    entries = load_entries()
    posts_written = 0
    # clean previous posts
    if SITE_POSTS.exists():
        for file in SITE_POSTS.glob("*.md"):
            file.unlink()
    for idx, entry in enumerate(entries):
        post = build_post(entry, idx)
        if not post:
            continue
        write_post_file(post)
        posts_written += 1
    print(f"Generated {posts_written} posts into {SITE_POSTS}")


if __name__ == "__main__":
    main()
