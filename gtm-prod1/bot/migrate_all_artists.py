#!/usr/bin/env python3
"""
Скрипт для массовой загрузки всех артистов из папки assets/artists/ в Supabase
Загружает данные из links.json и bio.txt файлов, а также аватары и галереи
"""

import json
import os
import requests
import base64
from pathlib import Path

# Supabase конфигурация
SUPABASE_URL = "https://rxmtovqxjsvogyywyrha.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1Mjg1NTAsImV4cCI6MjA3MDEwNDU1MH0.gDkJybktFoi486hbIVwppDfmVQlAR0fM4o4Sl1-AxhE"
STORAGE_BUCKET = "gtm-assets-public"

# Путь к папке с артистами (относительно корня проекта)
ARTISTS_PATH = "../../assets/artists"

def get_headers():
    """Возвращает заголовки для API запросов"""
    return {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal'
    }

def get_storage_headers():
    """Возвращает заголовки для Storage API"""
    return {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
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

def upload_file_to_storage(file_path, storage_path):
    """Загружает файл в Supabase Storage"""
    try:
        with open(file_path, 'rb') as f:
            file_content = f.read()
        
        url = f"{SUPABASE_URL}/storage/v1/object/{STORAGE_BUCKET}/{storage_path}"
        headers = get_storage_headers()
        
        # Определяем Content-Type по расширению файла
        if file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
            headers['Content-Type'] = 'image/jpeg'
        elif file_path.endswith('.png'):
            headers['Content-Type'] = 'image/png'
        else:
            headers['Content-Type'] = 'application/octet-stream'
        
        response = requests.post(url, data=file_content, headers=headers)
        
        if response.status_code in [200, 201]:
            storage_url = f"{SUPABASE_URL}/storage/v1/object/public/{STORAGE_BUCKET}/{storage_path}"
            print(f"✅ Загружен файл: {storage_path}")
            return storage_url
        else:
            print(f"❌ Ошибка загрузки {storage_path}: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка загрузки файла {file_path}: {e}")
        return None

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

def insert_gallery_image(artist_name, image_url, display_order):
    """Вставляет изображение галереи в базу данных"""
    # Сначала находим ID артиста
    artist_url = f"{SUPABASE_URL}/rest/v1/artists?name=eq.{artist_name}&select=id"
    headers = get_headers()
    
    response = requests.get(artist_url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Ошибка поиска артиста {artist_name}: {response.status_code}")
        return False
    
    artists = response.json()
    if not artists:
        print(f"❌ Артист {artist_name} не найден в БД")
        return False
    
    artist_id = artists[0]['id']
    
    # Вставляем изображение галереи
    gallery_data = {
        "artist_id": artist_id,
        "image_url": image_url
    }
    
    gallery_url = f"{SUPABASE_URL}/rest/v1/artist_gallery"
    response = requests.post(gallery_url, json=gallery_data, headers=headers)
    
    if response.status_code in [200, 201]:
        print(f"✅ Изображение галереи добавлено для {artist_name}")
        return True
    else:
        print(f"❌ Ошибка добавления изображения галереи для {artist_name}: {response.status_code} - {response.text}")
        return False

def process_artist_folder(artist_folder_path):
    """Обрабатывает папку артиста и загружает все данные"""
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
    
    # Загружаем аватар
    avatar_file = None
    for ext in ['avatar.png', 'avatar.jpg']:
        avatar_path = os.path.join(artist_folder_path, ext)
        if os.path.exists(avatar_path):
            avatar_file = avatar_path
            break
    
    avatar_url = None
    if avatar_file:
        storage_path = f"artists/{folder_name}/avatar.{avatar_file.split('.')[-1]}"
        avatar_url = upload_file_to_storage(avatar_file, storage_path)
    
    # Загружаем изображения галереи
    gallery_urls = []
    for i in range(1, 11):  # gallery1.jpg - gallery10.jpg
        gallery_file = os.path.join(artist_folder_path, f"gallery{i}.jpg")
        if os.path.exists(gallery_file):
            storage_path = f"artists/{folder_name}/gallery{i}.jpg"
            gallery_url = upload_file_to_storage(gallery_file, storage_path)
            if gallery_url:
                gallery_urls.append((gallery_url, i))
    
    # Подготавливаем данные для БД
    specialties = []
    if links_data.get('category'):
        if links_data['category'] == 'Tattoo':
            specialties = ["Татуировки", "Черно-белые тату", "Цветные тату"]
        elif links_data['category'] == 'Piercing':
            specialties = ["Пирсинг", "Проколы ушей", "Боди пирсинг"]
        else:
            specialties = [links_data['category']]
    
    artist_data = {
        "name": links_data.get('name', folder_name),
        "username": links_data.get('telegram', '').replace('@', '') if links_data.get('telegram') else folder_name.lower(),
        "bio": bio_content or f"Мастер {links_data.get('category', 'Art')}",
        "avatar_url": avatar_url,
        "city": links_data.get('city', 'Санкт-Петербург'),
        "specialties": specialties,
        "rating": 4.5,
        "telegram": links_data.get('telegram', ''),
        "telegram_url": links_data.get('telegramUrl', ''),
        "instagram": links_data.get('instagram', ''),
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
        for gallery_url, order in gallery_urls:
            insert_gallery_image(artist_data['name'], gallery_url, order)
        return True
    
    return False

def main():
    """Основная функция"""
    print("🚀 Начинаем массовую загрузку артистов в Supabase...")
    
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