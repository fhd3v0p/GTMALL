#!/usr/bin/env python3
"""
GTM Supabase Bucket Fix
Исправление проблемы с бакетом через создание нового публичного бакета
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

def fix_bucket_issue():
    print("🔧 Исправление проблемы с бакетом Supabase...")
    print(f"URL: {SUPABASE_URL}")
    print(f"Bucket: {SUPABASE_STORAGE_BUCKET}")
    
    # Headers для service role
    service_headers = {
        'apikey': SUPABASE_SERVICE_ROLE_KEY,
        'Authorization': f'Bearer {SUPABASE_SERVICE_ROLE_KEY}',
        'Content-Type': 'application/json'
    }
    
    # Шаг 1: Проверяем текущий бакет
    print(f"\n📋 Шаг 1: Проверка текущего бакета '{SUPABASE_STORAGE_BUCKET}'")
    try:
        response = requests.get(f'{SUPABASE_URL}/storage/v1/bucket/{SUPABASE_STORAGE_BUCKET}', headers=service_headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            bucket_info = response.json()
            print(f"✅ Бакет найден: {bucket_info.get('name')}")
            print(f"  Public: {bucket_info.get('public')}")
            
            if bucket_info.get('public'):
                print("✅ Бакет уже публичный!")
                return True
            else:
                print("❌ Бакет не публичный")
        else:
            print(f"❌ Бакет не найден: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    # Шаг 2: Создаем новый публичный бакет
    print(f"\n🆕 Шаг 2: Создание нового публичного бакета")
    new_bucket_name = f"{SUPABASE_STORAGE_BUCKET}-public"
    
    try:
        create_data = {
            'name': new_bucket_name,
            'public': True
        }
        
        response = requests.post(
            f'{SUPABASE_URL}/storage/v1/bucket',
            headers=service_headers,
            json=create_data
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ Новый публичный бакет '{new_bucket_name}' создан!")
        else:
            print(f"❌ Ошибка создания: {response.text[:200]}...")
            return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False
    
    # Шаг 3: Копируем файлы из старого бакета в новый
    print(f"\n📁 Шаг 3: Копирование файлов в новый бакет")
    try:
        # Получаем список файлов из старого бакета
        response = requests.get(f'{SUPABASE_URL}/storage/v1/object/list/{SUPABASE_STORAGE_BUCKET}', headers=service_headers)
        if response.status_code == 200:
            files = response.json()
            print(f"Найдено файлов для копирования: {len(files)}")
            
            for file in files[:3]:  # Копируем первые 3 файла для теста
                file_name = file.get('name')
                print(f"  Копируем: {file_name}")
                
                # Скачиваем файл из старого бакета
                download_url = f'{SUPABASE_URL}/storage/v1/object/{SUPABASE_STORAGE_BUCKET}/{file_name}'
                file_response = requests.get(download_url, headers=service_headers)
                
                if file_response.status_code == 200:
                    # Загружаем файл в новый бакет
                    upload_url = f'{SUPABASE_URL}/storage/v1/object/{new_bucket_name}/{file_name}'
                    files_data = {'file': (file_name, file_response.content, 'application/octet-stream')}
                    
                    upload_response = requests.post(upload_url, headers=service_headers, files=files_data)
                    if upload_response.status_code == 200:
                        print(f"    ✅ {file_name} скопирован")
                    else:
                        print(f"    ❌ Ошибка копирования {file_name}")
                else:
                    print(f"    ❌ Не удалось скачать {file_name}")
        else:
            print(f"❌ Не удалось получить список файлов: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ Ошибка копирования: {e}")
    
    # Шаг 4: Обновляем конфигурацию
    print(f"\n⚙️ Шаг 4: Обновление конфигурации")
    print(f"Новый бакет: {new_bucket_name}")
    print(f"Обновите переменную SUPABASE_STORAGE_BUCKET в .env файле:")
    print(f"SUPABASE_STORAGE_BUCKET={new_bucket_name}")
    
    # Шаг 5: Тест нового бакета
    print(f"\n🧪 Шаг 5: Тест нового бакета")
    try:
        response = requests.get(f'{SUPABASE_URL}/storage/v1/bucket/{new_bucket_name}', headers=service_headers)
        if response.status_code == 200:
            bucket_info = response.json()
            print(f"✅ Новый бакет: {bucket_info.get('name')}")
            print(f"✅ Public: {bucket_info.get('public')}")
            
            if bucket_info.get('public'):
                print("🎉 Новый бакет успешно настроен как публичный!")
                return True
        else:
            print(f"❌ Ошибка проверки нового бакета: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    return False

def show_manual_instructions():
    """Показывает инструкции по ручной настройке"""
    print("\n📋 Инструкции по ручной настройке бакета:")
    print("=" * 50)
    print("1. Откройте Supabase Dashboard:")
    print(f"   https://supabase.com/dashboard/project/rxmtovqxjsvogyywyrha")
    print("\n2. Перейдите в Storage → Buckets")
    print("\n3. Найдите бакет 'gtm-assets'")
    print("\n4. Нажмите на бакет для редактирования")
    print("\n5. Включите опцию 'Public bucket'")
    print("\n6. Сохраните изменения")
    print("\n7. Загрузите файлы в бакет:")
    print("   - Перейдите в папку бакета")
    print("   - Нажмите 'Upload file'")
    print("   - Загрузите файлы из папки assets/")

if __name__ == "__main__":
    print("🚀 Исправление проблемы с бакетом Supabase")
    print("=" * 50)
    
    if fix_bucket_issue():
        print("\n✅ Проблема исправлена!")
    else:
        print("\n❌ Автоматическое исправление не удалось!")
        show_manual_instructions() 