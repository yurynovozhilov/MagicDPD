import json
import re
import shutil

with open('vk/ifttt_url_mapping.json') as f:
    mapping = json.load(f)

mapping = {int(k): v for k, v in mapping.items()}

def fix_text(text, real_url):
    if not text:
        return text
    # Replace ift.tt URL before Media/emoji marker (article link)
    # Handles: http://ift.tt/XXXXMedia📼, http://ift.tt/XXXX🔗, http://ift.tt/XXXXMedia🔗
    text = re.sub(r'https?://ift\.tt/\w+(?:Media)?(?=[📼🔗])', real_url + ' ', text)
    # Remove "via MagicDPD http://ift.tt/..." at end
    text = re.sub(r'\n+via MagicDPD https?://ift\.tt/\S+\s*$', '', text)
    # Remove trailing lone ift.tt URL at very end (source link)
    text = re.sub(r'\n+https?://ift\.tt/\S+\s*$', '', text)
    return text.strip()

def fix_links(links, real_url):
    if not links:
        return links
    # Remove ift.tt entries, add real_url if not already present
    cleaned = [l for l in links if 'ift.tt' not in l and not l.startswith('ttp://')]
    if real_url not in cleaned:
        cleaned.append(real_url)
    return cleaned

def apply_to_dump(path):
    with open(path) as f:
        posts = json.load(f)

    fixed = 0
    for post in posts:
        pid = post.get('id')
        if pid not in mapping:
            continue
        real_url = mapping[pid]['real_url']
        original_text = post.get('text', '')
        original_links = post.get('links', [])

        post['text'] = fix_text(original_text, real_url)
        post['links'] = fix_links(original_links, real_url)
        fixed += 1

    shutil.copy(path, path + '.bak_ifttt')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    print(f'{path}: fixed {fixed} posts (backup saved as {path}.bak_ifttt)')

apply_to_dump('magicdpd_readable_dump.json')
apply_to_dump('unified_posts.json')
