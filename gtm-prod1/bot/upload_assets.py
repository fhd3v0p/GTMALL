#!/usr/bin/env python3
"""
GTM Supabase Assets Upload
Загрузка файлов из папки assets в Supabase Storage
"""
import os
import requests
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Конфигурация
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
SUPABASE_STORAGE_BUCKET = os.getenv('SUPABASE_STORAGE_BUCKET', 'gtm-assets-public')

def upload_assets():
    print("📤 Загрузка файлов в Supabase Storage...")
    print(f"URL: {SUPABASE_URL}")
    print(f"Bucket: {SUPABASE_STORAGE_BUCKET}")
    
    # Headers для service role
    service_headers = {
        'apikey': SUPABASE_SERVICE_ROLE_KEY,
        'Authorization': f'Bearer {SUPABASE_SERVICE_ROLE_KEY}',
        'Content-Type': 'application/json'
    }
    
    # Путь к папке assets
    assets_path = Path("../assets")
    if not assets_path.exists():
        print(f"❌ Папка assets не найдена: {assets_path}")
        return False
    
    print(f"📁 Папка assets: {assets_path.absolute()}")
    
    # Список файлов для загрузки
    files_to_upload = [
        # Баннеры
        ("assets/banners/city_selection_banner.png", "banners/city_selection_banner.png"),
        ("assets/banners/welcome_banner.png", "banners/welcome_banner.png"),
        ("assets/banners/artist_selection_banner.png", "banners/artist_selection_banner.png"),
        
        # Аватары
        ("assets/avatar1.png", "avatars/avatar1.png"),
        ("assets/avatar2.png", "avatars/avatar2.png"),
        ("assets/avatar3.png", "avatars/avatar3.png"),
        ("assets/avatar4.png", "avatars/avatar4.png"),
        
        # Артисты
        ("assets/artists/aspergill/avatar.png", "artists/aspergill/avatar.png"),
        ("assets/artists/Blodivamp/avatar.png", "artists/Blodivamp/avatar.png"),
        ("assets/artists/EMI/avatar.png", "artists/EMI/avatar.png"),
        ("assets/artists/Lin++/avatar.png", "artists/Lin++/avatar.png"),
        ("assets/artists/msk_tattoo_EMI/avatar.png", "artists/msk_tattoo_EMI/avatar.png"),
        ("assets/artists/Клубника/avatar.png", "artists/Клубника/avatar.png"),
        ("assets/artists/Чучундра/avatar.png", "artists/Чучундра/avatar.png"),
    ]
    
    uploaded_count = 0
    total_count = len(files_to_upload)
    
    for local_path, storage_path in files_to_upload:
        full_local_path = Path("../") / local_path
        
        if not full_local_path.exists():
            print(f"⚠️ Файл не найден: {full_local_path}")
            continue
        
        print(f"📤 Загружаем: {local_path} → {storage_path}")
        
        try:
            with open(full_local_path, 'rb') as file:
                files_data = {'file': (storage_path.split('/')[-1], file, 'application/octet-stream')}
                
                upload_url = f'{SUPABASE_URL}/storage/v1/object/{SUPABASE_STORAGE_BUCKET}/{storage_path}'
                response = requests.post(upload_url, headers=service_headers, files=files_data)
                
                if response.status_code == 200:
                    print(f"  ✅ Успешно загружен")
                    uploaded_count += 1
                else:
                    print(f"  ❌ Ошибка: {response.text[:100]}...")
        except Exception as e:
            print(f"  ❌ Ошибка: {e}")
    
    print(f"\n📊 Результат загрузки:")
    print(f"  Загружено: {uploaded_count}/{total_count} файлов")
    
    if uploaded_count > 0:
        print(f"\n✅ Файлы успешно загружены в бакет '{SUPABASE_STORAGE_BUCKET}'")
        return True
    else:
        print(f"\n❌ Не удалось загрузить файлы")
        return False

def test_public_access():
    """Тест публичного доступа к загруженным файлам"""
    print(f"\n🌐 Тест публичного доступа к файлам")
    
    # Headers для anon key
    anon_headers = {
        'apikey': os.getenv('SUPABASE_ANON_KEY'),
        'Authorization': f'Bearer {os.getenv("SUPABASE_ANON_KEY")}',
        'Content-Type': 'application/json'
    }
    
    # Тестируем доступ к загруженным файлам
    test_files = [
        "banners/city_selection_banner.png",
        "avatars/avatar1.png",
        "artists/aspergill/avatar.png"
    ]
    
    for file_path in test_files:
        test_url = f'{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_STORAGE_BUCKET}/{file_path}'
        print(f"Тестируем: {file_path}")
        
        try:
            response = requests.get(test_url, headers=anon_headers)
            if response.status_code == 200:
                print(f"  ✅ Доступен")
            else:
                print(f"  ❌ Недоступен: {response.status_code}")
        except Exception as e:
            print(f"  ❌ Ошибка: {e}")

if __name__ == "__main__":
    print("🚀 Загрузка файлов в Supabase Storage")
    print("=" * 50)
    
    if upload_assets():
        print("\n✅ Загрузка завершена успешно!")
        test_public_access()
    else:
        print("\n❌ Загрузка не удалась!") 