# MagicDPD Archive Tool

A Python utility for archiving posts and images from the VKontakte community "magicdpd", including Wayback Machine snapshot recovery.

## Features

- **VK Community Archive**: Download posts and images from VKontakte
- **Wayback Machine Recovery**: Retrieve historical snapshots of deleted content
- **Bulk Image Download**: Automated downloading of all image attachments
- **JSON Export**: Structured data export in both raw and readable formats

## Prerequisites

- Python 3.14.2 or higher
- VK API access token (for VK scraping)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yurynovozhilov/MagicDPD.git
cd MagicDPD
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
   - Create a `.env` file in the project root
   - Add your VK API token: `VK_TOKEN=your_token_here`

## Usage

### VK Community Archiving

1. **Dump posts from VK**:
```bash
python dump_vk.py
```
This creates:
- `magicdpd_raw_dump.json` - Raw API response data
- `magicdpd_readable_dump.json` - Processed data for image downloading

2. **Download images**:
```bash
python download_images.py
```
Downloads all photo attachments to the `images/` directory.

### Telegram Channel Archiving

1. **Configure Telegram credentials**: add the following to `.env` (API credentials are created at [https://my.telegram.org](https://my.telegram.org)):
   ```
   TELEGRAM_API_ID=your_api_id
   TELEGRAM_API_HASH=your_api_hash
   TELEGRAM_PHONE=+1XXXXXXXXXX         # only needed on the first run to receive the login code
   TELEGRAM_CHANNEL=@MagicDPD          # or any public/private channel you have access to
   TELEGRAM_SESSION=magicdpd_session   # optional, stores the local login session
   TELEGRAM_LIMIT=0                    # optional, number of messages to fetch (0 = all)
   ```

2. **Dump the channel**:
```bash
python dump_telegram.py
```
This script uses Telethon to iterate over every message in the channel and produces two files:
- `<channel>_telegram_raw_dump.json` — full Telethon `Message.to_dict()` payload for each message
- `<channel>_telegram_readable_dump.json` — trimmed JSON with text, metadata, media descriptions, and links

The script prints progress every 100 messages and can resume quickly thanks to the local `.session` file.

### Wayback Machine Recovery

1. **Scrape Wayback Machine snapshots**:
```bash
python wayback_scraper.py
```
This creates:
- `wayback_cdx_cache.json` - CDX index cache
- `wayback_dump.json` - Scraped post data
- `wayback_urls.txt` - List of discovered URLs
- `wayback_image_urls.txt` - List of image URLs

2. **Download historical images**:
```bash
python download_wayback_images.py
```
Downloads images to the `images_wayback/` directory.

## Project Structure

```
MagicDPD/
├── dump_vk.py                    # VK post scraper
├── download_images.py            # VK image downloader
├── wayback_scraper.py            # Wayback Machine scraper
├── download_wayback_images.py   # Wayback image downloader
├── requirements.txt              # Python dependencies
├── .env                          # Environment variables (not in git)
├── images/                       # Downloaded VK images (not in git)
├── images_wayback/              # Downloaded Wayback images (not in git)
└── *.json                        # Data dumps
```

## Jekyll Static Blog

В директории `site/` находится восстановленный блог MagicDPD на Jekyll. Контент автоматически строится по дампу Wayback.

### Генерация Markdown-постов

```bash
python generate_jekyll_posts.py
```

Скрипт `generate_jekyll_posts.py` читает `wayback_dump.json`, очищает текст от служебной разметки WordPress и создаёт публикации в `site/_posts`.

### Локальный запуск блога

```bash
cd site
bundle install
bundle exec jekyll serve --livereload
```

После сборки сайт доступен на `http://127.0.0.1:4000`. Конфигурация включает пагинацию, страницу архива и галереи изображений. Для обновления достаточно перегенерировать посты и перезапустить `jekyll serve`.

## Dependencies

- `vk_api==11.10.0` - VKontakte API wrapper
- `requests==2.32.5` - HTTP library
- `python-dotenv==1.2.1` - Environment variable management
- `urllib3==2.6.3` - HTTP client
- `charset-normalizer==3.4.4` - Character encoding detection

## Notes

- Large JSON dumps and image directories are excluded from git by default
- Keep your `.env` file secure and never commit it to the repository
- The Wayback Machine scraper respects rate limits to avoid overwhelming the service

## License

This project is for archival and educational purposes.
