import vk_api
import json
import time
import os
import webbrowser
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
VK_LOGIN = os.getenv("VK_LOGIN")
VK_PASSWORD = os.getenv("VK_PASSWORD")
VK_TOKEN = os.getenv("VK_TOKEN")

def get_all_posts(vk, domain):
    all_posts = []
    offset = 0
    count = 100
    
    print(f"[*] Starting dump for {domain}...")
    
    while True:
        try:
            response = vk.wall.get(domain=domain, count=count, offset=offset)
            posts = response.get('items', [])
            
            if not posts:
                break
                
            all_posts.extend(posts)
            offset += count
            
            print(f"[+] Fetched {len(all_posts)} / {response['count']} posts...")
            time.sleep(0.34)
            
        except Exception as e:
            print(f"[!] Error fetching posts: {e}")
            break
            
    return all_posts

def captcha_handler(captcha):
    webbrowser.open(captcha.get_url())
    tty = open('/dev/tty')
    print(f"Captcha opened in browser. Enter the text from the image: ", end='', flush=True)
    key = tty.readline().strip()
    tty.close()
    return captcha.try_again(key)

def auth_handler():
    tty = open('/dev/tty')
    print("Enter 2FA code from SMS/app: ", end='', flush=True)
    code = tty.readline().strip()
    tty.close()
    return code, True

def main():
    if VK_LOGIN and VK_PASSWORD:
        print(f"[*] Logging in as {VK_LOGIN}...")
        vk_session = vk_api.VkApi(
            login=VK_LOGIN,
            password=VK_PASSWORD,
            auth_handler=auth_handler,
            captcha_handler=captcha_handler,
        )
        try:
            vk_session.auth()
        except vk_api.AuthError as e:
            print(f"[!] Auth error: {e}")
            return
    elif VK_TOKEN:
        vk_session = vk_api.VkApi(token=VK_TOKEN)
    else:
        print("[!] No VK_LOGIN/VK_PASSWORD or VK_TOKEN found in .env!")
        return

    vk = vk_session.get_api()

    try:
        domain = 'magicdpd'
        posts = get_all_posts(vk, domain)
        
        # Save raw data
        os.makedirs('vk', exist_ok=True)
        raw_file = f"vk/{domain}_raw_dump.json"
        with open(raw_file, 'w', encoding='utf-8') as f:
            json.dump(posts, f, ensure_ascii=False, indent=4)
            
        print(f"\n[*] Raw data saved to {raw_file}")

        # Process data for readability
        readable_data = []
        for post in posts:
            date = datetime.fromtimestamp(post['date']).strftime('%Y-%m-%d %H:%M:%S')
            text = post.get('text', '')
            
            attachments = []
            if 'attachments' in post:
                for att in post['attachments']:
                    att_type = att['type']
                    if att_type == 'photo':
                        # Get largest image
                        sizes = att['photo']['sizes']
                        best_size = max(sizes, key=lambda x: x['width'] * x['height'])
                        attachments.append({'type': 'photo', 'url': best_size['url']})
                    elif att_type == 'video':
                        attachments.append({'type': 'video', 'title': att['video'].get('title', 'Video')})
                    elif att_type == 'link':
                        attachments.append({'type': 'link', 'url': att['link']['url']})
                    else:
                        attachments.append({'type': att_type})

            readable_data.append({
                'date': date,
                'text': text,
                'attachments': attachments,
                'likes': post.get('likes', {}).get('count', 0),
                'reposts': post.get('reposts', {}).get('count', 0),
                'comments': post.get('comments', {}).get('count', 0),
                'id': post['id']
            })

        processed_file = f"vk/{domain}_readable_dump.json"
        with open(processed_file, 'w', encoding='utf-8') as f:
            json.dump(readable_data, f, ensure_ascii=False, indent=4)

        print(f"[*] Processed data saved to {processed_file}")
        print(f"[*] Total posts dumped: {len(posts)}")
        
    except Exception as e:
        print(f"[!] An error occurred: {e}")

if __name__ == "__main__":
    main()
