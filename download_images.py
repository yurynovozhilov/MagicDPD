import json
import os
import requests
import time
from urllib.parse import urlparse

def download_images():
    # File to read from
    dump_file = 'magicdpd_readable_dump.json'
    # Folder to save images
    output_dir = 'images'
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"[*] Created directory: {output_dir}")

    if not os.path.exists(dump_file):
        print(f"[!] {dump_file} not found. Please run dump_vk.py first.")
        return

    with open(dump_file, 'r', encoding='utf-8') as f:
        posts = json.load(f)

    total_images = 0
    downloaded = 0
    errors = 0

    # First pass: count total images
    for post in posts:
        for att in post.get('attachments', []):
            if att.get('type') == 'photo':
                total_images += 1

    print(f"[*] Found {total_images} images to download.")

    # Second pass: download
    for post in posts:
        post_id = post.get('id')
        img_idx = 0
        for att in post.get('attachments', []):
            if att.get('type') == 'photo' and 'url' in att:
                url = att['url']
                img_idx += 1
                
                # Get extension from URL
                path = urlparse(url).path
                ext = os.path.splitext(path)[1]
                if not ext:
                    ext = '.jpg'
                
                filename = f"post_{post_id}_{img_idx}{ext}"
                filepath = os.path.join(output_dir, filename)

                if os.path.exists(filepath):
                    downloaded += 1
                    continue

                try:
                    response = requests.get(url, timeout=10)
                    if response.status_code == 200:
                        with open(filepath, 'wb') as f:
                            f.write(response.content)
                        downloaded += 1
                        if downloaded % 50 == 0:
                            print(f"[+] Downloaded {downloaded}/{total_images}...")
                    else:
                        print(f"[!] Failed to download {url}: Status {response.status_code}")
                        errors += 1
                except Exception as e:
                    print(f"[!] Error downloading {url}: {e}")
                    errors += 1
                
                # Tiny sleep to avoid overloading the server
                # time.sleep(0.05)

    print(f"\n[*] Download complete!")
    print(f"[*] Total downloaded: {downloaded}")
    print(f"[*] Total errors: {errors}")

if __name__ == "__main__":
    download_images()
