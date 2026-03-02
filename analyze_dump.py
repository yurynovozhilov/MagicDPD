import json
from datetime import datetime

with open('magicdpd_readable_dump.json', 'r', encoding='utf-8') as f:
    messages = json.load(f)

# Sort messages chronologically
messages.sort(key=lambda x: x.get('date') or '')

valid_messages = []
for msg in messages:
    if not msg.get('date'): continue
    valid_messages.append(msg)

def is_only_photo(msg):
    # Check if text is empty and there's a photo in media
    text = msg.get('text', '').strip()
    if text:
        return False
    media = msg.get('media', [])
    for m in media:
        if m.get('type') == 'photo':
            return True
    return False

# Group by grouped_id to merge albums
albums = []
for msg in valid_messages:
    gid = msg.get('grouped_id')
    if gid:
        if albums and albums[-1]['gid'] == gid:
            albums[-1]['msgs'].append(msg)
            continue
    albums.append({'gid': gid, 'msgs': [msg]})

print(f"Total posts/albums: {len(albums)}")

found = []
for i in range(len(albums) - 1):
    cur_album = albums[i]
    next_album = albums[i+1]
    
    cur_msgs = cur_album['msgs']
    next_msgs = next_album['msgs']
    
    t1 = datetime.fromisoformat(cur_msgs[0]['date'])
    t2 = datetime.fromisoformat(next_msgs[0]['date'])
    
    diff = (t2 - t1).total_seconds()
    
    if 0 < diff < 600: # strictly greater than 0, to avoid same exact time if any? actually diff >= 0
        # Check if one of them is only photo
        
        # Consider an album "only photo" if all its messages are only photo
        cur_only_photo = all(is_only_photo(m) for m in cur_msgs)
        next_only_photo = all(is_only_photo(m) for m in next_msgs)
        
        if cur_only_photo or next_only_photo:
            found.append({
                'time_diff_sec': diff,
                'time_diff_min': diff / 60,
                'post1_date': cur_msgs[0]['date'],
                'post1_id': cur_msgs[0]['id'],
                'post1_only_photo': cur_only_photo,
                'post2_date': next_msgs[0]['date'],
                'post2_id': next_msgs[0]['id'],
                'post2_only_photo': next_only_photo,
            })

print(f"Found {len(found)} pairs of posts with < 10min gap where one is only photo.")
for f in found[:20]:
    print(f"Gap: {f['time_diff_min']:.1f} min | Post1: ID {f['post1_id']}, Date: {f['post1_date']}, Only Photo: {f['post1_only_photo']} | Post2: ID {f['post2_id']}, Date: {f['post2_date']}, Only Photo: {f['post2_only_photo']}")

if len(found) > 20:
    print(f"... and {len(found) - 20} more.")
