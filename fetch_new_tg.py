#!/usr/bin/env python3
"""Fetch only NEW Telegram messages (newer than the last saved ID) and append them to the dump.

Usage:
    python fetch_new_tg.py

Reads:  magicdpd_readable_dump.json, magicdpd_raw_dump.json
Writes: same files (appends new messages, sorts by ID ascending)
"""

import asyncio
import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import FloodWaitError

load_dotenv()

ROOT = Path(__file__).resolve().parent
READABLE_DUMP = ROOT / "magicdpd_readable_dump.json"
RAW_DUMP      = ROOT / "magicdpd_raw_dump.json"
MEDIA_DIR     = ROOT / "magicdpd_media"


# -- reuse helpers from dump_telegram.py ----------------------------------

import base64
from dataclasses import asdict, is_dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from telethon.tl.types import (
    DocumentAttributeFilename,
    MessageEntityTextUrl,
    MessageEntityUrl,
)


def _require_env(key: str) -> str:
    value = os.getenv(key, '').strip()
    if not value:
        raise RuntimeError(f"Environment variable '{key}' is required but not set in .env")
    return value


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
        poll = getattr(poll_media, 'poll', poll_media)
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


def _load(path: Path) -> list:
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding='utf-8'))
            if isinstance(data, list):
                return data
        except Exception as exc:
            print(f"[!] Could not read {path}: {exc}")
    return []


def _save(path: Path, data: list) -> None:
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    tmp.replace(path)


# -------------------------------------------------------------------------

async def fetch_new() -> None:
    api_id       = int(_require_env('TELEGRAM_API_ID'))
    api_hash     = _require_env('TELEGRAM_API_HASH')
    channel      = os.getenv('TELEGRAM_CHANNEL', '@MagicDPD').strip()
    session_name = os.getenv('TELEGRAM_SESSION', 'magicdpd_session').strip()
    download_media = os.getenv('TELEGRAM_DOWNLOAD_MEDIA', '').strip().lower() in ('1', 'true', 'yes')

    readable_messages: list = _load(READABLE_DUMP)
    raw_messages: list      = _load(RAW_DUMP)

    saved_ids: set = {m['id'] for m in readable_messages if isinstance(m, dict) and 'id' in m}
    max_saved_id = max(saved_ids, default=0)

    print(f"[*] Existing dump: {len(readable_messages):,} messages, max ID = {max_saved_id}")
    print(f"[*] Will fetch messages newer than ID {max_saved_id} from {channel} ...")

    client = TelegramClient(session_name, api_id, api_hash)
    await client.connect()

    if not await client.is_user_authorized():
        import qrcode
        from getpass import getpass
        from telethon.errors import SessionPasswordNeededError
        print("\n[*] Not authorized. Starting QR-code login...")
        print("[*] Open Telegram on your phone:")
        print("    Settings → Devices → Link Desktop Device\n")
        while True:
            try:
                qr_login = await client.qr_login()
                qr = qrcode.QRCode()
                qr.add_data(qr_login.url)
                qr.make(fit=True)
                qr.print_ascii(invert=True)
                print("\n[*] Scan the QR code above (expires in ~30 s)...")
                try:
                    await qr_login.wait(30)
                    break
                except asyncio.TimeoutError:
                    print("\n[!] QR code expired, refreshing...")
            except SessionPasswordNeededError:
                password = os.getenv('TELEGRAM_PASSWORD') or getpass('\n[*] Enter 2FA password: ')
                await client.sign_in(password=password)
                break
        me = await client.get_me()
        print(f"\n[✓] Logged in as: {me.first_name} (@{me.username})")

    entity = await client.get_entity(channel)

    new_raw: list      = []
    new_readable: list = []
    start_time = time.monotonic()

    try:
        async for message in client.iter_messages(entity, min_id=max_saved_id):
            if message.id in saved_ids:
                continue
            saved_ids.add(message.id)
            new_raw.append(_json_safe(message.to_dict()))
            new_readable.append(_format_message(message))

            if len(new_readable) % 50 == 0:
                elapsed = time.monotonic() - start_time
                print(f"\r[+] {len(new_readable):,} new messages  ({elapsed:.0f}s elapsed)   ", end='', flush=True)

    except FloodWaitError as e:
        print(f"\n[!] FloodWait: sleeping {e.seconds}s — restart the script afterwards.")
        await asyncio.sleep(e.seconds + 1)
    except KeyboardInterrupt:
        print("\n[!] Interrupted.")

    print(f"\n[+] Fetched {len(new_readable):,} new messages.")

    if new_readable:
        raw_messages.extend(new_raw)
        readable_messages.extend(new_readable)

        raw_messages.sort(key=lambda m: m.get('id', 0) if isinstance(m, dict) else 0)
        readable_messages.sort(key=lambda m: m.get('id', 0) if isinstance(m, dict) else 0)

        print(f"[*] Saving {len(readable_messages):,} total messages ...")
        _save(RAW_DUMP, raw_messages)
        _save(READABLE_DUMP, readable_messages)
        print(f"[✓] Dumps updated.")
    else:
        print("[✓] Nothing new — dump is up to date.")

    # -- media download for new messages --
    if download_media and new_raw:
        MEDIA_DIR.mkdir(exist_ok=True)
        print(f"\n[*] Downloading media for new messages → {MEDIA_DIR}/")
        missing_ids = []
        for msg in new_raw:
            msg_id = msg.get('id')
            media_info = msg.get('media')
            if not msg_id or not media_info or not isinstance(media_info, dict):
                continue
            if media_info.get('_') in ('MessageMediaPhoto', 'MessageMediaDocument'):
                if not any(MEDIA_DIR.glob(f"{msg_id}.*")):
                    missing_ids.append(msg_id)

        if not missing_ids:
            print("[✓] No media to download.")
        else:
            print(f"[*] {len(missing_ids):,} media files to download ...")
            chunk_size = 50
            downloaded = 0
            for i in range(0, len(missing_ids), chunk_size):
                chunk = missing_ids[i: i + chunk_size]
                try:
                    msgs = await client.get_messages(entity, ids=chunk)
                    for m in msgs:
                        if m and getattr(m, 'media', None):
                            print(f"\r[+] ID {m.id} ...   ", end='', flush=True)
                            await client.download_media(m, file=str(MEDIA_DIR / str(m.id)))
                            downloaded += 1
                except FloodWaitError as e:
                    print(f"\n[!] FloodWait: {e.seconds}s ...")
                    await asyncio.sleep(e.seconds + 1)
                except Exception as exc:
                    print(f"\n[!] Media error: {exc}")
            print(f"\n[✓] Downloaded {downloaded} media files.")

    await client.disconnect()


if __name__ == '__main__':
    asyncio.run(fetch_new())
