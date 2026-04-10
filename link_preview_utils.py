#!/usr/bin/env python3
"""Shared helpers for building and ranking link previews."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import parse_qs, urlparse

URL_RE = re.compile(r"https?://[^\s\)\]>\"'<,]+")
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")

SKIP_PREVIEW_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".webp",
    ".svg",
    ".pdf",
    ".zip",
    ".tar",
    ".gz",
    ".mp4",
    ".mp3",
}

SKIP_PREVIEW_HOSTS = {
    "magicdpd.com",
    "www.magicdpd.com",
    "magicdpd.ru",
    "www.magicdpd.ru",
    "doi.org",
    "dx.doi.org",
    "support.ansys.com",
}

SHORTENER_HOSTS = {
    "bit.ly",
    "www.bit.ly",
    "buff.ly",
    "goo.gl",
    "ift.tt",
    "is.gd",
    "lnk.al",
    "ow.ly",
    "t.co",
    "tinyurl.com",
    "trib.al",
    "wp.me",
}

LOW_QUALITY_TITLES = {"", "- YouTube"}


def preview_host(url: str) -> str:
    return urlparse(url).netloc.lower().split(":", 1)[0]


def extract_urls_from_body(body: str) -> list[str]:
    seen: set[str] = set()
    urls: list[str] = []
    for url in URL_RE.findall(body):
        cleaned = url.rstrip(".,;:!?)]")
        if cleaned and cleaned not in seen and len(cleaned) < 2048:
            seen.add(cleaned)
            urls.append(cleaned)
    return urls


def youtube_video_id(url: str) -> str | None:
    parsed = urlparse(url)
    host = preview_host(url)

    if host.endswith("youtu.be"):
        video_id = parsed.path.strip("/").split("/")[0]
        return video_id or None

    if "youtube.com" not in host:
        return None

    if parsed.path == "/watch":
        return parse_qs(parsed.query).get("v", [None])[0]

    if parsed.path.startswith("/shorts/"):
        video_id = parsed.path.split("/", 2)[2]
        return video_id or None

    return None


def canonicalize_preview_url(url: str) -> str:
    if not url:
        return url

    video_id = youtube_video_id(url)
    if video_id:
        return f"https://www.youtube.com/watch?v={video_id}"

    return url


def cache_lookup_keys(url: str) -> list[str]:
    keys: list[str] = []
    for candidate in (url, canonicalize_preview_url(url)):
        if candidate and candidate not in keys:
            keys.append(candidate)
    return keys


def is_linkedin_profile_url(url: str) -> bool:
    host = preview_host(url)
    return host.endswith("linkedin.com") and urlparse(url).path.startswith("/in/")


def should_skip_preview_url(url: str) -> bool:
    host = preview_host(url)
    return host in SKIP_PREVIEW_HOSTS or is_linkedin_profile_url(url)


def is_useful_preview_url(url: str) -> bool:
    if should_skip_preview_url(url):
        return False

    ext = Path(urlparse(url).path.lower()).suffix.lower()
    return ext not in SKIP_PREVIEW_EXTENSIONS


def collect_markdown_link_labels(body: str) -> dict[str, str]:
    labels: dict[str, str] = {}
    for label, url in MARKDOWN_LINK_RE.findall(body):
        clean_label = label.strip()
        if not clean_label or clean_label == url:
            continue
        for key in cache_lookup_keys(url):
            labels.setdefault(key, clean_label)
    return labels


def preview_has_content(preview: dict) -> bool:
    return any((preview.get(key) or "").strip() for key in ("title", "description", "image"))


def looks_like_mojibake(text: str) -> bool:
    return text.count("Ð") + text.count("Ñ") >= 3


def is_low_quality_youtube_title(url: str, title: str) -> bool:
    host = preview_host(url)
    return ("youtube.com" in host or host.endswith("youtu.be")) and title in LOW_QUALITY_TITLES


def preview_is_usable(preview: dict) -> bool:
    if not preview_has_content(preview):
        return False

    url = preview.get("url", "")
    host = preview_host(url)
    title = (preview.get("title") or "").strip()

    if host in SHORTENER_HOSTS:
        return False

    if "/preview/deprecated/" in url:
        return False

    if title and looks_like_mojibake(title):
        return False

    if is_low_quality_youtube_title(url, title):
        return False

    return True


def preview_priority(preview: dict) -> int:
    host = preview_host(preview.get("url", ""))
    score = 0

    if (preview.get("title") or "").strip():
        score += 4
    if (preview.get("description") or "").strip():
        score += 2
    if (preview.get("image") or "").strip():
        score += 4

    if "youtube.com" in host or host.endswith("youtu.be"):
        score += 1

    return score


def normalize_preview(preview: dict, label_map: dict[str, str] | None = None) -> dict:
    normalized = dict(preview)
    url = canonicalize_preview_url(normalized.get("url", ""))
    title = (normalized.get("title") or "").strip()
    description = (normalized.get("description") or "").strip()
    image = (normalized.get("image") or "").strip()

    if title in LOW_QUALITY_TITLES and label_map and url in label_map:
        title = label_map[url]

    if not image:
        video_id = youtube_video_id(url)
        if video_id:
            image = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"

    normalized["url"] = url
    normalized["title"] = title
    normalized["description"] = description
    normalized["image"] = image
    return normalized


def preview_needs_refresh(preview: dict | None, source_url: str) -> bool:
    if should_skip_preview_url(source_url):
        return False

    if not isinstance(preview, dict):
        return True

    normalized = normalize_preview(preview)
    url = normalized.get("url", "") or canonicalize_preview_url(source_url)
    host = preview_host(url)
    title = (normalized.get("title") or "").strip()

    if host in SHORTENER_HOSTS:
        return True

    if not preview_is_usable(normalized):
        return True

    if is_low_quality_youtube_title(url, title):
        return True

    return False


def best_cached_preview(url: str, cache: dict, label_map: dict[str, str] | None = None) -> dict | None:
    for key in cache_lookup_keys(url):
        candidate = cache.get(key)
        if isinstance(candidate, dict):
            preview = normalize_preview(candidate, label_map)
            if preview_is_usable(preview):
                return preview
    return None


def build_link_previews_from_cache(body: str, cache: dict) -> list[dict]:
    urls = [url for url in extract_urls_from_body(body) if is_useful_preview_url(url)]
    if not urls:
        return []

    label_map = collect_markdown_link_labels(body)
    previews: list[tuple[int, int, dict]] = []

    for index, url in enumerate(urls):
        preview = best_cached_preview(url, cache, label_map)
        if preview:
            previews.append((preview_priority(preview), index, preview))

    previews.sort(key=lambda item: (-item[0], item[1]))
    return [preview for _, _, preview in previews]
