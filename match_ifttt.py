import json
from datetime import date, timedelta

with open('vk/magicdpd_readable_dump.json') as f:
    vk_posts = json.load(f)
with open('magicdpd_readable_dump.json') as f:
    tg_posts = json.load(f)

tg_ifttt = [p for p in tg_posts if 'ift.tt' in (p.get('text') or '')]

vk_by_date = {}
for p in vk_posts:
    vk_by_date.setdefault(p['date'][:10], []).append(p)

def overlap(a, b):
    wa = set((a or '').lower().split())
    wb = set((b or '').lower().split())
    return len(wa & wb) / min(len(wa), len(wb)) if wa and wb else 0

mapping = {}
stats = {'with_url': 0, 'no_url': 0, 'unmatched': 0}

for tg in tg_ifttt:
    d = date.fromisoformat(tg['date'][:10])
    cands = []
    for i in (-1, 0, 1):
        cands += vk_by_date.get(str(d + timedelta(days=i)), [])

    if not cands:
        stats['unmatched'] += 1
        continue

    best = max(cands, key=lambda v: overlap(tg.get('text', ''), v.get('text', '')))
    sc = overlap(tg.get('text', ''), best.get('text', ''))

    if sc < 0.3:
        stats['unmatched'] += 1
        continue

    links = [a['url'] for a in best.get('attachments', []) if a['type'] == 'link']
    if links:
        mapping[tg['id']] = {
            'real_url': links[0],
            'all_urls': links,
            'vk_id': best['id'],
            'score': round(sc, 3),
            'tg_date': tg['date'],
        }
        stats['with_url'] += 1
    else:
        stats['no_url'] += 1

with open('vk/ifttt_url_mapping.json', 'w', encoding='utf-8') as f:
    json.dump(mapping, f, ensure_ascii=False, indent=2)

print(f'TG posts with ift.tt in text : {len(tg_ifttt)}')
print(f'Recovered real URL from VK   : {stats["with_url"]}')
print(f'Matched, VK has no link      : {stats["no_url"]}')
print(f'Unmatched (score < 0.3)      : {stats["unmatched"]}')
print(f'\nMapping saved to vk/ifttt_url_mapping.json')
print()
print('=== All recovered mappings ===')
for tg_id, info in sorted(mapping.items()):
    print(f'TG {tg_id:4d} (score={info["score"]:.2f}) → {info["real_url"]}')
