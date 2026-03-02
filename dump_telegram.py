"""
dump_telegram.py — full archive dump for a Telegram channel.

Authorization
-------------
Uses QR-code login (no phone/SMS needed).
On first run: scan the QR code with the Telegram mobile app
  Settings → Devices → Link Desktop Device
The session is saved locally — subsequent runs skip auth entirely.

Features
--------
* Fetches ALL messages by default (TELEGRAM_LIMIT empty = unlimited).
* Resume support: continues from the last saved message ID.
* Incremental saves every SAVE_EVERY messages — progress never lost.
* Automatic FloodWaitError back-off.
* Progress: messages/sec, elapsed, ETA.

.env variables
--------------
TELEGRAM_API_ID    = <from my.telegram.org>
TELEGRAM_API_HASH  = <from my.telegram.org>
TELEGRAM_CHANNEL   = @MagicDPD
TELEGRAM_SESSION   = magicdpd_session
# TELEGRAM_LIMIT   =   # leave empty = full archive
"""

import asyncio
import base64
import json
import os
import sys
import time
from dataclasses import asdict, is_dataclass
from datetime import datetime
from getpass import getpass
from pathlib import Path
from typing import Any, Dict, List, Optional

import qrcode
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import FloodWaitError, SessionPasswordNeededError
from telethon.tl.types import (
    DocumentAttributeFilename,
    MessageEntityTextUrl,
    MessageEntityUrl,
)


load_dotenv()

SAVE_EVERY = 500  # flush to disk every N new messages


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _require_env(key: str) -> str:
    value = os.getenv(key, '').strip()
    if not value:
        raise RuntimeError(f"Environment variable '{key}' is required but not set in .env")
    return value


def _slugify_channel(name: str) -> str:
    clean = name.strip().lstrip('@') or "channel"
    slug = ''.join(ch.lower() if ch.isalnum() else '_' for ch in clean)
    return slug.strip('_') or "channel"


def _json_safe(value: Any) -> Any:
    if isinstance(value, bytes):
        return base64.b64encode(value).decode('ascii')
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_json_safe(v) for v in value]
    if is_dataclass(value):
        return _json_safe(asdict(value))
    to_dict = getattr(value, 'to_dict', None)
    if callable(to_dict):
        return _json_safe(to_dict())
    return value


def _extract_links(message) -> List[str]:
    links: List[str] = []
    text = message.message or ''
    for entity in (message.entities or []):
        if isinstance(entity, MessageEntityTextUrl):
            links.append(entity.url)
        elif isinstance(entity, MessageEntityUrl):
            links.append(text[entity.offset: entity.offset + entity.length])
    return links


def _describe_media(message) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []

    photo = getattr(message, 'photo', None)
    if photo:
        sizes = [
            {'type': getattr(s, 'type', None),
             'width': getattr(s, 'w', None),
             'height': getattr(s, 'h', None)}
            for s in (getattr(photo, 'sizes', []) or [])
        ]
        out.append({'type': 'photo', 'id': getattr(photo, 'id', None), 'sizes': sizes})

    document = getattr(message, 'document', None)
    if document:
        file_name = next(
            (a.file_name for a in (getattr(document, 'attributes', []) or [])
             if isinstance(a, DocumentAttributeFilename)),
            None,
        )
        out.append({
            'type': 'document',
            'size': getattr(document, 'size', None),
            'mime_type': getattr(document, 'mime_type', None),
            'file_name': file_name,
        })

    webpage = getattr(getattr(message, 'media', None), 'webpage', None)
    if webpage:
        out.append({
            'type': 'webpage',
            'site_name': getattr(webpage, 'site_name', None),
            'title': getattr(webpage, 'title', None),
            'description': getattr(webpage, 'description', None),
            'url': getattr(webpage, 'url', None),
        })

    poll_media = getattr(message, 'poll', None)
    if poll_media:
        poll = getattr(poll_media, 'poll', poll_media)  # MessageMediaPoll wraps a Poll object
        out.append({
            'type': 'poll',
            'question': getattr(poll, 'question', None),
            'multiple_choice': getattr(poll, 'multiple_choice', None),
            'closed': getattr(poll, 'closed', None),
            'answers': [getattr(a, 'text', str(a)) for a in (getattr(poll, 'answers', []) or [])],
        })

    return out


def _describe_forward(message) -> Optional[Dict[str, Any]]:
    fwd = getattr(message, 'fwd_from', None)
    if not fwd:
        return None
    result: Dict[str, Any] = {
        'from_name': getattr(fwd, 'from_name', None),
        'post_author': getattr(fwd, 'post_author', None),
        'channel_post': getattr(fwd, 'channel_post', None),
        'channel_id': getattr(fwd, 'channel_id', None),
        'date': fwd.date.isoformat() if getattr(fwd, 'date', None) else None,
    }
    from_id = getattr(fwd, 'from_id', None)
    if from_id:
        result['from_id'] = _json_safe(from_id)
    return result


def _format_message(message) -> Dict[str, Any]:
    replies = getattr(message, 'replies', None)
    reply_info = None
    if replies:
        reply_info = {
            'replies': getattr(replies, 'replies', None),
            'forum_topic': getattr(replies, 'forum_topic', None),
            'recent_repliers': [
                _json_safe(p) for p in (getattr(replies, 'recent_repliers', []) or [])
            ],
        }
    return {
        'id': message.id,
        'date': message.date.isoformat() if message.date else None,
        'text': message.message or '',
        'views': message.views,
        'forwards': message.forwards,
        'replies': reply_info,
        'reply_to': getattr(getattr(message, 'reply_to', None), 'reply_to_msg_id', None),
        'post_author': message.post_author,
        'via_bot': getattr(getattr(message, 'via_bot', None), 'username', None),
        'pinned': message.pinned,
        'grouped_id': message.grouped_id,
        'links': _extract_links(message),
        'media': _describe_media(message),
        'forwarded_from': _describe_forward(message),
    }


# ---------------------------------------------------------------------------
# Progress
# ---------------------------------------------------------------------------

def _fmt_duration(seconds: float) -> str:
    s = int(seconds)
    h, rem = divmod(s, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}h {m}m {s}s"
    if m:
        return f"{m}m {s}s"
    return f"{s}s"


def _print_progress(count: int, total: Optional[int], start_time: float) -> None:
    elapsed = time.monotonic() - start_time
    rate = count / elapsed if elapsed > 0 else 0
    if total:
        pct = count / total * 100
        eta = (total - count) / rate if rate > 0 else 0
        line = (f"\r[+] {count:,}/{total:,} ({pct:.1f}%)  "
                f"{rate:.0f} msg/s  elapsed {_fmt_duration(elapsed)}  "
                f"ETA {_fmt_duration(eta)}   ")
    else:
        line = (f"\r[+] {count:,} messages  {rate:.0f} msg/s  "
                f"elapsed {_fmt_duration(elapsed)}   ")
    print(line, end='', flush=True)


# ---------------------------------------------------------------------------
# Incremental save
# ---------------------------------------------------------------------------

def _load_existing(path: Path) -> list:
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding='utf-8'))
            if isinstance(data, list):
                return data
        except Exception as exc:
            print(f"\n[!] Could not read {path}: {exc}. Starting fresh.")
    return []


def _save(path: Path, data: list) -> None:
    """Atomic write via temp file."""
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    tmp.replace(path)


# ---------------------------------------------------------------------------
# QR-code authorization
# ---------------------------------------------------------------------------

def _print_qr(url: str) -> None:
    """Print QR code as ASCII art to stdout."""
    qr = qrcode.QRCode()
    qr.add_data(url)
    qr.make(fit=True)
    # Use invert so dark modules = filled blocks on light terminal bg
    qr.print_ascii(invert=True)


async def _ensure_authorized(client: TelegramClient) -> None:
    if await client.is_user_authorized():
        return

    print("\n[*] Not authorized. Starting QR-code login...")
    print("[*] Open Telegram on your phone:")
    print("    Settings → Devices → Link Desktop Device\n")

    # Telethon's QR login loop — the token refreshes every ~30 s
    while True:
        try:
            qr_login = await client.qr_login()
            _print_qr(qr_login.url)
            print(f"\n[*] Scan the QR code above (expires in ~30 s)...")

            try:
                await qr_login.wait(30)
                break  # scan successful
            except asyncio.TimeoutError:
                print("\n[!] QR code expired, refreshing...")
                # loop continues → new qr_login object with fresh token

        except SessionPasswordNeededError:
            # 2FA enabled
            password = os.getenv('TELEGRAM_PASSWORD') or getpass('\n[*] Enter 2FA password: ')
            await client.sign_in(password=password)
            break

    me = await client.get_me()
    print(f"\n[✓] Logged in as: {me.first_name} (@{me.username})")


# ---------------------------------------------------------------------------
# Main dump
# ---------------------------------------------------------------------------

async def dump_channel() -> None:
    api_id       = int(_require_env('TELEGRAM_API_ID'))
    api_hash     = _require_env('TELEGRAM_API_HASH')
    channel      = os.getenv('TELEGRAM_CHANNEL', '@MagicDPD').strip()
    session_name = os.getenv('TELEGRAM_SESSION', 'magicdpd_session').strip()
    download_media = os.getenv('TELEGRAM_DOWNLOAD_MEDIA', '').strip().lower() in ('1', 'true', 'yes')

    limit_str = os.getenv('TELEGRAM_LIMIT', '').strip()
    limit_value: Optional[int] = None
    if limit_str and limit_str != '0':
        limit_value = int(limit_str)

    client = TelegramClient(session_name, api_id, api_hash)
    await client.connect()
    await _ensure_authorized(client)

    entity = await client.get_entity(channel)
    slug = _slugify_channel(channel)
    raw_output      = Path(f'{slug}_raw_dump.json')
    readable_output = Path(f'{slug}_readable_dump.json')

    # --- Resume support ---
    raw_messages: list      = _load_existing(raw_output)
    readable_messages: list = _load_existing(readable_output)

    if len(raw_messages) != len(readable_messages):
        min_len = min(len(raw_messages), len(readable_messages))
        print(f"[!] File length mismatch — keeping {min_len} entries from both.")
        raw_messages      = raw_messages[:min_len]
        readable_messages = readable_messages[:min_len]

    # Build a set of already-saved IDs for deduplication
    saved_ids: set = {m['id'] for m in raw_messages if isinstance(m, dict) and 'id' in m}
    already_fetched = len(raw_messages)
    max_id = 0  # 0 = no upper bound (start from newest)

    if already_fetched:
        max_existing_id = max(saved_ids, default=0)
        # NOTE: we fetch newest→oldest, so resume means fetching messages
        # OLDER than our oldest already-saved message.
        min_existing_id = min(saved_ids, default=0)
        max_id = min_existing_id  # offset_id: fetch messages with id < min_existing_id
        print(
            f"[*] Resuming: {already_fetched:,} saved "
            f"(IDs {min_existing_id}–{max_existing_id}); "
            f"fetching older messages (id < {min_existing_id})."
        )
    else:
        print(f"[*] Starting fresh dump of {channel}.")

    # Try to get total for ETA
    total: Optional[int] = None
    try:
        result = await client.get_messages(entity, limit=1)
        total_in_channel = result.total
        if total_in_channel:
            print(f"[*] Channel has ~{total_in_channel:,} messages total.")
            remaining = total_in_channel - already_fetched
            total = min(limit_value, remaining) if limit_value else remaining
            if already_fetched:
                print(f"[*] ~{remaining:,} left to fetch.")
    except Exception as exc:
        print(f"[~] Could not determine total: {exc}")

    start_time = time.monotonic()
    new_count  = 0
    limit_label = 'unlimited' if not limit_value else str(limit_value)
    print(f"[*] Fetching messages newest→oldest (limit={limit_label})...")

    try:
        # Fetch newest→oldest (default Telethon direction).
        # reverse=True has a bug with non-contiguous IDs — avoid it.
        # max_id=0 means start from newest; max_id=N means start from before ID N.
        async for message in client.iter_messages(
            entity,
            limit=limit_value,   # None = all messages (works correctly newest-first)
            max_id=max_id if max_id else 0,
        ):
            # Skip if already stored (safety dedup)
            if message.id in saved_ids:
                continue
            saved_ids.add(message.id)
            new_count += 1
            raw_messages.append(_json_safe(message.to_dict()))
            readable_messages.append(_format_message(message))

            if new_count % 10 == 0:
                progress_total = (already_fetched + total) if total else None
                _print_progress(already_fetched + new_count, progress_total, start_time)

            if new_count % SAVE_EVERY == 0:
                print(f"\n[*] Checkpoint: {already_fetched + new_count:,} messages saved...")
                # Sort by ID ascending before saving checkpoint
                raw_messages.sort(key=lambda m: m.get('id', 0) if isinstance(m, dict) else 0)
                readable_messages.sort(key=lambda m: m.get('id', 0) if isinstance(m, dict) else 0)
                _save(raw_output, raw_messages)
                _save(readable_output, readable_messages)

    except FloodWaitError as e:
        print(f"\n[!] FloodWait: sleeping {e.seconds}s — then restart the script.")
        raw_messages.sort(key=lambda m: m.get('id', 0) if isinstance(m, dict) else 0)
        readable_messages.sort(key=lambda m: m.get('id', 0) if isinstance(m, dict) else 0)
        _save(raw_output, raw_messages)
        _save(readable_output, readable_messages)
        await asyncio.sleep(e.seconds + 1)
        raise
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user. Saving progress...")

    # Sort by ID ascending before final save
    raw_messages.sort(key=lambda m: m.get('id', 0) if isinstance(m, dict) else 0)
    readable_messages.sort(key=lambda m: m.get('id', 0) if isinstance(m, dict) else 0)

    print(f"\n[*] Saving final output ({already_fetched + new_count:,} total)...")
    _save(raw_output, raw_messages)
    _save(readable_output, readable_messages)

    elapsed = time.monotonic() - start_time
    print(f"[✓] Done! {new_count:,} new messages fetched in {_fmt_duration(elapsed)}.")
    print(f"[✓] Total stored: {len(raw_messages):,} messages.")
    print(f"[✓] Raw data  → {raw_output}")
    print(f"[✓] Readable  → {readable_output}")

    # ---------------------------------------------------------------------------
    # Phase 2: Media download
    # ---------------------------------------------------------------------------
    if download_media:
        media_dir = Path(f'{slug}_media')
        media_dir.mkdir(exist_ok=True)
        print(f"\n[*] Syncing media to {media_dir}/ ...")

        missing_ids = []
        for msg in raw_messages:
            msg_id = msg.get('id')
            media_info = msg.get('media')
            if not msg_id or not media_info or not isinstance(media_info, dict):
                continue
            
            # Telethon serializes the class name into the '_' key
            if media_info.get('_') in ('MessageMediaPhoto', 'MessageMediaDocument'):
                # Check if file with this ID prefix already exists (Telethon auto-appends extension)
                if not any(media_dir.glob(f"{msg_id}.*")):
                    missing_ids.append(msg_id)

        if not missing_ids:
            print("[✓] All media files are already downloaded.")
        else:
            print(f"[*] Found {len(missing_ids):,} missing media files. Fetching...")
            chunk_size = 200
            downloaded = 0
            for i in range(0, len(missing_ids), chunk_size):
                chunk = missing_ids[i : i + chunk_size]
                try:
                    msgs = await client.get_messages(entity, ids=chunk)
                    for m in msgs:
                        # get_messages may return None for deleted/missing messages
                        if m and getattr(m, 'media', None):
                            print(f"\r[+] Downloading media for message ID {m.id}...   ", end='', flush=True)
                            await client.download_media(m, file=str(media_dir / str(m.id)))
                            downloaded += 1
                except FloodWaitError as e:
                    print(f"\n[!] FloodWait: sleeping {e.seconds}s during media sync...")
                    await asyncio.sleep(e.seconds + 1)
                except Exception as e:
                    print(f"\n[!] Error fetching media chunk: {e}")
            
            print(f"\n[✓] Finished syncing media. {downloaded} new files downloaded.")

    await client.disconnect()


if __name__ == '__main__':
    asyncio.run(dump_channel())
