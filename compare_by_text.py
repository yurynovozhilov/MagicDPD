#!/usr/bin/env python3
"""
Сравнивает посты из VK дампа и Wayback дампа по содержимому текста.
"""

import json
import re
from difflib import SequenceMatcher
from datetime import datetime

def normalize_text(text):
    """Нормализует текст для сравнения."""
    if not text:
        return ""
    # Удаляем лишние пробелы и переводы строк
    text = re.sub(r'\s+', ' ', text.strip().lower())
    # Удаляем специфичные для платформы элементы
    text = re.sub(r'https?://\S+', '', text)  # URL
    return text[:500]  # Первые 500 символов

def extract_title_from_wayback(text):
    """Извлекает заголовок из wayback текста."""
    if not text:
        return ""
    # Обычно первая строка - это заголовок
    lines = text.strip().split('\n')
    if lines:
        return lines[0].strip()
    return ""

def similarity_ratio(text1, text2):
    """Вычисляет схожесть двух текстов (0.0 - 1.0)."""
    return SequenceMatcher(None, text1, text2).ratio()

def parse_vk_date(date_str):
    """Парсит дату из VK дампа."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        return None

def get_text_signature(text):
    """Создает сигнатуру текста из первых 50 символов."""
    return normalize_text(text)[:50]

def main():
    print("Загрузка дампов...")
    
    # Загрузка VK дампа
    with open('/Users/GlukRazor/MagicDPD/magicdpd_readable_dump.json') as f:
        vk_posts = json.load(f)
    
    # Загрузка Wayback дампа
    with open('/Users/GlukRazor/MagicDPD/wayback_dump.json') as f:
        wayback_entries = json.load(f)
    
    print(f"VK постов: {len(vk_posts)}")
    print(f"Wayback записей: {len(wayback_entries)}")
    print()
    
    # Фильтруем wayback записи с текстом
    wayback_with_text = [(i, e) for i, e in enumerate(wayback_entries) if e.get('text', '').strip()]
    print(f"Wayback записей с текстом: {len(wayback_with_text)}")
    print()
    
    # Создаем индекс wayback по сигнатуре текста для быстрого поиска
    print("Создание индекса wayback записей...")
    wb_index = {}
    for wb_idx, wb_entry in wayback_with_text:
        wb_text = normalize_text(wb_entry.get('text', ''))
        if wb_text and len(wb_text) >= 20:
            signature = get_text_signature(wb_text)
            if signature not in wb_index:
                wb_index[signature] = []
            wb_index[signature].append((wb_idx, wb_entry, wb_text))
    
    print(f"Создан индекс с {len(wb_index)} уникальными сигнатурами")
    print()
    
    # Поиск совпадений
    matches = []
    vk_matched = set()
    wb_matched = set()
    
    print("Поиск совпадений...")
    
    for vk_idx, vk_post in enumerate(vk_posts):
        if vk_idx % 100 == 0:
            print(f"  Обработано VK постов: {vk_idx}/{len(vk_posts)}, найдено совпадений: {len(matches)}")
        
        vk_text = normalize_text(vk_post.get('text', ''))
        if not vk_text or len(vk_text) < 20:
            continue
        
        # Быстрый поиск по индексу
        signature = get_text_signature(vk_text)
        candidates = wb_index.get(signature, [])
        
        best_match = None
        best_ratio = 0
        
        for wb_idx, wb_entry, wb_text in candidates:
            if wb_idx in wb_matched:
                continue
            
            # Вычисляем схожесть
            ratio = similarity_ratio(vk_text, wb_text)
            
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = (wb_idx, wb_entry)
        
        # Считаем совпадением если схожесть > 70%
        if best_match and best_ratio > 0.7:
            wb_idx, wb_entry = best_match
            matches.append({
                'vk_idx': vk_idx,
                'wb_idx': wb_idx,
                'ratio': best_ratio,
                'vk_date': vk_post.get('date'),
                'wb_archive_date': wb_entry.get('archive_date'),
                'vk_text': vk_post.get('text', '')[:200],
                'wb_text': wb_entry.get('text', '')[:200],
                'vk_url': wb_entry.get('original_url', ''),
                'vk_likes': vk_post.get('likes', 0),
                'wb_image_count': wb_entry.get('image_count', 0),
            })
            vk_matched.add(vk_idx)
            wb_matched.add(wb_idx)
    
    print(f"  Обработано VK постов: {len(vk_posts)}/{len(vk_posts)}, найдено совпадений: {len(matches)}")
    print()
    
    # Сортируем по схожести
    matches.sort(key=lambda x: x['ratio'], reverse=True)
    
    # Результаты
    print(f"{'='*80}")
    print(f"РЕЗУЛЬТАТЫ СРАВНЕНИЯ ПО ТЕКСТУ:")
    print(f"{'='*80}")
    print(f"Найдено совпадений: {len(matches)}")
    print(f"VK постов без совпадений: {len(vk_posts) - len(vk_matched)}")
    print(f"Wayback записей без совпадений: {len(wayback_with_text) - len(wb_matched)}")
    print()
    
    if matches:
        print(f"{'='*80}")
        print(f"ПРИМЕРЫ СОВПАДЕНИЙ (топ 20 по схожести):")
        print(f"{'='*80}")
        
        for i, match in enumerate(matches[:20]):
            print(f"\n{i+1}. Схожесть: {match['ratio']:.1%}")
            print(f"   VK дата: {match['vk_date']}")
            print(f"   WB дата архивации: {match['wb_archive_date']}")
            print(f"   VK URL в архиве: {match['vk_url']}")
            print(f"   VK текст: {match['vk_text'][:150]}...")
            print(f"   WB текст: {match['wb_text'][:150]}...")
    
    # Статистика по датам
    print(f"\n{'='*80}")
    print(f"СТАТИСТИКА ПО РАЗНИЦЕ ДАТ:")
    print(f"{'='*80}")
    
    date_diffs = []
    for match in matches:
        vk_date = parse_vk_date(match['vk_date'])
        wb_date = parse_vk_date(match['wb_archive_date'])
        if vk_date and wb_date:
            diff_days = abs((wb_date - vk_date).days)
            date_diffs.append(diff_days)
    
    if date_diffs:
        print(f"Среднее расхождение: {sum(date_diffs)/len(date_diffs):.1f} дней")
        print(f"Минимум: {min(date_diffs)} дней")
        print(f"Максимум: {max(date_diffs)} дней")
        
        # Распределение
        same_day = sum(1 for d in date_diffs if d == 0)
        within_week = sum(1 for d in date_diffs if 0 < d <= 7)
        within_month = sum(1 for d in date_diffs if 7 < d <= 30)
        within_year = sum(1 for d in date_diffs if 30 < d <= 365)
        more_year = sum(1 for d in date_diffs if d > 365)
        
        print(f"\nРаспределение:")
        print(f"  В тот же день: {same_day}")
        print(f"  В течение недели: {within_week}")
        print(f"  В течение месяца: {within_month}")
        print(f"  В течение года: {within_year}")
        print(f"  Более года: {more_year}")
    
    # Сохраняем результаты
    with open('/Users/GlukRazor/MagicDPD/matches_result.json', 'w', encoding='utf-8') as f:
        json.dump(matches, f, ensure_ascii=False, indent=2)
    
    print(f"\nРезультаты сохранены в matches_result.json")

if __name__ == "__main__":
    main()
