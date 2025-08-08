#!/usr/bin/env python3
"""
Загрузка файлов Murderdoll в Supabase Storage
"""

import requests
import json
import os
from pathlib import Path

# Конфигурация
SUPABASE_URL = "https://rxmtovqxjsvogyywyrha.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1Mjg1NTAsImV4cCI6MjA3MDEwNDU1MH0.gDkJybktFoi486hbIVwppDfmVQlAR0fM4o4Sl1-AxhE"

headers = {
    'apikey': SUPABASE_ANON_KEY,
    'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
    'Content-Type': 'application/json',
    'Prefer': 'return=representation'
}

def upload_file_to_storage(file_path, storage_path):
    """Загрузка файла в Supabase Storage"""
    try:
        with open(file_path, 'rb') as file:
            files = {'file': file}
            response = requests.post(
                f"{SUPABASE_URL}/storage/v1/object/{storage_path}",
                headers={'apikey': SUPABASE_ANON_KEY, 'Authorization': f'Bearer {SUPABASE_ANON_KEY}'},
                files=files
            )
            
            if response.status_code in [200, 201]:
                print(f"  ✅ {os.path.basename(file_path)} загружен")
                return True
            else:
                print(f"  ❌ Ошибка загрузки {os.path.basename(file_path)}: {response.status_code}")
                return False
    except Exception as e:
        print(f"  ❌ Ошибка чтения файла {file_path}: {e}")
        return False

def add_gallery_entries(artist_id, gallery_files):
    """Добавление записей галереи в базу данных"""
    print(f"\n📋 Добавление записей галереи для артиста {artist_id}...")
    
    gallery_items = []
    for i, file_path in enumerate(gallery_files, 1):
        if os.path.exists(file_path):
            storage_url = f"https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets-public/artists/{artist_id}/gallery{i}.jpg"
            gallery_item = {
                "artist_id": artist_id,
                "image_url": storage_url,
                "title": f"Работа {i}"
            }
            gallery_items.append(gallery_item)
    
    if gallery_items:
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/artist_gallery",
            headers=headers,
            json=gallery_items
        )
        
        if response.status_code == 201:
            print(f"✅ Добавлено {len(gallery_items)} записей галереи")
            return True
        else:
            print(f"❌ Ошибка добавления галереи: {response.status_code}")
            return False
    else:
        print("⚠️ Нет файлов для добавления в галерею")
        return False

def main():
    print("🖼️ Загрузка файлов Murderdoll в Supabase Storage")
    print("=" * 60)
    
    # Пути к файлам Murderdoll
    base_path = Path("../../assets/artists/MurderDoll")
    artist_id = 4  # ID Murderdoll в базе данных
    
    print(f"📁 Базовый путь: {base_path}")
    print(f"🆔 ID артиста: {artist_id}")
    
    # Проверяем существование папки
    if not base_path.exists():
        print(f"❌ Папка {base_path} не найдена")
        return
    
    # Список файлов для загрузки
    files_to_upload = [
        ("avatar.png", f"gtm-assets-public/artists/{artist_id}/avatar.png"),
        ("gallery1.jpg", f"gtm-assets-public/artists/{artist_id}/gallery1.jpg"),
        ("gallery2.jpg", f"gtm-assets-public/artists/{artist_id}/gallery2.jpg"),
        ("gallery3.jpg", f"gtm-assets-public/artists/{artist_id}/gallery3.jpg"),
        ("gallery4.jpg", f"gtm-assets-public/artists/{artist_id}/gallery4.jpg"),
        ("gallery5.jpg", f"gtm-assets-public/artists/{artist_id}/gallery5.jpg"),
        ("gallery6.jpg", f"gtm-assets-public/artists/{artist_id}/gallery6.jpg"),
        ("gallery7.jpg", f"gtm-assets-public/artists/{artist_id}/gallery7.jpg"),
        ("gallery8.jpg", f"gtm-assets-public/artists/{artist_id}/gallery8.jpg"),
        ("gallery9.jpg", f"gtm-assets-public/artists/{artist_id}/gallery9.jpg"),
        ("gallery10.jpg", f"gtm-assets-public/artists/{artist_id}/gallery10.jpg"),
    ]
    
    # Загружаем файлы
    uploaded_count = 0
    gallery_files = []
    
    for local_file, storage_path in files_to_upload:
        local_path = base_path / local_file
        if local_path.exists():
            print(f"📤 Загружаем {local_file}...")
            if upload_file_to_storage(local_path, storage_path):
                uploaded_count += 1
                if local_file.startswith("gallery"):
                    gallery_files.append(str(local_path))
        else:
            print(f"⚠️ Файл {local_file} не найден")
    
    print(f"\n📊 Загружено файлов: {uploaded_count}/{len(files_to_upload)}")
    
    # Добавляем записи галереи в базу данных
    if gallery_files:
        add_gallery_entries(artist_id, gallery_files)
    
    print("\n✅ Загрузка файлов Murderdoll завершена!")

if __name__ == "__main__":
    main() 