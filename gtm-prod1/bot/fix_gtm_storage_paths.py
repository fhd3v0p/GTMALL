#!/usr/bin/env python3
"""
Исправление путей к файлам GTM - копирование из artists/GTM/ в artists/14/
"""
import requests
import json

# Supabase Configuration
SUPABASE_URL = 'https://rxmtovqxjsvogyywyrha.supabase.co'
SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1Mjg1NTAsImV4cCI6MjA3MDEwNDU1MH0.gDkJybktFoi486hbIVwppDfmVQlAR0fM4o4Sl1-AxhE'

def copy_gtm_files():
    """Копирование файлов GTM из artists/GTM/ в artists/14/"""
    print("🔧 Копирование файлов GTM...")
    
    # Список файлов для копирования
    files_to_copy = [
        'avatar.png',
        'gallery1.jpg',
        'gallery2.jpg',
        'gallery3.jpg'
    ]
    
    copied_files = []
    
    for filename in files_to_copy:
        try:
            # URL исходного файла
            source_url = f'{SUPABASE_URL}/storage/v1/object/public/gtm-assets-public/artists/GTM/{filename}'
            
            # Скачиваем файл
            response = requests.get(source_url)
            if response.status_code == 200:
                file_data = response.content
                
                # Загружаем в новое место
                upload_url = f'{SUPABASE_URL}/storage/v1/object/gtm-assets-public/artists/14/{filename}'
                headers = {
                    'apikey': SUPABASE_ANON_KEY,
                    'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
                    'Content-Type': 'image/jpeg' if filename.endswith('.jpg') else 'image/png'
                }
                
                upload_response = requests.post(upload_url, headers=headers, data=file_data)
                
                if upload_response.status_code == 200:
                    print(f"✅ Скопирован: {filename}")
                    copied_files.append(filename)
                else:
                    print(f"❌ Ошибка загрузки {filename}: {upload_response.status_code}")
            else:
                print(f"❌ Файл {filename} не найден в artists/GTM/")
                
        except Exception as e:
            print(f"❌ Ошибка при копировании {filename}: {e}")
    
    return copied_files

def update_avatar_url():
    """Обновление avatar_url в базе данных"""
    print("\n🔧 Обновление avatar_url в базе данных...")
    
    url = f'{SUPABASE_URL}/rest/v1/artists'
    headers = {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal'
    }
    
    # Новый avatar_url
    new_avatar_url = f'{SUPABASE_URL}/storage/v1/object/public/gtm-assets-public/artists/14/avatar.png'
    
    data = {
        'avatar_url': new_avatar_url
    }
    
    params = {
        'id': 'eq.14'
    }
    
    try:
        response = requests.patch(url, headers=headers, params=params, json=data)
        response.raise_for_status()
        
        print("✅ Avatar URL обновлен в базе данных")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка обновления avatar_url: {e}")
        return False

def delete_old_gtm_files():
    """Удаление старых файлов из artists/GTM/"""
    print("\n🗑️ Удаление старых файлов из artists/GTM/...")
    
    files_to_delete = [
        'avatar.png',
        'gallery1.jpg',
        'gallery2.jpg',
        'gallery3.jpg'
    ]
    
    deleted_files = []
    
    for filename in files_to_delete:
        try:
            delete_url = f'{SUPABASE_URL}/storage/v1/object/gtm-assets-public/artists/GTM/{filename}'
            headers = {
                'apikey': SUPABASE_ANON_KEY,
                'Authorization': f'Bearer {SUPABASE_ANON_KEY}'
            }
            
            response = requests.delete(delete_url, headers=headers)
            
            if response.status_code == 200:
                print(f"✅ Удален: {filename}")
                deleted_files.append(filename)
            else:
                print(f"❌ Ошибка удаления {filename}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Ошибка при удалении {filename}: {e}")
    
    return deleted_files

if __name__ == "__main__":
    print("🔧 Исправление путей к файлам GTM")
    print("=" * 50)
    
    # 1. Копируем файлы
    copied_files = copy_gtm_files()
    
    # 2. Обновляем avatar_url в базе
    if copied_files:
        update_avatar_url()
        
        # 3. Удаляем старые файлы
        delete_old_gtm_files()
        
        print("\n✅ Исправление завершено!")
        print(f"📁 Скопировано файлов: {len(copied_files)}")
        print("🔗 Новый путь: artists/14/")
    else:
        print("\n❌ Не удалось скопировать файлы") 