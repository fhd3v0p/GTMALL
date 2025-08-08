#!/usr/bin/env python3
"""
Загрузка галереи Lin++ в Supabase Storage и добавление в artist_gallery
"""

import os
import requests
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Конфигурация
SUPABASE_URL = "https://rxmtovqxjsvogyywyrha.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1Mjg1NTAsImV4cCI6MjA3MDEwNDU1MH0.gDkJybktFoi486hbIVwppDfmVQlAR0fM4o4Sl1-AxhE"
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

# Headers
anon_headers = {
    'apikey': SUPABASE_ANON_KEY,
    'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
    'Content-Type': 'application/json',
    'Prefer': 'return=representation'
}

service_headers = {
    'apikey': SUPABASE_SERVICE_ROLE_KEY,
    'Authorization': f'Bearer {SUPABASE_SERVICE_ROLE_KEY}',
    'Content-Type': 'application/json'
}

def upload_gallery_files():
    """Загрузка файлов галереи Lin++ в Supabase Storage"""
    print("📤 Загрузка файлов галереи Lin++ в Supabase Storage...")
    
    # Путь к папке с галереей Lin++
    gallery_path = Path("../assets/artists/Lin++")
    
    if not gallery_path.exists():
        print(f"❌ Папка не найдена: {gallery_path}")
        return False
    
    uploaded_files = []
    
    # Загружаем gallery1.jpg - gallery8.jpg
    for i in range(1, 9):
        filename = f"gallery{i}.jpg"
        local_file = gallery_path / filename
        storage_path = f"artists/Lin++/{filename}"
        
        if not local_file.exists():
            print(f"⚠️ Файл не найден: {local_file}")
            continue
        
        print(f"📤 Загружаем: {filename} → {storage_path}")
        
        try:
            with open(local_file, 'rb') as file:
                files_data = {'file': (filename, file, 'image/jpeg')}
                
                upload_url = f'{SUPABASE_URL}/storage/v1/object/gtm-assets-public/{storage_path}'
                response = requests.post(upload_url, headers=service_headers, files=files_data)
                
                if response.status_code == 200:
                    print(f"  ✅ Успешно загружен")
                    uploaded_files.append({
                        'filename': filename,
                        'storage_path': storage_path,
                        'public_url': f"{SUPABASE_URL}/storage/v1/object/public/gtm-assets-public/{storage_path}"
                    })
                else:
                    print(f"  ❌ Ошибка: {response.status_code} - {response.text[:100]}...")
        except Exception as e:
            print(f"  ❌ Ошибка: {e}")
    
    print(f"\n📊 Загружено файлов: {len(uploaded_files)}/8")
    return uploaded_files

def add_gallery_to_database(uploaded_files):
    """Добавление записей галереи в таблицу artist_gallery"""
    print("\n🖼️ Добавление галереи в базу данных...")
    
    artist_id = 7  # ID артиста Lin++
    gallery_items = []
    
    for i, file_info in enumerate(uploaded_files, 1):
        gallery_item = {
            "artist_id": artist_id,
            "image_url": file_info['public_url'],
            "title": f"Работа {i}"
        }
        gallery_items.append(gallery_item)
    
    # Добавляем галерею в базу
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/artist_gallery",
        headers=anon_headers,
        json=gallery_items
    )
    
    if response.status_code == 201:
        gallery = response.json()
        print(f"✅ Галерея добавлена: {len(gallery)} изображений")
        return gallery
    else:
        print(f"❌ Ошибка добавления галереи: {response.status_code}")
        print(f"   Ответ: {response.text}")
        return None

def check_existing_gallery():
    """Проверка существующей галереи для Lin++"""
    print("🔍 Проверка существующей галереи для Lin++...")
    
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/artist_gallery?artist_id=eq.7",
        headers=anon_headers
    )
    
    if response.status_code == 200:
        existing_gallery = response.json()
        if existing_gallery:
            print(f"⚠️ Найдено {len(existing_gallery)} существующих записей галереи")
            return existing_gallery
        else:
            print("✅ Существующих записей галереи не найдено")
            return []
    else:
        print(f"❌ Ошибка проверки галереи: {response.status_code}")
        return []

def main():
    print("🖼️ Загрузка галереи Lin++ в Supabase")
    print("=" * 50)
    
    # Проверяем существующую галерею
    existing_gallery = check_existing_gallery()
    
    if existing_gallery:
        print(f"\n⚠️ У Lin++ уже есть {len(existing_gallery)} записей в галерее")
        print("Хотите продолжить и добавить новые записи? (y/n): ", end="")
        # Для автоматизации продолжаем
        print("y")
    
    # Загружаем файлы в Storage
    uploaded_files = upload_gallery_files()
    
    if not uploaded_files:
        print("❌ Не удалось загрузить файлы")
        return
    
    # Добавляем в базу данных
    gallery = add_gallery_to_database(uploaded_files)
    
    if gallery:
        print(f"\n✅ Галерея Lin++ успешно загружена!")
        print(f"   Загружено файлов: {len(uploaded_files)}")
        print(f"   Добавлено записей: {len(gallery)}")
    else:
        print("\n❌ Не удалось добавить галерею в базу данных")

if __name__ == "__main__":
    main() 