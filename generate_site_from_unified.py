#!/usr/bin/env python3
"""Convert Unified VK+TG dump JSON into Markdown posts for the Jekyll site."""
import json
import re
import shutil
import unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "unified_posts.json"
SITE_POSTS = ROOT / "site" / "content" / "posts"

# Known source identifiers for building canonical URLs
VK_OWNER_ID = -97265142  # magicdpd public page
TG_CHANNEL = "magicdpd"

RUS_TO_LAT = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e", "ж": "zh",
    "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o",
    "п": "p", "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f", "х": "h", "ц": "ts",
    "ч": "ch", "ш": "sh", "щ": "sch", "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya",
}

def transliterate(text: str) -> str:
    # Remove unsafe characters from the start
    text = re.sub(r'[!@#$%^&*()\[\]{};:\'\",.<>?/\\|`~]', '', text or "")
    text = text.replace(" ", "-")
    buffer: list[str] = []
    for char in text.lower():
        if char in RUS_TO_LAT:
            buffer.append(RUS_TO_LAT[char])
        elif char.isalnum():
            buffer.append(char)
        elif char in {"-", "_"}:
            buffer.append("-")
        else:
            normalized = unicodedata.normalize("NFKD", char).encode("ascii", "ignore").decode()
            if normalized:
                buffer.append(normalized)
            else:
                buffer.append("-")
    slug = re.sub(r"-+", "-", "".join(buffer)).strip("-")
    return slug

def _is_tag_only_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False

    # Plain hashtags: "#AI #ML #Dataset"
    if re.fullmatch(r'(?:#\w+\s*)+', stripped):
        return True

    # Legacy generated markdown links with Liquid template:
    # [#AI]({{ "/archive/" | relative_url }}#AI) [#ML](...)
    if re.fullmatch(
        r'(?:\[#\w+\]\(\{\{\s*"/archive/"\s*\|\s*relative_url\s*\}\}#\w+\)\s*)+',
        stripped,
    ):
        return True

    return False

def remove_trailing_tag_lines(text: str) -> str:
    lines = text.splitlines()

    # Trim tail whitespace-only lines first.
    while lines and not lines[-1].strip():
        lines.pop()

    # Remove one or more trailing tag-only lines.
    while lines and _is_tag_only_line(lines[-1]):
        lines.pop()
        while lines and not lines[-1].strip():
            lines.pop()

    return "\n".join(lines)

def derive_slug(post: dict) -> str:
    text = post.get("text", "")
    # Try to get first few words of title or text
    title= post.get("title")
    if not title and text:
        # Take first 40 chars of first line
        first_line = text.splitlines()[0] if text else ""
        title = first_line[:40]
    
    slug = transliterate(title or "")
    if not slug:
        slug = f"post-{post.get('id', 'unknown')}"
    return slug

def _build_media_index() -> dict[str, Path]:
    index: dict[str, Path] = {}
    media_dir = ROOT / "magicdpd_media"
    if media_dir.exists():
        for p in media_dir.iterdir():
            if p.suffix.lower() in {".jpg", ".png", ".gif"}:
                index[p.stem] = p
    return index


def _build_images_index() -> dict[str, list[Path]]:
    index: dict[str, list[Path]] = {}
    images_dir = ROOT / "images"
    if images_dir.exists():
        for p in images_dir.iterdir():
            if p.suffix.lower() == ".jpg":
                parts = p.stem.split("_", 2)
                if len(parts) >= 2 and parts[0] == "post":
                    key = f"post_{parts[1]}"
                    index.setdefault(key, []).append(p)
    return index


def _copy_to_assets(src: Path, name: str) -> str:
    target = SITE_POSTS.parent / "assets" / "images" / name
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy(src, target)
        except OSError:
            pass
    return f"/assets/images/{name}"


def extract_images(
    post: dict,
    media_index: dict[str, Path],
    images_index: dict[str, list[Path]],
) -> list[dict]:
    images = []
    post_id_global = post.get("id")
    media = post.get("media", [])
    if not media:
        for key in (str(post_id_global),):
            if key in media_index:
                p = media_index[key]
                images.append({"url": _copy_to_assets(p, p.name), "alt": ""})
                return images
        return []

    for item in media:
        if item.get("type") == "photo":
            photo_id = item.get("id")
            post_id = item.get("post_id") or post_id_global

            found_path = None

            # 1. Try magicdpd_media/{post_id}.*
            key = str(post_id)
            if key in media_index:
                p = media_index[key]
                found_path = _copy_to_assets(p, p.name)

            # 2. Try images/post_{post_id}_*.jpg via pre-built index
            if not found_path:
                matches = images_index.get(f"post_{post_id}", [])
                if matches:
                    p = matches[0]
                    found_path = _copy_to_assets(p, p.name)

            # 3. Try magicdpd_media/{photo_id}.*
            if not found_path and photo_id:
                key = str(photo_id)
                if key in media_index:
                    p = media_index[key]
                    found_path = _copy_to_assets(p, p.name)

            if found_path:
                images.append({"url": found_path, "alt": ""})

    return images


def build_post(
    post: dict,
    media_index: dict[str, Path],
    images_index: dict[str, list[Path]],
) -> dict | None:
    text = (post.get("text") or "").strip()
    if not text and not post.get("media"):
        return None
        
    source = post.get("source", "unknown")
    if source != "vk":
        # Static blog now shows only VK posts
        return None
    date_str = post.get("date")
    if not date_str:
        return None
        
    try:
        if "T" in date_str:
            date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        else:
            date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except:
        return None

    # Step 1: Extract and clean up title
    lines = [line.strip() for line in text.splitlines()]
    
    # Remove leading "Метки:" or "Рубрики:" lines if they exist
    while lines and any(lines[0].startswith(prefix) for prefix in ["Метки:", "Рубрики:", "Tags:", "Categories:"]):
        lines.pop(0)
    
    title = post.get("title")
    if not title and lines:
        title = lines[0][:60]
        # If we took the title from the first line, we must remove it from the body
        lines.pop(0)
    elif title and lines:
        first_line_lower = lines[0].lower().strip()
        title_lower = title.strip().lower()
        # Remove first line if it is the title or starts with the title text
        if first_line_lower == title_lower or first_line_lower.startswith(title_lower):
            lines.pop(0)

    if not title:
        title = f"Post from {source.upper()}"

    # Clean up empty lines at the start
    while lines and not lines[0]:
        lines.pop(0)
        
    clean_text = "\n".join(lines)
    
    # Extract tags from the cleaned text
    # Tags are typically #word
    tags = list(set(re.findall(r'#(\w+)', clean_text)))

    # Global removals as requested by user
    # Remove "by GlukRazor" (case-insensitive)
    clean_text = re.sub(r'(?i)\bby\s+GlukRazor\b', '', clean_text)
    
    # Remove structural words "Метки:", "Рубрики:", etc. (typically at start of lines)
    # Using a regex that handles potential whitespace
    clean_text = re.sub(r'^[ \t]*(Метки|Рубрики|Tags|Categories):\s*', '', clean_text, flags=re.MULTILINE)

    # Keep URLs as-is; do not inject extra callouts or markdown links.
    body = clean_text
    
    # Convert pseudo-bullets (–, —, •, ·) at the start of lines to standard markdown bullets (-)
    body = re.sub(r'^[ \t]*[–—•·][ \t]*', '- ', body, flags=re.MULTILINE)

    # Remove trailing hashtag blocks if they were appended at the end of a post.
    body = remove_trailing_tag_lines(body)

    # Calculate original post URL on the source platform
    original_url = None
    post_id = post.get("id") or post.get("grouped_id")
    if post_id:
        if source == "vk":
            original_url = f"https://vk.com/wall{VK_OWNER_ID}_{post_id}"
        elif source == "tg":
            original_url = f"https://t.me/{TG_CHANNEL}/{post_id}"

    return {
        "title": title,
        "author": post.get("post_author") or "GlukRazor",
        "date": date,
        "slug": derive_slug(post),
        "body": body,
        "tags": tags,
        "source": source,
        "images": extract_images(post, media_index, images_index),
        "original_url": original_url,
    }

def write_post_file(post: dict):
    SITE_POSTS.mkdir(parents=True, exist_ok=True)
    filename = f"{post['date']:%Y-%m-%d}-{post['slug']}.md"
    path = SITE_POSTS / filename
    
    title_safe = post['title'].replace('"', '\\"')
    author_safe = post['author'].replace('"', '\\"')
    
    front_matter = [
        "---",
        "layout: post",
        f'title: "{title_safe}"',
        f"date: {post['date'].isoformat()}",
        f'author: "{author_safe}"',
        f"source: {post['source']}",
    ]

    if post.get("original_url"):
        front_matter.append(f"original_url: {post['original_url']}")
    
    if post.get("tags"):
        front_matter.append("tags:")
        for tag in post["tags"]:
            front_matter.append(f"  - {tag}")

    if post.get("images"):
        front_matter.append("images:")
        for img in post["images"]:
            front_matter.append(f"  - url: \"{img['url']}\"")
            
    front_matter.append("---")
    front_matter.append("\n")
    
    content = "\n".join(front_matter) + post["body"] + "\n"
    path.write_text(content, encoding="utf-8")

def main():
    if not DATA_PATH.exists():
        print(f"Error: {DATA_PATH} not found.")
        return

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        posts = json.load(f)

    print("Building file indexes...")
    media_index = _build_media_index()
    images_index = _build_images_index()
    print(f"  magicdpd_media: {len(media_index)} files, images/: {sum(len(v) for v in images_index.values())} files")

    # Clear old posts
    if SITE_POSTS.exists():
        print(f"Cleaning {SITE_POSTS}...")
        for file in SITE_POSTS.glob("*.md"):
            file.unlink()

    def process(p: dict) -> int:
        post_data = build_post(p, media_index, images_index)
        if post_data:
            write_post_file(post_data)
            return 1
        return 0

    count = 0
    with ThreadPoolExecutor() as executor:
        for result in executor.map(process, posts):
            count += result

    print(f"Successfully generated {count} posts into {SITE_POSTS}")

if __name__ == "__main__":
    main()
