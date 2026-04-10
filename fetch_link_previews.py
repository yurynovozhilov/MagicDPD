#!/usr/bin/env python3
"""
Обходит все .md файлы в site/content/posts/, извлекает URL из тела поста,
получает OG-метаданные и записывает их в front matter как link_previews.

Кэш хранится в link_previews_cache.json — при повторном запуске уже
обработанные URL перефетчиваться не будут.
"""

import html as html_lib
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

import frontmatter
import requests
from link_preview_utils import (
    cache_lookup_keys,
    canonicalize_preview_url,
    collect_markdown_link_labels,
    extract_urls_from_body as util_extract_urls_from_body,
    is_useful_preview_url,
    normalize_preview as util_normalize_preview,
    preview_has_content as util_preview_has_content,
    preview_needs_refresh,
    preview_priority as util_preview_priority,
)

POSTS_DIR = Path("site/content/posts")
CACHE_FILE = Path("link_previews_cache.json")
REQUEST_TIMEOUT = 5  # секунд

# Заголовки, которые имитируют обычный браузер (избегаем 403)
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; LinkPreviewBot/1.0; "
        "+https://github.com/yurynovozhilov/MagicDPD)"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}


def load_cache() -> dict:
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {}


def save_cache(cache: dict) -> None:
    CACHE_FILE.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def fetch_preview(url: str) -> dict | None:
    """Возвращает dict с title/description/image или None при ошибке."""
    request_url = canonicalize_preview_url(url)
    try:
        resp = requests.get(request_url, headers=HEADERS, timeout=REQUEST_TIMEOUT, allow_redirects=True)
        resp.raise_for_status()
        content_type = resp.headers.get("Content-Type", "")
        if "text/html" not in content_type:
            return None
        html = resp.text
    except Exception as exc:
        print(f"  SKIP {request_url} — {exc}", file=sys.stderr)
        return None

    # Парсим OG / стандартные мета-теги без внешних зависимостей
    title = _extract_meta(html, "og:title") or _extract_title(html) or ""
    description = _extract_meta(html, "og:description") or _extract_meta(html, "description") or ""
    image = _extract_meta(html, "og:image") or ""

    # Decode HTML entities (e.g. &amp; → &, &lt; → <) so we store clean values
    title = html_lib.unescape(title[:200].strip())
    description = html_lib.unescape(description[:500].strip())
    image = html_lib.unescape(image.strip())

    # Skip entries with truncated/useless descriptions
    if len(description) < 5:
        description = ""

    preview = {
        "url": canonicalize_preview_url(resp.url or request_url),
        "title": title,
        "description": description,
        "image": image,
    }

    if preview["title"] in {"", "- YouTube"} and "youtube.com" in urlparse(preview["url"]).netloc.lower():
        oembed = _fetch_youtube_oembed(preview["url"])
        if oembed.get("title"):
            preview["title"] = oembed["title"]
        if not preview["image"] and oembed.get("thumbnail_url"):
            preview["image"] = oembed["thumbnail_url"]

    return util_normalize_preview(preview)


def _fetch_youtube_oembed(url: str) -> dict:
    try:
        resp = requests.get(
            "https://www.youtube.com/oembed",
            params={"url": url, "format": "json"},
            headers=HEADERS,
            timeout=min(REQUEST_TIMEOUT, 3),
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        return {}

    return {
        "title": html_lib.unescape((data.get("title") or "").strip()),
        "thumbnail_url": html_lib.unescape((data.get("thumbnail_url") or "").strip()),
    }


def _extract_meta(html: str, name: str) -> str:
    """Извлекает content из <meta property="name"> или <meta name="name">."""
    patterns = [
        rf'<meta[^>]+property=["\']{{?{re.escape(name)}}}?["\'][^>]+content=["\']([^"\']*)["\']',
        rf'<meta[^>]+content=["\']([^"\']*)["\'][^>]+property=["\']{{?{re.escape(name)}}}?["\']',
        rf'<meta[^>]+name=["\']{{?{re.escape(name)}}}?["\'][^>]+content=["\']([^"\']*)["\']',
        rf'<meta[^>]+content=["\']([^"\']*)["\'][^>]+name=["\']{{?{re.escape(name)}}}?["\']',
    ]
    for pat in patterns:
        m = re.search(pat, html, re.IGNORECASE)
        if m:
            return m.group(1).strip()
    return ""


def _extract_title(html: str) -> str:
    m = re.search(r"<title[^>]*>([^<]+)</title>", html, re.IGNORECASE)
    return m.group(1).strip() if m else ""


def extract_urls_from_body(body: str) -> list[str]:
    """Извлекает URL из markdown-тела поста (не из front matter)."""
    return util_extract_urls_from_body(body)


def is_useful_url(url: str) -> bool:
    """Фильтруем заведомо бесполезные URL (изображения, архивы и т.д.)."""
    return is_useful_preview_url(url)


def process_post(md_path: Path, cache: dict) -> bool:
    """Обрабатывает один пост. Возвращает True если файл был изменён."""
    raw = md_path.read_text(encoding="utf-8")
    post = frontmatter.loads(raw)

    body = post.content
    urls = [u for u in extract_urls_from_body(body) if is_useful_url(u)]
    label_map = collect_markdown_link_labels(body)

    if not urls:
        return False

    refresh_urls = []
    for url in urls:
        cached = None
        found_cached = False
        for key in cache_lookup_keys(url):
            if key in cache:
                found_cached = True
                cached = cache[key]
                break
        if not found_cached:
            refresh_urls.append(url)
        elif isinstance(cached, dict) and preview_needs_refresh(cached, url):
            refresh_urls.append(url)

    if refresh_urls:
        print(f"  Fetching {len(refresh_urls)} URL(s) in {md_path.name}…")
        for url in refresh_urls:
            print(f"    → {url}")
            result = fetch_preview(url)
            # Сохраняем даже None, чтобы не перефетчивать неудачные URL
            cache[url] = result
            if isinstance(result, dict):
                for key in cache_lookup_keys(result.get("url", "")):
                    cache[key] = result

    # Собираем финальный список превью (только успешные)
    previews: list[tuple[int, int, dict]] = []
    for index, url in enumerate(urls):
        entry = None
        for key in cache_lookup_keys(url):
            candidate = cache.get(key)
            if isinstance(candidate, dict):
                entry = dict(candidate)
                break
        if entry:
            entry["url"] = entry.get("url") or url
            entry = util_normalize_preview(entry, label_map)
            cache[url] = entry
            if util_preview_has_content(entry):
                previews.append((util_preview_priority(entry), index, entry))

    previews.sort(key=lambda item: (-item[0], item[1]))
    previews_data = [entry for _, _, entry in previews]

    # Если данные не изменились — не перезаписываем файл
    existing = post.metadata.get("link_previews", [])
    if not previews_data:
        if "link_previews" not in post.metadata:
            return False
        del post.metadata["link_previews"]
    elif existing == previews_data:
        return False
    else:
        post.metadata["link_previews"] = previews_data

    # Записываем обратно в файл
    md_path.write_text(frontmatter.dumps(post) + "\n", encoding="utf-8")
    return True


def main() -> None:
    cache = load_cache()
    # Process newest files first so homepage/archive content gets previews
    # even when CI runtime is limited.
    md_files = sorted(POSTS_DIR.glob("**/*.md"), reverse=True)
    print(f"Processing {len(md_files)} posts…")

    changed = 0
    for md_path in md_files:
        result = process_post(md_path, cache)
        if result:
            changed += 1

    save_cache(cache)
    print(f"Done. {changed} file(s) updated.")


if __name__ == "__main__":
    main()
