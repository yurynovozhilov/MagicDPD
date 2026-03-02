#!/usr/bin/env python3
"""Generate Hugo posts from a Telegram channel dump.

Reads:
  magicdpd_readable_dump.json  — text, media metadata, dates
  magicdpd_raw_dump.json       — full Telethon to_dict() with formatting entities

Groups messages posted within 1 hour into a single Hugo post.
The first bold entity at offset 0 (if any) in the first message becomes the title;
otherwise the first line of text is used.
"""
import json
import re
import shutil
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
READABLE_DUMP = ROOT / "magicdpd_readable_dump.json"
RAW_DUMP = ROOT / "magicdpd_raw_dump.json"
MEDIA_DIR = ROOT / "magicdpd_media"
SITE_POSTS = ROOT / "site" / "content" / "posts"
SITE_IMAGES = ROOT / "site" / "static" / "assets" / "images"
TG_CHANNEL = "MagicDPD"
MERGE_WINDOW = 3600  # seconds (1 hour)

# ---------------------------------------------------------------------------
# Transliteration (same mapping as generate_site_from_unified.py)
# ---------------------------------------------------------------------------

RUS_TO_LAT = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e", "ж": "zh",
    "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o",
    "п": "p", "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f", "х": "h", "ц": "ts",
    "ч": "ch", "ш": "sh", "щ": "sch", "ъ": "", "ы": "y", "ь": "", "э": "e",
    "ю": "yu", "я": "ya",
}


def transliterate(text: str) -> str:
    text = re.sub(r'[!@#$%^&*()\[\]{};:\'\",.<>?/\\|`~]', '', text or "")
    text = text.replace(" ", "-")
    buf: list[str] = []
    for ch in text.lower():
        if ch in RUS_TO_LAT:
            buf.append(RUS_TO_LAT[ch])
        elif ch.isalnum():
            buf.append(ch)
        elif ch in {"-", "_"}:
            buf.append("-")
        else:
            norm = unicodedata.normalize("NFKD", ch).encode("ascii", "ignore").decode()
            buf.append(norm if norm else "-")
    return re.sub(r"-+", "-", "".join(buf)).strip("-")


# ---------------------------------------------------------------------------
# Title extraction
# ---------------------------------------------------------------------------

def extract_title_from_raw(raw_msg: dict, readable_text: str) -> str | None:
    """Return text of the first MessageEntityBold at offset 0, or None."""
    entities = raw_msg.get("entities") or []
    for ent in entities:
        if ent.get("_") == "MessageEntityBold" and ent.get("offset") == 0:
            length = ent.get("length", 0)
            if length > 0:
                return readable_text[:length].strip()
    return None


def derive_title(group: list[dict], raw_by_id: dict) -> tuple[str, bool]:
    """Return (title, title_is_first_line).

    title_is_first_line=True means the title was the first line of text and
    should be stripped from the body to avoid duplication.
    """
    first = group[0]
    msg_id = first.get("id")
    text = (first.get("text") or "").strip()

    # Try bold entity from raw dump
    raw = raw_by_id.get(msg_id, {})
    bold_title = extract_title_from_raw(raw, text)
    if bold_title:
        return bold_title, False  # entity-based title, keep full text in body

    # Fall back to first non-empty line across the whole group
    for msg in group:
        for line in (msg.get("text") or "").splitlines():
            line = line.strip()
            if line:
                return line[:80], True  # first line → strip from body

    # Last resort
    return f"Post {msg_id}", False


# ---------------------------------------------------------------------------
# Image handling
# ---------------------------------------------------------------------------

IMAGE_EXTS = ["jpg", "jpeg", "png", "gif", "webp"]


def find_media_file(msg_id: int) -> Path | None:
    for ext in IMAGE_EXTS:
        p = MEDIA_DIR / f"{msg_id}.{ext}"
        if p.exists():
            return p
    return None


def collect_images(group: list[dict]) -> list[str]:
    """Copy images to site/static and return list of /assets/images/… URLs."""
    urls: list[str] = []
    seen: set[str] = set()
    for msg in group:
        msg_id = msg.get("id")
        # Check media list for photos
        has_photo = any(m.get("type") == "photo" for m in (msg.get("media") or []))
        if not has_photo:
            # Also try even if media list is empty — file might still be on disk
            pass
        src = find_media_file(msg_id)
        if src and src.name not in seen:
            seen.add(src.name)
            dest = SITE_IMAGES / src.name
            if not dest.exists():
                shutil.copy2(src, dest)
            urls.append(f"/assets/images/{src.name}")
    return urls


# ---------------------------------------------------------------------------
# Post grouping
# ---------------------------------------------------------------------------

def parse_date(s: str) -> datetime:
    # Telethon dates are UTC with +00:00; fromisoformat handles both
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def group_messages(messages: list[dict]) -> list[list[dict]]:
    """Group consecutive messages with ≤ MERGE_WINDOW seconds between them."""
    valid = [m for m in messages if m.get("date")]
    valid.sort(key=lambda m: m["date"])

    groups: list[list[dict]] = []
    current: list[dict] = []
    for msg in valid:
        if not current:
            current = [msg]
            continue
        t_prev = parse_date(current[-1]["date"])
        t_cur = parse_date(msg["date"])
        gap = (t_cur - t_prev).total_seconds()
        if gap <= MERGE_WINDOW:
            current.append(msg)
        else:
            groups.append(current)
            current = [msg]
    if current:
        groups.append(current)
    return groups


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------

def build_body(group: list[dict], skip_first_line: bool) -> str:
    """Combine texts; if skip_first_line, drop the first non-empty line."""
    parts: list[str] = []
    first_line_skipped = False
    for msg in group:
        text = (msg.get("text") or "").strip()
        if not text:
            continue
        if skip_first_line and not first_line_skipped:
            lines = text.splitlines()
            # Remove first non-empty line (the title)
            trimmed = []
            skipped = False
            for line in lines:
                if not skipped and line.strip():
                    skipped = True
                    first_line_skipped = True
                    continue
                trimmed.append(line)
            text = "\n".join(trimmed).strip()
            if not text:
                continue
        parts.append(text)
    return "\n\n".join(parts)


def yaml_str(s: str) -> str:
    """Escape a string for YAML front matter."""
    s = s.replace('\\', '\\\\')  # backslash must be first
    s = s.replace('"', '\\"')
    return f'"{s}"'


def render_post(group: list[dict], raw_by_id: dict) -> str:
    first = group[0]
    date_str = first["date"]
    date = parse_date(date_str)
    first_id = first.get("id", 0)

    title, title_is_first_line = derive_title(group, raw_by_id)
    body = build_body(group, skip_first_line=title_is_first_line)
    images = collect_images(group)

    # Front matter
    fm_lines = [
        "---",
        f"title: {yaml_str(title)}",
        f"date: {date.isoformat()}",
        "source: tg",
        f"original_url: \"https://t.me/{TG_CHANNEL}/{first_id}\"",
    ]
    if images:
        fm_lines.append("images:")
        for url in images:
            fm_lines.append(f'  - url: "{url}"')
    fm_lines.append("---")

    parts = ["\n".join(fm_lines)]
    if body:
        parts.append(body)
    return "\n\n".join(parts) + "\n"


def make_filename(group: list[dict], title: str) -> str:
    first = group[0]
    date = parse_date(first["date"])
    date_prefix = date.strftime("%Y-%m-%d")
    slug = transliterate(title)[:50].strip("-") or f"post-{first.get('id', 0)}"
    return f"{date_prefix}-{slug}.md"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    if not READABLE_DUMP.exists():
        raise FileNotFoundError(f"Not found: {READABLE_DUMP}\nRun dump_telegram.py first.")

    print(f"Loading {READABLE_DUMP.name} …")
    readable: list[dict] = json.loads(READABLE_DUMP.read_text(encoding="utf-8"))
    print(f"  {len(readable):,} messages loaded.")

    raw_by_id: dict[int, dict] = {}
    if RAW_DUMP.exists():
        print(f"Loading {RAW_DUMP.name} for entity info …")
        raw_list: list[dict] = json.loads(RAW_DUMP.read_text(encoding="utf-8"))
        raw_by_id = {m["id"]: m for m in raw_list if isinstance(m, dict) and "id" in m}
        print(f"  {len(raw_by_id):,} raw messages indexed.")
    else:
        print(f"[!] {RAW_DUMP.name} not found — bold title detection disabled.")

    # Prepare output directories
    SITE_POSTS.mkdir(parents=True, exist_ok=True)
    SITE_IMAGES.mkdir(parents=True, exist_ok=True)

    groups = group_messages(readable)
    print(f"Grouped {len(readable):,} messages into {len(groups):,} posts "
          f"(merge window: {MERGE_WINDOW // 60} min).")

    posts_written = 0
    images_copied = 0
    img_count_before = sum(1 for _ in SITE_IMAGES.iterdir())

    for group in groups:
        title, title_is_first_line = derive_title(group, raw_by_id)
        filename = make_filename(group, title)
        dest = SITE_POSTS / filename

        content = render_post(group, raw_by_id)
        dest.write_text(content, encoding="utf-8")
        posts_written += 1

    img_count_after = sum(1 for _ in SITE_IMAGES.iterdir())
    images_copied = img_count_after - img_count_before

    print(f"\nDone!")
    print(f"  Posts written : {posts_written:,}  →  {SITE_POSTS}")
    print(f"  Images copied : {images_copied:,}  →  {SITE_IMAGES}")


if __name__ == "__main__":
    main()
