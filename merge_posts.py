import json
import subprocess
from datetime import datetime, timezone
from difflib import SequenceMatcher

def get_vk_data():
    try:
        # Trying to get VK data from git as previously done in compare_vk_tg.py
        out = subprocess.check_output(['git', 'show', 'HEAD~1:magicdpd_readable_dump.json'])
        return json.loads(out)
    except:
        # Fallback if git is not available or file is missing in history
        print("Warning: Could not get VK data from git history, using default method if applicable")
        return []

def get_tg_data():
    with open('magicdpd_readable_dump.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def clean_text(text, title=None):
    if not text:
        text = ""
    if title:
        text = f"{title}\n{text}"
    return text.strip().lower()

print("Loading data...")
vk_posts = get_vk_data()
tg_posts_raw = get_tg_data()
tg_posts = [p for p in tg_posts_raw if p.get('date')]

tg_parsed = []
for p in tg_posts:
    try:
        dt = datetime.fromisoformat(p['date'])
        tg_parsed.append({'post': p, 'dt': dt})
    except:
        pass
tg_parsed.sort(key=lambda x: x['dt'])

paired_tg_ids = set()
WINDOW_HOURS = 6
WINDOW_SECONDS = WINDOW_HOURS * 3600

print(f"Identifying duplicates between VK and TG (within {WINDOW_HOURS} hours)...")

# First, find all matching TG posts for VK posts
for vk in vk_posts:
    try:
        vk_dt = datetime.strptime(vk['date'], '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
        
        matches_tg = []
        for tg in tg_parsed:
            diff = abs((tg['dt'] - vk_dt).total_seconds())
            if diff <= WINDOW_SECONDS:
                tg_id = tg['post'].get('id', tg['post'].get('grouped_id', 'unknown'))
                if tg_id not in paired_tg_ids:
                    matches_tg.append((tg['post'], diff, tg_id))
        
        if matches_tg:
            matches_tg.sort(key=lambda x: x[1])
            best_tg_id = matches_tg[0][2]
            # We don't necessarily need text similarity for just marking them as "paired" 
            # if we trust the time window, but let's keep it consistent.
            paired_tg_ids.add(best_tg_id)
            
    except Exception as e:
        pass

print(f"Creating unified list...")
unified_list = []

# 1. Add all VK posts with source tag
for vk in vk_posts:
    post_copy = vk.copy()
    post_copy['source'] = 'vk'
    unified_list.append(post_copy)

# 2. Add only non-paired TG posts
tg_added = 0
for tg in tg_posts:
    tg_id = tg.get('id', tg.get('grouped_id', 'unknown'))
    if tg_id not in paired_tg_ids:
        post_copy = tg.copy()
        post_copy['source'] = 'tg'
        unified_list.append(post_copy)
        tg_added += 1

# Sort unified list by date
def get_sort_date(post):
    date_str = post.get('date')
    if not date_str:
        return datetime.min.replace(tzinfo=timezone.utc)
    try:
        if post['source'] == 'vk':
            return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
        else:
            return datetime.fromisoformat(date_str)
    except:
        return datetime.min.replace(tzinfo=timezone.utc)

unified_list.sort(key=get_sort_date)

output_file = 'unified_posts.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(unified_list, f, ensure_ascii=False, indent=2)

print(f"Success!")
print(f"Total VK posts added: {len(vk_posts)}")
print(f"Total TG posts (non-duplicates) added: {tg_added}")
print(f"Grand total in {output_file}: {len(unified_list)}")
