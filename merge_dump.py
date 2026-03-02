import json
from datetime import datetime
import copy
import os

print("Loading dump...")
with open('magicdpd_readable_dump.json', 'r', encoding='utf-8') as f:
    messages = json.load(f)

valid_messages = [copy.deepcopy(m) for m in messages if m.get('date')]
other_messages = [copy.deepcopy(m) for m in messages if not m.get('date')]

valid_messages.sort(key=lambda x: x.get('date') or '')

def is_only_photo(msg):
    if msg.get('text', '').strip(): return False
    return any(m.get('type') == 'photo' for m in msg.get('media', []))

albums = []
for msg in valid_messages:
    gid = msg.get('grouped_id')
    if gid and albums and albums[-1]['gid'] == gid:
        albums[-1]['msgs'].append(msg)
    else:
        albums.append({'gid': gid, 'msgs': [msg]})

def album_is_only_photo(album):
    return all(is_only_photo(m) for m in album['msgs'])

merged_albums = []
merged_count = 0

i = 0
while i < len(albums):
    cur_album = albums[i]
    
    # Try to gobble up subsequent albums that fit the criteria
    while i + 1 < len(albums):
        next_album = albums[i+1]
        
        t1 = datetime.fromisoformat(cur_album['msgs'][-1]['date']) 
        t2 = datetime.fromisoformat(next_album['msgs'][0]['date'])
        diff = (t2 - t1).total_seconds()
        
        # <= 60 seconds (1 minute interval)
        if 0 <= diff <= 60:
            cur_photo = album_is_only_photo(cur_album)
            next_photo = album_is_only_photo(next_album)
            
            # Merge condition: one of them is only photo
            if (cur_photo and not next_photo) or (not cur_photo and next_photo):
                merged_count += 1
                combined_msgs = cur_album['msgs'] + next_album['msgs']
                
                new_gid = cur_album['gid'] or next_album['gid'] or f"merged_{combined_msgs[0]['id']}"
                for m in combined_msgs:
                    m['grouped_id'] = new_gid
                
                # Fold text-only messages into the first media message
                text_only_msgs = [m for m in combined_msgs if not m.get('media')]
                media_msgs = [m for m in combined_msgs if m.get('media')]
                
                if text_only_msgs and media_msgs:
                    base_msg = media_msgs[0]
                    for tm in text_only_msgs:
                        text_to_add = tm.get('text', '').strip()
                        if text_to_add:
                            if base_msg.get('text', '').strip():
                                base_msg['text'] += "\n\n" + text_to_add
                            else:
                                base_msg['text'] = text_to_add
                                
                        links = base_msg.get('links', []) + tm.get('links', [])
                        base_msg['links'] = list(set(links))
                        
                        combined_msgs.remove(tm)
                
                cur_album = {'gid': new_gid, 'msgs': combined_msgs}
                i += 1
            else:
                break
        else:
            break
            
    merged_albums.append(cur_album)
    i += 1

final_messages = other_messages
for a in merged_albums:
    for m in a['msgs']:
        final_messages.append(m)

final_messages.sort(key=lambda m: m.get('date') or '')

# Safe overwrite by keeping backup
if os.path.exists('magicdpd_readable_dump.backup.json'):
    os.remove('magicdpd_readable_dump.backup.json')
os.rename('magicdpd_readable_dump.json', 'magicdpd_readable_dump.backup.json')

with open('magicdpd_readable_dump.json', 'w', encoding='utf-8') as f:
    json.dump(final_messages, f, ensure_ascii=False, indent=2)

print(f"Done! Merged {merged_count} adjacent pairs/groups into unified posts (<= 60s gap).")
print(f"Original messages count: {len(messages)}")
print(f"Messages count after merge: {len(final_messages)}")
print("A backup of the original dump was saved to 'magicdpd_readable_dump.backup.json'.")
