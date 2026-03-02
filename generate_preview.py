#!/usr/bin/env python3
"""Generate HTML preview with random posts from wayback_dump.json"""

import json
import random
from datetime import datetime

# Load posts
with open('wayback_dump.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

# Filter posts with content
posts_with_content = [p for p in posts if p.get('text') or p.get('images')]

# Select 10 random posts
random.seed(42)  # For reproducibility
selected = random.sample(posts_with_content, min(10, len(posts_with_content)))

# Generate HTML
html = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MagicDPD Archive Preview - 10 Random Posts</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .stats {
            color: #7f8c8d;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #ecf0f1;
        }
        .post {
            margin-bottom: 40px;
            padding: 30px;
            background: #fafafa;
            border-left: 4px solid #3498db;
            border-radius: 4px;
        }
        .post-header {
            margin-bottom: 20px;
        }
        .post-title {
            font-size: 1.8em;
            color: #2c3e50;
            margin-bottom: 10px;
            font-weight: 600;
        }
        .post-meta {
            color: #7f8c8d;
            font-size: 0.9em;
            margin-bottom: 5px;
        }
        .post-meta a {
            color: #3498db;
            text-decoration: none;
        }
        .post-meta a:hover {
            text-decoration: underline;
        }
        .post-text {
            margin: 20px 0;
            white-space: pre-wrap;
            line-height: 1.8;
            font-size: 1.05em;
        }
        .post-images {
            margin: 20px 0;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 15px;
        }
        .post-images img {
            width: 100%;
            height: auto;
            border-radius: 4px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .post-links {
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #e0e0e0;
        }
        .post-links a {
            display: inline-block;
            margin-right: 15px;
            margin-bottom: 8px;
            color: #3498db;
            text-decoration: none;
            font-size: 0.9em;
        }
        .post-links a:hover {
            text-decoration: underline;
        }
        .tag {
            background: #3498db;
            color: white;
            padding: 3px 10px;
            border-radius: 3px;
            font-size: 0.85em;
            display: inline-block;
            margin-right: 5px;
            margin-bottom: 5px;
        }
        .wayback-link {
            display: inline-block;
            margin-top: 10px;
            padding: 8px 15px;
            background: #e74c3c;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            font-size: 0.9em;
        }
        .wayback-link:hover {
            background: #c0392b;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 MagicDPD Archive Preview</h1>
        <div class="stats">
            <p><strong>Всего постов в архиве:</strong> """ + str(len(posts)) + """</p>
            <p><strong>Постов с контентом:</strong> """ + str(len(posts_with_content)) + """</p>
            <p><strong>Показано случайных постов:</strong> """ + str(len(selected)) + """</p>
            <p><strong>Дата генерации:</strong> """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
        </div>
"""

# Add posts
for i, post in enumerate(selected, 1):
    title = post.get('title', 'Без заголовка')
    text = post.get('text', '')
    archive_date = post.get('archive_date', '')
    wayback_url = post.get('wayback_url', '')
    original_url = post.get('original_url', '')
    images = post.get('images', [])
    links = post.get('links', [])

    html += f"""
        <div class="post">
            <div class="post-header">
                <h2 class="post-title">{i}. {title}</h2>
                <div class="post-meta">
                    <p><strong>Дата архивации:</strong> {archive_date}</p>
                    <p><strong>Оригинальный URL:</strong> <a href="{original_url}" target="_blank">{original_url}</a></p>
                </div>
                <a href="{wayback_url}" target="_blank" class="wayback-link">🕐 Открыть в Wayback Machine</a>
            </div>
"""

    if text:
        html += f"""
            <div class="post-text">{text}</div>
"""

    if images:
        html += """
            <div class="post-images">
"""
        for img in images[:6]:  # Показываем максимум 6 изображений
            img_src = img.get('wayback_src') or img.get('src', '')
            img_alt = img.get('alt', 'Image')
            html += f"""
                <img src="{img_src}" alt="{img_alt}" loading="lazy">
"""
        html += """
            </div>
"""

    if links:
        html += """
            <div class="post-links">
                <strong>Ссылки:</strong><br>
"""
        for link in links[:10]:  # Показываем максимум 10 ссылок
            link_text = link.get('text', 'Link')
            link_url = link.get('url', '#')
            html += f"""
                <a href="{link_url}" target="_blank">→ {link_text}</a>
"""
        html += """
            </div>
"""

    html += """
        </div>
"""

html += """
    </div>
</body>
</html>
"""

# Save HTML
with open('preview.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✅ HTML страница создана: preview.html")
print(f"📊 Всего постов: {len(posts)}")
print(f"📝 Постов с контентом: {len(posts_with_content)}")
print(f"🎲 Выбрано случайных постов: {len(selected)}")
