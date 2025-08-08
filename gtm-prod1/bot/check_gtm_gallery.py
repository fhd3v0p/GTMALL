#!/usr/bin/env python3
"""
Проверка и исправление записей галереи GTM в таблице artist_gallery
"""
import requests
import json

# Supabase Configuration
SUPABASE_URL = 'https://rxmtovqxjsvogyywyrha.supabase.co'
SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1Mjg1NTAsImV4cCI6MjA3MDEwNDU1MH0.gDkJybktFoi486hbIVwppDfmVQlAR0fM4o4Sl1-AxhE'

def check_gtm_gallery():
    """Проверка записей галереи GTM"""
    print("🔍 Проверка записей галереи GTM...")
    
    url = f'{SUPABASE_URL}/rest/v1/artist_gallery'
    headers = {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
        'Content-Type': 'application/json'
    }
    
    params = {
        'artist_id': 'eq.14',
        'select': 'id,artist_id,image_url'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        if data:
            print(f"📋 Найдено записей в artist_gallery для GTM: {len(data)}")
            for record in data:
                print(f"   ID: {record['id']}, URL: {record['image_url']}")
            return data
        else:
            print("❌ Записей в artist_gallery для GTM не найдено")
            return []
            
    except Exception as e:
        print(f"❌ Ошибка при проверке artist_gallery: {e}")
        return []

def add_gtm_gallery_entries():
    """Добавление записей галереи GTM"""
    print("\n🔧 Добавление записей галереи GTM...")
    
    url = f'{SUPABASE_URL}/rest/v1/artist_gallery'
    headers = {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
        'Content-Type': 'application/json'
    }
    
    # Создаем записи для галереи GTM
    gallery_items = []
    for i in range(1, 4):  # gallery1.jpg - gallery3.jpg
        item = {
            'artist_id': 14,
            'image_url': f'{SUPABASE_URL}/storage/v1/object/public/gtm-assets-public/artists/14/gallery{i}.jpg'
        }
        gallery_items.append(item)
    
    try:
        response = requests.post(url, headers=headers, json=gallery_items)
        response.raise_for_status()
        
        print("✅ Записи галереи GTM добавлены")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка добавления записей галереи: {e}")
        return False

def update_gtm_gallery_urls():
    """Обновление URL в существующих записях галереи GTM"""
    print("\n🔧 Обновление URL в записях галереи GTM...")
    
    # Сначала получаем существующие записи
    existing_records = check_gtm_gallery()
    
    if not existing_records:
        print("❌ Нет записей для обновления")
        return False
    
    url = f'{SUPABASE_URL}/rest/v1/artist_gallery'
    headers = {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
        'Content-Type': 'application/json'
    }
    
    updated_count = 0
    
    for record in existing_records:
        try:
            # Определяем номер изображения из URL
            old_url = record['image_url']
            if 'gallery' in old_url:
                # Извлекаем номер из старого URL
                if 'gallery1' in old_url:
                    new_url = f'{SUPABASE_URL}/storage/v1/object/public/gtm-assets-public/artists/14/gallery1.jpg'
                elif 'gallery2' in old_url:
                    new_url = f'{SUPABASE_URL}/storage/v1/object/public/gtm-assets-public/artists/14/gallery2.jpg'
                elif 'gallery3' in old_url:
                    new_url = f'{SUPABASE_URL}/storage/v1/object/public/gtm-assets-public/artists/14/gallery3.jpg'
                else:
                    continue
                
                # Обновляем запись
                update_url = f'{url}?id=eq.{record["id"]}'
                data = {'image_url': new_url}
                
                response = requests.patch(update_url, headers=headers, json=data)
                if response.status_code == 200:
                    print(f"✅ Обновлен URL: {old_url} -> {new_url}")
                    updated_count += 1
                else:
                    print(f"❌ Ошибка обновления записи {record['id']}")
                    
        except Exception as e:
            print(f"❌ Ошибка при обновлении записи {record['id']}: {e}")
    
    print(f"📊 Обновлено записей: {updated_count}")
    return updated_count > 0

if __name__ == "__main__":
    print("🔧 Проверка и исправление галереи GTM")
    print("=" * 50)
    
    # Проверяем существующие записи
    existing_records = check_gtm_gallery()
    
    if existing_records:
        # Обновляем существующие записи
        update_gtm_gallery_urls()
    else:
        # Добавляем новые записи
        add_gtm_gallery_entries()
    
    # Проверяем результат
    print("\n🔍 Проверка результата...")
    check_gtm_gallery()
    
    print("\n✅ Обработка галереи GTM завершена!") 