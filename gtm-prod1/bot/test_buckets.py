#!/usr/bin/env python3
"""
GTM Supabase Bucket Test
Детальное тестирование бакетов Supabase Storage
"""
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# Конфигурация
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
SUPABASE_STORAGE_BUCKET = os.getenv('SUPABASE_STORAGE_BUCKET', 'gtm-assets')

def test_supabase_buckets():
    print("🔍 Тестирование Supabase Storage Buckets...")
    print(f"URL: {SUPABASE_URL}")
    print(f"Bucket: {SUPABASE_STORAGE_BUCKET}")
    
    # Headers для service role (нужен для управления storage)
    service_headers = {
        'apikey': SUPABASE_SERVICE_ROLE_KEY,
        'Authorization': f'Bearer {SUPABASE_SERVICE_ROLE_KEY}',
        'Content-Type': 'application/json'
    }
    
    # Headers для anon key (для публичного доступа)
    anon_headers = {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
        'Content-Type': 'application/json'
    }
    
    # Тест 1: Список всех бакетов
    print("\n📦 Тест 1: Список всех бакетов")
    try:
        response = requests.get(f'{SUPABASE_URL}/storage/v1/bucket/list', headers=service_headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            buckets = response.json()
            print(f"Найдено бакетов: {len(buckets)}")
            for bucket in buckets:
                print(f"  - {bucket.get('name')} (public: {bucket.get('public')})")
        else:
            print(f"Response: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    # Тест 2: Проверка конкретного бакета
    print(f"\n🔍 Тест 2: Проверка бакета '{SUPABASE_STORAGE_BUCKET}'")
    try:
        response = requests.get(f'{SUPABASE_URL}/storage/v1/bucket/{SUPABASE_STORAGE_BUCKET}', headers=service_headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            bucket_info = response.json()
            print(f"✅ Бакет найден: {bucket_info.get('name')}")
            print(f"  Public: {bucket_info.get('public')}")
            print(f"  Created: {bucket_info.get('created_at')}")
        else:
            print(f"Response: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    # Тест 3: Список файлов в бакете
    print(f"\n📁 Тест 3: Список файлов в бакете '{SUPABASE_STORAGE_BUCKET}'")
    try:
        response = requests.get(f'{SUPABASE_URL}/storage/v1/object/list/{SUPABASE_STORAGE_BUCKET}', headers=service_headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            files = response.json()
            print(f"Найдено файлов: {len(files)}")
            for file in files[:5]:  # Показываем первые 5 файлов
                print(f"  - {file.get('name')} ({file.get('size')} bytes)")
        else:
            print(f"Response: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    # Тест 4: Проверка публичного доступа к файлу
    print(f"\n🌐 Тест 4: Публичный доступ к файлу")
    try:
        # Пробуем получить URL файла
        test_file_url = f'{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_STORAGE_BUCKET}/banners/city_selection_banner.png'
        print(f"Тестируем URL: {test_file_url}")
        
        response = requests.get(test_file_url, headers=anon_headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Файл доступен публично")
        else:
            print(f"❌ Файл недоступен: {response.text[:100]}...")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    # Тест 5: Создание тестового файла (если бакет существует)
    print(f"\n📝 Тест 5: Попытка создания тестового файла")
    try:
        test_content = "This is a test file for GTM project"
        files = {'file': ('test.txt', test_content, 'text/plain')}
        
        response = requests.post(
            f'{SUPABASE_URL}/storage/v1/object/{SUPABASE_STORAGE_BUCKET}/test.txt',
            headers=service_headers,
            files=files
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Тестовый файл создан")
        else:
            print(f"❌ Не удалось создать файл: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    test_supabase_buckets() 