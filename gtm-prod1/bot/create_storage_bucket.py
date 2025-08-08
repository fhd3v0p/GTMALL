#!/usr/bin/env python3
"""
Создание и настройка Supabase Storage bucket gtm-assets-public
"""

import requests
import json

# Конфигурация
SUPABASE_URL = "https://rxmtovqxjsvogyywyrha.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1Mjg1NTAsImV4cCI6MjA3MDEwNDU1MH0.gDkJybktFoi486hbIVwppDfmVQlAR0fM4o4Sl1-AxhE"
BUCKET_NAME = "gtm-assets-public"

headers = {
    'apikey': SUPABASE_ANON_KEY,
    'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
    'Content-Type': 'application/json'
}

def create_bucket():
    """Создание bucket"""
    try:
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
            print(f"✅ Bucket {BUCKET_NAME} создан успешно!")
            return True
        else:
            print(f"❌ Ошибка создания bucket: {response.status_code}")
            print(f"   Ответ: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Исключение при создании bucket: {e}")
        return False

def create_folder_structure():
    """Создание структуры папок"""
    folders = [
        "artists",
        "artists/Чучундра",
        "avatars",
        "gallery",
        "banners", 
        "GTM_products"
    ]
    
    print("\n📁 Создание структуры папок...")
    
    for folder in folders:
        try:
            # Создаем пустой файл .gitkeep для создания папки
            file_data = b""
            
            response = requests.post(
                f"{SUPABASE_URL}/storage/v1/object/{BUCKET_NAME}/{folder}/.gitkeep",
                headers={
                    'apikey': SUPABASE_ANON_KEY,
                    'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
                },
                files={'file': ('/.gitkeep', file_data, 'text/plain')}
            )
            
            if response.status_code == 200:
                print(f"   ✅ Папка {folder}/ создана")
            else:
                print(f"   ❌ Ошибка создания папки {folder}/: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Исключение при создании папки {folder}/: {e}")

def upload_placeholder_files():
    """Загрузка placeholder файлов для Чучундра"""
    print("\n🎨 Создание placeholder файлов для Чучундра...")
    
    # Создаем простой SVG placeholder для аватара
    avatar_svg = '''<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect width="200" height="200" fill="#2D2A3A"/>
  <circle cx="100" cy="80" r="30" fill="#666"/>
  <path d="M70 140 Q100 120 130 140 Q130 160 100 180 Q70 160 70 140" fill="#666"/>
  <text x="100" y="195" text-anchor="middle" fill="#999" font-size="12">Чучундра</text>
</svg>'''
    
    # Загружаем аватар
    try:
        response = requests.post(
            f"{SUPABASE_URL}/storage/v1/object/{BUCKET_NAME}/artists/Чучундра/avatar.png",
            headers={
                'apikey': SUPABASE_ANON_KEY,
                'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
            },
            files={'file': ('avatar.svg', avatar_svg.encode(), 'image/svg+xml')}
        )
        
        if response.status_code == 200:
            print("   ✅ Placeholder аватар загружен")
        else:
            print(f"   ❌ Ошибка загрузки аватара: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Исключение при загрузке аватара: {e}")
    
    # Загружаем placeholder галерею
    gallery_svg = '''<svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">
  <rect width="400" height="300" fill="#1A1820"/>
  <rect x="50" y="50" width="300" height="200" fill="#333" stroke="#666" stroke-width="2"/>
  <text x="200" y="140" text-anchor="middle" fill="#999" font-size="16">Tattoo Work</text>
  <text x="200" y="165" text-anchor="middle" fill="#666" font-size="12">by Чучундра</text>
</svg>'''
    
    for i in range(1, 11):
        try:
            response = requests.post(
                f"{SUPABASE_URL}/storage/v1/object/{BUCKET_NAME}/artists/Чучундра/gallery{i}.jpg",
                headers={
                    'apikey': SUPABASE_ANON_KEY,
                    'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
                },
                files={'file': (f'gallery{i}.svg', gallery_svg.encode(), 'image/svg+xml')}
            )
            
            if response.status_code == 200:
                print(f"   ✅ Placeholder gallery{i}.jpg загружен")
            else:
                print(f"   ❌ Ошибка загрузки gallery{i}.jpg: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Исключение при загрузке gallery{i}.jpg: {e}")

def main():
    print("🚀 Создание и настройка Supabase Storage")
    print("=" * 50)
    
    print("1. Создание bucket...")
    if create_bucket():
        print("2. Создание структуры папок...")
        create_folder_structure()
        
        print("3. Загрузка placeholder файлов...")
        upload_placeholder_files()
        
        print("\n✅ Storage настроен успешно!")
        print(f"   Bucket: {BUCKET_NAME}")
        print(f"   Public URL: {SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/")
        print(f"   Пример: {SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/artists/Чучундра/avatar.png")
    else:
        print("❌ Не удалось создать bucket")

if __name__ == "__main__":
    main()