#!/usr/bin/env python3
"""
Скрипт для загрузки артистов только в базу данных (без загрузки файлов в Storage)
Использует прямые ссылки на файлы для аватаров и галереи
"""

import json
import os
import requests
from pathlib import Path

# Supabase конфигурация
SUPABASE_URL = "https://rxmtovqxjsvogyywyrha.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1Mjg1NTAsImV4cCI6MjA3MDEwNDU1MH0.gDkJybktFoi486hbIVwppDfmVQlAR0fM4o4Sl1-AxhE"

# Базовый URL для assets (будет использоваться как CDN)
CDN_BASE_URL = "/assets/artists"

# Путь к папке с артистами
ARTISTS_PATH = "../../assets/artists"

def get_headers():
    """Возвращает заголовки для API запросов"""
    return {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal'
    }

def read_json_file(file_path):
    """Читает JSON файл и возвращает данные"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Ошибка чтения {file_path}: {e}")
        return None

def read_text_file(file_path):
    """Читает текстовый файл и возвращает содержимое"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        print(f"Ошибка чтения {file_path}: {e}")
        return ""

def insert_artist_to_db(artist_data):
    """Вставляет данные артиста в базу данных"""
    url = f"{SUPABASE_URL}/rest/v1/artists"
    headers = get_headers()
    
    response = requests.post(url, json=artist_data, headers=headers)
    
    if response.status_code in [200, 201]:
        print(f"✅ Артист {artist_data['name']} добавлен в БД")
        return True
    else:
        print(f"❌ Ошибка добавления артиста {artist_data['name']}: {response.status_code} - {response.text}")
        return False

def get_artist_id(artist_name):
    """Получает ID артиста по имени"""
    url = f"{SUPABASE_URL}/rest/v1/artists?name=eq.{artist_name}&select=id"
    headers = get_headers()
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Ошибка поиска артиста {artist_name}: {response.status_code}")
        return None
    
    artists = response.json()
    if not artists:
        print(f"❌ Артист {artist_name} не найден в БД")
        return None
    
    return artists[0]['id']

def insert_gallery_images(artist_name, gallery_urls):
    """Вставляет изображения галереи в базу данных"""
    artist_id = get_artist_id(artist_name)
    if not artist_id:
        return False
    
    url = f"{SUPABASE_URL}/rest/v1/artist_gallery"
    headers = get_headers()
    
    success_count = 0
    for gallery_url in gallery_urls:
        gallery_data = {
            "artist_id": artist_id,
            "image_url": gallery_url
        }
        
        response = requests.post(url, json=gallery_data, headers=headers)
        
        if response.status_code in [200, 201]:
            success_count += 1
        else:
            print(f"❌ Ошибка добавления изображения галереи для {artist_name}: {response.status_code} - {response.text}")
    
    print(f"✅ Добавлено {success_count}/{len(gallery_urls)} изображений галереи для {artist_name}")
    return success_count > 0

def process_artist_folder(artist_folder_path):
    """Обрабатывает папку артиста и загружает данные в БД"""
    folder_name = os.path.basename(artist_folder_path)
    print(f"\n🎨 Обрабатываем артиста: {folder_name}")
    
    # Читаем links.json
    links_file = os.path.join(artist_folder_path, "links.json")
    if not os.path.exists(links_file):
        print(f"❌ Файл links.json не найден в {folder_name}")
        return False
    
    links_data = read_json_file(links_file)
    if not links_data:
        print(f"❌ Не удалось прочитать links.json для {folder_name}")
        return False
    
    # Читаем bio.txt если есть
    bio_file = os.path.join(artist_folder_path, "bio.txt")
    bio_content = read_text_file(bio_file) if os.path.exists(bio_file) else ""
    
    # Определяем URL аватара
    avatar_url = None
    for ext in ['png', 'jpg']:
        avatar_file = os.path.join(artist_folder_path, f"avatar.{ext}")
        if os.path.exists(avatar_file):
            avatar_url = f"{CDN_BASE_URL}/{folder_name}/avatar.{ext}"
            break
    
    # Определяем URLs галереи
    gallery_urls = []
    for i in range(1, 11):  # gallery1.jpg - gallery10.jpg
        gallery_file = os.path.join(artist_folder_path, f"gallery{i}.jpg")
        if os.path.exists(gallery_file):
            gallery_url = f"{CDN_BASE_URL}/{folder_name}/gallery{i}.jpg"
            gallery_urls.append(gallery_url)
    
    # Определяем специализации на основе категории
    specialties = []
    category = links_data.get('category', '')
    if category == 'Tattoo':
        specialties = ["Черно-белые тату", "Цветные тату", "Минимализм"]
    elif category == 'Piercing':
        specialties = ["Пирсинг ушей", "Боди пирсинг", "Классический пирсинг"]
    elif category:
        specialties = [category]
    
    # Подготавливаем данные для БД (только поля из существующей схемы)
    artist_data = {
        "name": links_data.get('name', folder_name),
        "username": links_data.get('telegram', '').replace('@', '') if links_data.get('telegram') else folder_name.lower(),
        "bio": bio_content or f"Профессиональный мастер {category}",
        "avatar_url": avatar_url,
        "city": links_data.get('city', 'Санкт-Петербург'),
        "specialties": specialties,
        "rating": 4.5,
        "telegram": links_data.get('telegram', ''),
        "telegram_url": links_data.get('telegramUrl', ''),
        "tiktok": links_data.get('tiktok', ''),
        "tiktok_url": links_data.get('tiktokUrl', ''),
        "pinterest": links_data.get('pinterest', ''),
        "pinterest_url": links_data.get('pinterestUrl', ''),
        "booking_url": links_data.get('bookingUrl', ''),
        "location_html": links_data.get('locationHtml', ''),
        "is_active": True
    }
    
    # Вставляем артиста в БД
    if insert_artist_to_db(artist_data):
        # Вставляем изображения галереи
        if gallery_urls:
            insert_gallery_images(artist_data['name'], gallery_urls)
        return True
    
    return False

def main():
    """Основная функция"""
    print("🚀 Начинаем загрузку артистов в Supabase БД...")
    
    # Получаем абсолютный путь к папке с артистами
    script_dir = os.path.dirname(os.path.abspath(__file__))
    artists_dir = os.path.join(script_dir, ARTISTS_PATH)
    artists_dir = os.path.normpath(artists_dir)
    
    print(f"📁 Путь к артистам: {artists_dir}")
    
    if not os.path.exists(artists_dir):
        print(f"❌ Папка с артистами не найдена: {artists_dir}")
        return
    
    # Получаем список всех папок артистов
    artist_folders = [
        d for d in os.listdir(artists_dir) 
        if os.path.isdir(os.path.join(artists_dir, d)) and not d.startswith('.')
    ]
    
    print(f"📊 Найдено папок артистов: {len(artist_folders)}")
    
    success_count = 0
    error_count = 0
    
    # Обрабатываем каждого артиста
    for folder_name in artist_folders:
        artist_folder_path = os.path.join(artists_dir, folder_name)
        
        try:
            if process_artist_folder(artist_folder_path):
                success_count += 1
            else:
                error_count += 1
        except Exception as e:
            print(f"❌ Критическая ошибка при обработке {folder_name}: {e}")
            error_count += 1
    
    print(f"\n📈 Результаты загрузки:")
    print(f"✅ Успешно загружено: {success_count}")
    print(f"❌ Ошибок: {error_count}")
    print(f"📊 Всего обработано: {success_count + error_count}")

if __name__ == "__main__":
    main()