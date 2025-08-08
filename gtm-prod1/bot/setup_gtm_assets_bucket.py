#!/usr/bin/env python3
"""
Настройка бакета gtm-assets с правильной структурой
"""

import requests
import json

# Конфигурация
SUPABASE_URL = "https://rxmtovqxjsvogyywyrha.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1Mjg1NTAsImV4cCI6MjA3MDEwNDU1MH0.gDkJybktFoi486hbIVwppDfmVQlAR0fM4o4Sl1-AxhE"
BUCKET_NAME = "gtm-assets"

headers = {
    'apikey': SUPABASE_ANON_KEY,
    'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
    'Content-Type': 'application/json'
}

def create_gtm_assets_bucket():
    """Создание бакета gtm-assets"""
    print("🆕 Создание бакета gtm-assets...")
    
    bucket_data = {
        "id": BUCKET_NAME,
        "name": BUCKET_NAME,
        "public": True,
        "file_size_limit": 52428800,  # 50MB
        "allowed_mime_types": ["image/jpeg", "image/png", "image/webp", "image/gif"]
    }
    
    response = requests.post(
        f"{SUPABASE_URL}/storage/v1/bucket",
        headers=headers,
        json=bucket_data
    )
    
    if response.status_code == 200:
        print(f"✅ Бакет {BUCKET_NAME} создан успешно!")
        return True
    else:
        print(f"❌ Ошибка создания бакета: {response.status_code}")
        print(f"   Ответ: {response.text}")
        return False

def check_bucket_exists():
    """Проверка существования бакета"""
    try:
        response = requests.get(
            f"{SUPABASE_URL}/storage/v1/bucket",
            headers=headers
        )
        
        if response.status_code == 200:
            buckets = response.json()
            print(f"📋 Найдено buckets: {len(buckets)}")
            
            for bucket in buckets:
                print(f"   - {bucket['name']} (public: {bucket.get('public', False)})")
                if bucket['name'] == BUCKET_NAME:
                    print(f"     ✅ Бакет {BUCKET_NAME} найден!")
                    return bucket
            
            print(f"❌ Бакет {BUCKET_NAME} не найден")
            return None
        else:
            print(f"❌ Ошибка получения buckets: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Исключение при проверке buckets: {e}")
        return None

def create_directory_structure():
    """Создание структуры директорий"""
    print("\n📁 Создание структуры директорий...")
    
    directories = [
        "artists",
        "avatars", 
        "banners",
        "gtm-merch",
        "products"
    ]
    
    created_count = 0
    for directory in directories:
        # Создаем пустой файл для создания директории
        dummy_file_path = f"{directory}/.keep"
        dummy_data = ""
        
        response = requests.post(
            f"{SUPABASE_URL}/storage/v1/object/{BUCKET_NAME}/{dummy_file_path}",
            headers=headers,
            data=dummy_data
        )
        
        if response.status_code == 200:
            print(f"  ✅ Создана директория: {directory}")
            created_count += 1
        else:
            print(f"  ❌ Ошибка создания директории {directory}: {response.status_code}")
    
    print(f"\n📊 Создано директорий: {created_count}/{len(directories)}")
    return created_count == len(directories)

def main():
    print("🔧 Настройка бакета gtm-assets")
    print("=" * 50)
    
    # Проверяем существующий бакет
    existing_bucket = check_bucket_exists()
    
    if existing_bucket:
        print(f"\n✅ Бакет {BUCKET_NAME} уже существует!")
        if existing_bucket.get('public'):
            print("✅ Бакет уже публичный!")
        else:
            print("⚠️ Бакет не публичный, нужно настроить...")
    else:
        # Создаем бакет
        if create_gtm_assets_bucket():
            print("✅ Бакет создан успешно!")
        else:
            print("❌ Не удалось создать бакет")
            return
    
    # Создаем структуру директорий
    if create_directory_structure():
        print("\n✅ Структура директорий создана!")
        print("\n📋 Структура бакета gtm-assets:")
        print("   ├── artists/     (артисты)")
        print("   ├── avatars/     (аватары)")
        print("   ├── banners/     (баннеры)")
        print("   ├── gtm-merch/   (мерч)")
        print("   └── products/    (продукты)")
    else:
        print("\n❌ Не удалось создать структуру директорий")

if __name__ == "__main__":
    main() 