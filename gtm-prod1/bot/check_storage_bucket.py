#!/usr/bin/env python3
"""
Проверка Supabase Storage bucket gtm-assets-public
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

def check_bucket_exists():
    """Проверка существования bucket"""
    try:
        response = requests.get(
            f"{SUPABASE_URL}/storage/v1/bucket",
            headers=headers
        )
        
        if response.status_code == 200:
            buckets = response.json()
            print(f"✅ Найдено buckets: {len(buckets)}")
            
            for bucket in buckets:
                print(f"   - {bucket['name']} (public: {bucket.get('public', False)})")
                if bucket['name'] == BUCKET_NAME:
                    print(f"     ✅ Bucket {BUCKET_NAME} найден!")
                    return bucket
            
            print(f"❌ Bucket {BUCKET_NAME} не найден")
            return None
        else:
            print(f"❌ Ошибка получения buckets: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Исключение при проверке buckets: {e}")
        return None

def list_bucket_contents(path=""):
    """Список файлов в bucket"""
    try:
        url = f"{SUPABASE_URL}/storage/v1/object/list/{BUCKET_NAME}"
        if path:
            url += f"?prefix={path}/"
        
        response = requests.post(
            url,
            headers=headers,
            json={"limit": 100, "offset": 0, "sortBy": {"column": "name", "order": "asc"}}
        )
        
        if response.status_code == 200:
            files = response.json()
            print(f"📁 Содержимое {BUCKET_NAME}/{path}: {len(files)} элементов")
            
            for file in files[:10]:  # Показываем первые 10
                print(f"   - {file['name']} ({file.get('metadata', {}).get('size', 'N/A')} bytes)")
                
            if len(files) > 10:
                print(f"   ... и еще {len(files) - 10} файлов")
                
            return files
        else:
            print(f"❌ Ошибка получения содержимого: {response.status_code}")
            print(f"   Ответ: {response.text}")
            return []
    except Exception as e:
        print(f"❌ Исключение при получении содержимого: {e}")
        return []

def check_chchundra_folder():
    """Проверка папки Чучундра"""
    print("\n🔍 Проверка папки artists/Чучундра...")
    
    # Проверяем папку artists
    artists_files = list_bucket_contents("artists")
    
    # Ищем папку Чучундра
    chchundra_found = False
    for file in artists_files:
        if "Чучундра" in file['name'] or "chchundra" in file['name'].lower():
            chchundra_found = True
            print(f"   ✅ Найден: {file['name']}")
    
    if not chchundra_found:
        print("   ❌ Папка Чучундра не найдена")
        print("   💡 Нужно создать папку artists/Чучундра/ и загрузить файлы")
        
    return chchundra_found

def test_public_url():
    """Тест публичного URL"""
    test_url = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/artists/Чучундра/avatar.png"
    
    try:
        response = requests.head(test_url)
        print(f"\n🌐 Тест публичного URL:")
        print(f"   URL: {test_url}")
        print(f"   Статус: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Публичный доступ работает!")
            return True
        else:
            print("   ❌ Файл не найден или нет доступа")
            return False
    except Exception as e:
        print(f"   ❌ Ошибка тестирования URL: {e}")
        return False

def main():
    print("🪣 Проверка Supabase Storage")
    print("=" * 40)
    
    # Проверяем bucket
    bucket = check_bucket_exists()
    
    if bucket:
        print(f"\n📋 Детали bucket {BUCKET_NAME}:")
        print(f"   ID: {bucket.get('id')}")
        print(f"   Public: {bucket.get('public', False)}")
        print(f"   Created: {bucket.get('created_at', 'N/A')}")
        
        # Проверяем содержимое
        print(f"\n📂 Содержимое bucket:")
        list_bucket_contents()
        
        # Проверяем папку Чучундра
        check_chchundra_folder()
        
        # Тестируем публичный URL
        test_public_url()
        
    else:
        print(f"\n❌ Bucket {BUCKET_NAME} не найден или недоступен")
        print("💡 Возможные причины:")
        print("   - Bucket не создан")
        print("   - Нет прав доступа")
        print("   - Неправильное имя bucket")

if __name__ == "__main__":
    main()