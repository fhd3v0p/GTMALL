#!/usr/bin/env python3
"""
Переименование файлов Lin++ в Storage с Lin++ на 7
"""

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# Конфигурация
SUPABASE_URL = "https://rxmtovqxjsvogyywyrha.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1Mjg1NTAsImV4cCI6MjA3MDEwNDU1MH0.gDkJybktFoi486hbIVwppDfmVQlAR0fM4o4Sl1-AxhE"
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

# Headers
service_headers = {
    'apikey': SUPABASE_SERVICE_ROLE_KEY,
    'Authorization': f'Bearer {SUPABASE_SERVICE_ROLE_KEY}',
    'Content-Type': 'application/json'
}

def copy_file_in_storage(old_path, new_path):
    """Копирование файла в Storage"""
    print(f"📋 Копируем: {old_path} → {new_path}")
    
    try:
        # Сначала получаем файл
        get_url = f'{SUPABASE_URL}/storage/v1/object/gtm-assets-public/{old_path}'
        response = requests.get(get_url, headers=service_headers)
        
        if response.status_code == 200:
            # Загружаем файл в новое место
            upload_url = f'{SUPABASE_URL}/storage/v1/object/gtm-assets-public/{new_path}'
            files_data = {'file': (new_path.split('/')[-1], response.content, 'image/jpeg')}
            
            upload_response = requests.post(upload_url, headers=service_headers, files=files_data)
            
            if upload_response.status_code == 200:
                print(f"  ✅ Успешно скопирован")
                return True
            else:
                print(f"  ❌ Ошибка загрузки: {upload_response.status_code} - {upload_response.text[:100]}...")
                return False
        else:
            print(f"  ❌ Ошибка получения: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Ошибка: {e}")
        return False

def delete_file_in_storage(path):
    """Удаление файла из Storage"""
    print(f"🗑️ Удаляем: {path}")
    
    try:
        delete_url = f'{SUPABASE_URL}/storage/v1/object/gtm-assets-public/{path}'
        response = requests.delete(delete_url, headers=service_headers)
        
        if response.status_code == 200:
            print(f"  ✅ Успешно удален")
            return True
        else:
            print(f"  ❌ Ошибка удаления: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Ошибка: {e}")
        return False

def fix_lin_plus_storage():
    """Переименование файлов Lin++ в Storage"""
    print("🔧 Переименование файлов Lin++ в Storage")
    print("=" * 50)
    
    # Список файлов для копирования
    files_to_copy = [
        ("artists/Lin++/avatar.png", "artists/7/avatar.png"),
        ("artists/Lin++/gallery1.jpg", "artists/7/gallery1.jpg"),
        ("artists/Lin++/gallery2.jpg", "artists/7/gallery2.jpg"),
        ("artists/Lin++/gallery3.jpg", "artists/7/gallery3.jpg"),
        ("artists/Lin++/gallery4.jpg", "artists/7/gallery4.jpg"),
        ("artists/Lin++/gallery5.jpg", "artists/7/gallery5.jpg"),
        ("artists/Lin++/gallery6.jpg", "artists/7/gallery6.jpg"),
        ("artists/Lin++/gallery7.jpg", "artists/7/gallery7.jpg"),
        ("artists/Lin++/gallery8.jpg", "artists/7/gallery8.jpg"),
    ]
    
    copied_count = 0
    total_count = len(files_to_copy)
    
    # Копируем файлы
    for old_path, new_path in files_to_copy:
        if copy_file_in_storage(old_path, new_path):
            copied_count += 1
    
    print(f"\n📊 Скопировано файлов: {copied_count}/{total_count}")
    
    if copied_count == total_count:
        print("\n🗑️ Удаляем старые файлы...")
        deleted_count = 0
        
        for old_path, _ in files_to_copy:
            if delete_file_in_storage(old_path):
                deleted_count += 1
        
        print(f"📊 Удалено файлов: {deleted_count}/{total_count}")
        
        if deleted_count == total_count:
            print("\n✅ Переименование завершено успешно!")
            print("   Теперь файлы доступны по пути artists/7/")
            return True
        else:
            print("\n⚠️ Не все старые файлы удалены")
            return False
    else:
        print("\n❌ Не все файлы скопированы")
        return False

def main():
    print("🔄 Исправление Storage для Lin++")
    print("=" * 50)
    
    success = fix_lin_plus_storage()
    
    if success:
        print("\n✅ Storage исправлен! Галерея Lin++ должна отображаться корректно.")
    else:
        print("\n❌ Не удалось исправить Storage")

if __name__ == "__main__":
    main() 