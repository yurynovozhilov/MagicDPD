import json
import subprocess
import re
from datetime import datetime, timezone
from difflib import SequenceMatcher

def get_vk_data():
    out = subprocess.check_output(['git', 'show', 'HEAD~1:magicdpd_readable_dump.json'])
    return json.loads(out)

def get_tg_data():
    with open('magicdpd_readable_dump.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def clean_text(text, title=None):
    if not text:
        text = ""
    if title:
        text = f"{title}\n{text}"
    # simple cleaning
    return text.strip().lower()

print("Loading data...")
vk_posts = get_vk_data()
tg_posts = [p for p in get_tg_data() if p.get('date')]

tg_parsed = []
for p in tg_posts:
    try:
        dt = datetime.fromisoformat(p['date'])
        tg_parsed.append({'post': p, 'dt': dt})
    except:
        pass
tg_parsed.sort(key=lambda x: x['dt'])

pairs = []
unmatched_vk = []
paired_tg_ids = set()

WINDOW_HOURS = 6
WINDOW_SECONDS = WINDOW_HOURS * 3600

print(f"Matching VK and TG (within {WINDOW_HOURS} hours)...")

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
            vk_text = clean_text(vk.get('text', ''))
            
            matches_tg.sort(key=lambda x: x[1])
            best_tg_match = matches_tg[0][0]
            diff_hours_tg = matches_tg[0][1] / 3600
            best_tg_id = matches_tg[0][2]
            tg_text = clean_text(best_tg_match.get('text', ''), best_tg_match.get('title'))
            sim_tg = SequenceMatcher(None, vk_text, tg_text).ratio() if (vk_text or tg_text) else 1.0
            paired_tg_ids.add(best_tg_id)
            
            pairs.append({
                'vk_id': vk['id'],
                'vk_date': vk['date'],
                'tg_id': best_tg_id,
                'tg_title': best_tg_match.get('title'),
                'tg_date': best_tg_match['date'],
                'tg_diff_hours': diff_hours_tg,
                'tg_similarity': sim_tg
            })
        else:
            unmatched_vk.append(vk)
            
    except Exception as e:
        print("error parsing vk date:", vk.get('date'), e)

print(f"Total VK posts: {len(vk_posts)}")
print(f"Total TG posts: {len(tg_posts)}")
print(f"Found {len(pairs)} UNIQUE pairs of VK+TG posts.")

# Text Similarity Stats
sims = [p['tg_similarity'] for p in pairs if p['tg_similarity'] is not None]

if sims:
    exact_matches = sum(1 for s in sims if s >= 0.99)
    high_matches = sum(1 for s in sims if 0.8 <= s < 0.99)
    medium_matches = sum(1 for s in sims if 0.4 <= s < 0.8)
    low_matches = sum(1 for s in sims if s < 0.4)

    print("\n--- Text Similarity Stats (Ratio) ---")
    print(f"Exact match (>99%): {exact_matches}")
    print(f"High similarity (80-99%): {high_matches}")
    print(f"Medium similarity (40-80%): {medium_matches}")
    print(f"Low similarity/Different text (<40%): {low_matches}")

    average_sim = sum(sims) / len(sims)
    print(f"\nAverage similarity across all {len(pairs)} pairs: {average_sim*100:.1f}%")
