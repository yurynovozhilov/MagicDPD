#!/usr/bin/env python3
"""
Обходит все .md файлы в site/content/posts/, извлекает URL из тела поста,
получает OG-метаданные и записывает их в front matter как link_previews.

Кэш хранится в link_previews_cache.json — при повторном запуске уже
обработанные URL перефетчиваться не будут.
"""

import html as html_lib
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import frontmatter
import requests

POSTS_DIR = Path("site/content/posts")
CACHE_FILE = Path("link_previews_cache.json")
URL_RE = re.compile(r"https?://[^\s\)\]>\"'<,]+")
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
    try:
        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT, allow_redirects=True)
        resp.raise_for_status()
        content_type = resp.headers.get("Content-Type", "")
        if "text/html" not in content_type:
            return None
        html = resp.text
    except Exception as exc:
        print(f"  SKIP {url} — {exc}", file=sys.stderr)
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
        "url": url,
        "title": title,
        "description": description,
        "image": image,
    }
    return normalize_preview(preview)


def _youtube_video_id(url: str) -> str | None:
    parsed = urlparse(url)
    host = parsed.netloc.lower()

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


def normalize_preview(preview: dict) -> dict:
    """Backfill provider-specific fields so cached entries can improve over time."""
    url = preview.get("url", "")
    image = (preview.get("image") or "").strip()

    if not image:
        video_id = _youtube_video_id(url)
        if video_id:
            # hqdefault is broadly available and more reliable than maxresdefault.
            preview["image"] = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"

    return preview


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
    urls = URL_RE.findall(body)
    # Убираем дубликаты, сохраняя порядок
    seen: set[str] = set()
    result = []
    for u in urls:
        # Чистим хвостовые пунктуационные символы
        u = u.rstrip(".,;:!?)]")
        if u not in seen and len(u) < 2048:
            seen.add(u)
            result.append(u)
    return result


def is_useful_url(url: str) -> bool:
    """Фильтруем заведомо бесполезные URL (изображения, архивы и т.д.)."""
    parsed = urlparse(url)
    path = parsed.path.lower()
    skip_exts = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg",
                 ".pdf", ".zip", ".tar", ".gz", ".mp4", ".mp3"}
    _, ext = os.path.splitext(path)
    return ext not in skip_exts


def process_post(md_path: Path, cache: dict) -> bool:
    """Обрабатывает один пост. Возвращает True если файл был изменён."""
    raw = md_path.read_text(encoding="utf-8")
    post = frontmatter.loads(raw)

    body = post.content
    urls = [u for u in extract_urls_from_body(body) if is_useful_url(u)]

    if not urls:
        return False

    # Определяем, какие URL ещё не в кэше
    new_urls = [u for u in urls if u not in cache]

    if new_urls:
        print(f"  Fetching {len(new_urls)} new URL(s) in {md_path.name}…")
        for url in new_urls:
            print(f"    → {url}")
            result = fetch_preview(url)
            # Сохраняем даже None, чтобы не перефетчивать неудачные URL
            cache[url] = result

    # Собираем финальный список превью (только успешные)
    previews = []
    for url in urls:
        entry = cache.get(url)
        if entry:
            entry = normalize_preview(dict(entry))
            cache[url] = entry
            previews.append(entry)

    if not previews:
        return False

    # Если данные не изменились — не перезаписываем файл
    existing = post.metadata.get("link_previews", [])
    if existing == previews:
        return False

    post.metadata["link_previews"] = previews

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
