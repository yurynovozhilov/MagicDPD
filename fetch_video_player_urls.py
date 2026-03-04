#!/usr/bin/env python3
"""
Fetches the YouTube player URLs for all VK-embedded YouTube videos via
the VK API video.get method (batched, up to 200 per request).

Updates vk/magicdpd_raw_dump.json in-place with the recovered player URLs,
then appends missing YouTube links to Hugo .md files.

Uses only stdlib — no third-party packages needed.
"""
import json
import re
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW_VK = ROOT / "vk" / "magicdpd_raw_dump.json"
SITE_POSTS = ROOT / "site" / "content" / "posts"
CACHE_FILE = ROOT / "video_player_cache.json"
VK_API_VERSION = "5.131"
BATCH_SIZE = 100
RATE_LIMIT_SLEEP = 0.35  # seconds between requests (~3 req/s limit)

URL_RE = re.compile(r"https?://\S+")
FRONT_MATTER_RE = re.compile(r"^---\n.*?\n---\n", re.DOTALL)


# ── helpers ────────────────────────────────────────────────────────────────────

def load_env(path: Path = ROOT / ".env") -> dict[str, str]:
    env: dict[str, str] = {}
    if not path.exists():
        return env
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        env[k.strip()] = v.strip()
    return env


def embed_to_watch(player_url: str) -> str:
    """Convert https://www.youtube.com/embed/ID to watch URL."""
    m = re.search(r"youtube\.com/embed/([\w\-]+)", player_url)
    if m:
        return f"https://www.youtube.com/watch?v={m.group(1)}"
    return player_url


def vk_api_call(method: str, params: dict, token: str) -> dict:
    params = {**params, "access_token": token, "v": VK_API_VERSION}
    url = f"https://api.vk.com/method/{method}?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def extract_body(md_text: str) -> str:
    m = FRONT_MATTER_RE.match(md_text)
    return md_text[m.end():] if m else md_text


def body_has_urls(md_text: str) -> bool:
    return bool(URL_RE.search(extract_body(md_text)))


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def first_body_line(md_text: str) -> str:
    for line in extract_body(md_text).splitlines():
        s = line.strip()
        if s:
            return s
    return ""


def raw_first_line(raw_post: dict) -> str:
    text = raw_post.get("text", "") or ""
    for line in text.splitlines():
        s = line.strip()
        if s:
            return s
    return ""


# ── step 1: fetch player URLs from VK API ─────────────────────────────────────

def fetch_player_urls(raw_posts: list[dict], token: str) -> dict[str, str]:
    """
    Returns mapping: "{owner_id}_{video_id}" → YouTube watch URL.
    Uses CACHE_FILE to avoid re-fetching on subsequent runs.
    """
    # Load existing cache
    cache: dict[str, str] = {}
    if CACHE_FILE.exists():
        cache = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        print(f"  Loaded {len(cache)} entries from cache.")

    # Collect all unique video refs
    video_refs: list[str] = []
    for p in raw_posts:
        for a in p.get("attachments", []):
            if a.get("type") == "video":
                v = a.get("video", {})
                if v.get("platform") == "YouTube":
                    ref = f"{v['owner_id']}_{v['id']}"
                    if ref not in cache:
                        video_refs.append(ref)

    video_refs = list(dict.fromkeys(video_refs))  # deduplicate, preserve order
    print(f"  {len(video_refs)} YouTube videos not yet in cache (need API calls).")

    if not video_refs:
        return cache

    # Batch requests
    batches = [video_refs[i:i + BATCH_SIZE] for i in range(0, len(video_refs), BATCH_SIZE)]
    print(f"  Fetching in {len(batches)} batch(es) of up to {BATCH_SIZE}…")

    for i, batch in enumerate(batches, 1):
        print(f"    Batch {i}/{len(batches)} ({len(batch)} videos)…", end=" ", flush=True)
        try:
            resp = vk_api_call("video.get", {"videos": ",".join(batch)}, token)
            items = resp.get("response", {}).get("items", [])
            found = 0
            for item in items:
                ref = f"{item['owner_id']}_{item['id']}"
                player = item.get("player", "")
                if player:
                    watch_url = embed_to_watch(player)
                    cache[ref] = watch_url
                    found += 1
                else:
                    cache[ref] = ""  # mark as "no URL available" to avoid re-fetching
            print(f"got {found}/{len(items)} player URLs")
        except Exception as e:
            print(f"ERROR: {e}")
        time.sleep(RATE_LIMIT_SLEEP)

    # Save updated cache
    CACHE_FILE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  Cache saved → {CACHE_FILE.name} ({len(cache)} entries)")
    return cache


# ── step 2: update raw dump with player URLs ───────────────────────────────────

def update_raw_dump(raw_posts: list[dict], url_map: dict[str, str]) -> int:
    updated = 0
    for p in raw_posts:
        for a in p.get("attachments", []):
            if a.get("type") == "video":
                v = a.get("video", {})
                if v.get("platform") == "YouTube" and not v.get("player"):
                    ref = f"{v['owner_id']}_{v['id']}"
                    url = url_map.get(ref, "")
                    if url:
                        v["player"] = url
                        updated += 1
    return updated


# ── step 3: update Hugo .md files ──────────────────────────────────────────────

def update_hugo_posts(raw_posts: list[dict]) -> int:
    """Add YouTube links to Hugo posts that have no URLs in body."""
    # Build index: (date_prefix, norm_first_line) → raw post
    raw_index: dict[tuple[str, str], list[dict]] = {}
    for rp in raw_posts:
        dt = datetime.fromtimestamp(rp["date"], tz=timezone.utc)
        date_prefix = dt.date().isoformat()
        fline = normalize(raw_first_line(rp))[:100]
        if not fline:
            continue
        raw_index.setdefault((date_prefix, fline), []).append(rp)

    fixed = 0
    for md_path in sorted(SITE_POSTS.glob("*.md")):
        text = md_path.read_text(encoding="utf-8")
        if "source: vk" not in text:
            continue
        if body_has_urls(text):
            continue

        date_prefix = md_path.name[:10]
        fline = normalize(first_body_line(text))[:100]
        if not fline:
            continue

        candidates = raw_index.get((date_prefix, fline), [])
        if len(candidates) != 1:
            continue

        raw_post = candidates[0]
        urls = []
        for a in raw_post.get("attachments", []):
            if a.get("type") == "video":
                v = a.get("video", {})
                player = v.get("player", "")
                if player:
                    title = v.get("title", "").strip()
                    urls.append(f"[{title}]({player})" if title else player)
            elif a.get("type") == "link":
                url = a.get("link", {}).get("url", "")
                if url:
                    title = a["link"].get("title", "").strip()
                    urls.append(f"[{title}]({url})" if title else url)

        if not urls:
            continue

        new_text = text.rstrip("\n") + "\n\n" + "\n".join(urls) + "\n"
        md_path.write_text(new_text, encoding="utf-8")
        print(f"  FIXED {md_path.name}: {urls[0][:80]}")
        fixed += 1

    return fixed


# ── main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    env = load_env()
    token = env.get("VK_TOKEN", "")
    if not token:
        print("ERROR: VK_TOKEN not found in .env")
        return

    print("Loading raw VK dump…")
    with open(RAW_VK, encoding="utf-8") as f:
        raw_posts: list[dict] = json.load(f)

    print(f"\nStep 1: Fetching YouTube player URLs from VK API…")
    url_map = fetch_player_urls(raw_posts, token)

    non_empty = sum(1 for v in url_map.values() if v)
    print(f"\n  Total with player URL: {non_empty} / {len(url_map)} queried")

    print(f"\nStep 2: Updating raw VK dump with player URLs…")
    updated = update_raw_dump(raw_posts, url_map)
    print(f"  Updated {updated} video attachment(s) in raw dump.")

    RAW_VK.write_text(json.dumps(raw_posts, ensure_ascii=False, indent=4), encoding="utf-8")
    print(f"  Saved → {RAW_VK.name}")

    print(f"\nStep 3: Updating Hugo posts with missing YouTube links…")
    fixed = update_hugo_posts(raw_posts)
    print(f"  Fixed {fixed} Hugo post(s).")

    print("\nDone.")


if __name__ == "__main__":
    main()
