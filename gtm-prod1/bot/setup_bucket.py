#!/usr/bin/env python3
"""
GTM Supabase Bucket Setup
Настройка бакета как публичного в Supabase Storage
"""
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# Конфигурация
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
SUPABASE_STORAGE_BUCKET = os.getenv('SUPABASE_STORAGE_BUCKET', 'gtm-assets')

def setup_public_bucket():
    print("🔧 Настройка публичного бакета в Supabase...")
    print(f"URL: {SUPABASE_URL}")
    print(f"Bucket: {SUPABASE_STORAGE_BUCKET}")
    
    # Headers для service role (нужен для управления storage)
    service_headers = {
        'apikey': SUPABASE_SERVICE_ROLE_KEY,
        'Authorization': f'Bearer {SUPABASE_SERVICE_ROLE_KEY}',
        'Content-Type': 'application/json'
    }
    
    # Шаг 1: Проверяем текущее состояние бакета
    print(f"\n📋 Шаг 1: Проверка текущего состояния бакета '{SUPABASE_STORAGE_BUCKET}'")
    try:
        response = requests.get(f'{SUPABASE_URL}/storage/v1/bucket/{SUPABASE_STORAGE_BUCKET}', headers=service_headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            bucket_info = response.json()
            print(f"✅ Бакет найден: {bucket_info.get('name')}")
            print(f"  Public: {bucket_info.get('public')}")
            print(f"  Created: {bucket_info.get('created_at')}")
            
            if bucket_info.get('public'):
                print("✅ Бакет уже публичный!")
                return True
            else:
                print("❌ Бакет не публичный, нужно настроить...")
        else:
            print(f"❌ Бакет не найден: {response.text[:200]}...")
            return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False
    
    # Шаг 2: Делаем бакет публичным
    print(f"\n🔓 Шаг 2: Настройка бакета как публичного")
    try:
        update_data = {
            'public': True
        }
        
        response = requests.patch(
            f'{SUPABASE_URL}/storage/v1/bucket/{SUPABASE_STORAGE_BUCKET}',
            headers=service_headers,
            json=update_data
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Бакет успешно настроен как публичный!")
        else:
            print(f"❌ Ошибка настройки: {response.text[:200]}...")
            return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False
    
    # Шаг 3: Проверяем результат
    print(f"\n✅ Шаг 3: Проверка результата")
    try:
        response = requests.get(f'{SUPABASE_URL}/storage/v1/bucket/{SUPABASE_STORAGE_BUCKET}', headers=service_headers)
        if response.status_code == 200:
            bucket_info = response.json()
            print(f"✅ Бакет: {bucket_info.get('name')}")
            print(f"✅ Public: {bucket_info.get('public')}")
            if bucket_info.get('public'):
                print("🎉 Бакет успешно настроен как публичный!")
                return True
        else:
            print(f"❌ Ошибка проверки: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    return False

def test_public_access():
    """Тест публичного доступа к файлам"""
    print(f"\n🌐 Тест публичного доступа к файлам")
    
    # Headers для anon key (для публичного доступа)
    anon_headers = {
        'apikey': os.getenv('SUPABASE_ANON_KEY'),
        'Authorization': f'Bearer {os.getenv("SUPABASE_ANON_KEY")}',
        'Content-Type': 'application/json'
    }
    
    # Тестируем доступ к тестовому файлу
    test_file_url = f'{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_STORAGE_BUCKET}/test.txt'
    print(f"Тестируем URL: {test_file_url}")
    
    try:
        response = requests.get(test_file_url, headers=anon_headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Файл доступен публично!")
            return True
        else:
            print(f"❌ Файл недоступен: {response.text[:100]}...")
            return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Настройка публичного бакета Supabase")
    print("=" * 50)
    
    if setup_public_bucket():
        print("\n✅ Настройка завершена успешно!")
        test_public_access()
    else:
        print("\n❌ Настройка не удалась!") 