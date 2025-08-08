#!/usr/bin/env python3
"""
Проверка файлов GTM в Supabase Storage
"""
import requests
import json

# Supabase Configuration
SUPABASE_URL = 'https://rxmtovqxjsvogyywyrha.supabase.co'
SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1Mjg1NTAsImV4cCI6MjA3MDEwNDU1MH0.gDkJybktFoi486hbIVwppDfmVQlAR0fM4o4Sl1-AxhE'

def check_gtm_files():
    """Проверка файлов GTM в Storage"""
    print("🔍 Проверка файлов GTM в Storage...")
    
    # Проверяем разные возможные пути
    paths_to_check = [
        'artists/GTM/',
        'artists/14/',
        'artists/gtm/',
        'artists/GTM_BRAND/'
    ]
    
    for path in paths_to_check:
        print(f"\n📁 Проверяем путь: {path}")
        
        # Список файлов для проверки
        files_to_check = [
            'avatar.png',
            'avatar.jpg',
            'gallery1.jpg',
            'gallery2.jpg',
            'gallery3.jpg'
        ]
        
        found_files = []
        
        for filename in files_to_check:
            try:
                url = f'{SUPABASE_URL}/storage/v1/object/public/gtm-assets-public/{path}{filename}'
                response = requests.head(url)
                
                if response.status_code == 200:
                    print(f"✅ Найден: {filename}")
                    found_files.append(filename)
                else:
                    print(f"❌ Не найден: {filename}")
                    
            except Exception as e:
                print(f"❌ Ошибка проверки {filename}: {e}")
        
        if found_files:
            print(f"📋 Найдено файлов в {path}: {len(found_files)}")
            return path, found_files
    
    return None, []

def check_artist_gallery_table():
    """Проверка записей в таблице artist_gallery для GTM"""
    print("\n🔍 Проверка записей в artist_gallery для GTM...")
    
    url = f'{SUPABASE_URL}/rest/v1/artist_gallery'
    headers = {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
        'Content-Type': 'application/json'
    }
    
    params = {
        'artist_id': 'eq.14',
        'select': 'id,artist_id,image_url,order_index'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        if data:
            print(f"📋 Найдено записей в artist_gallery для GTM: {len(data)}")
            for record in data:
                print(f"   ID: {record['id']}, URL: {record['image_url']}")
        else:
            print("❌ Записей в artist_gallery для GTM не найдено")
            
    except Exception as e:
        print(f"❌ Ошибка при проверке artist_gallery: {e}")

if __name__ == "__main__":
    print("🔍 Проверка файлов GTM в Supabase Storage")
    print("=" * 50)
    
    # Проверяем файлы в Storage
    path, files = check_gtm_files()
    
    # Проверяем записи в artist_gallery
    check_artist_gallery_table()
    
    if path and files:
        print(f"\n✅ Файлы GTM найдены в: {path}")
        print(f"📁 Файлы: {files}")
    else:
        print("\n❌ Файлы GTM не найдены в Storage") 