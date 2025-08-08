#!/usr/bin/env python3
"""
Обновление URL галереи Lin++ на новые пути artists/7/
"""

import requests
import json

# Конфигурация
SUPABASE_URL = "https://rxmtovqxjsvogyywyrha.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1Mjg1NTAsImV4cCI6MjA3MDEwNDU1MH0.gDkJybktFoi486hbIVwppDfmVQlAR0fM4o4Sl1-AxhE"

headers = {
    'apikey': SUPABASE_ANON_KEY,
    'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
    'Content-Type': 'application/json',
    'Prefer': 'return=representation'
}

def update_lin_plus_gallery_urls():
    """Обновление URL галереи Lin++ на новые пути"""
    artist_id = 7  # ID артиста Lin++
    
    print("🔄 Обновление URL галереи Lin++")
    print("=" * 50)
    
    # Получаем текущие записи галереи
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/artist_gallery?artist_id=eq.7",
        headers=headers
    )
    
    if response.status_code != 200:
        print(f"❌ Ошибка получения галереи: {response.status_code}")
        return False
    
    gallery_items = response.json()
    print(f"📋 Найдено {len(gallery_items)} записей галереи")
    
    if not gallery_items:
        print("❌ Записи галереи не найдены")
        return False
    
    # Обновляем URL для каждой записи
    updated_count = 0
    for item in gallery_items:
        item_id = item['id']
        old_url = item['image_url']
        
        # Заменяем Lin++ на 7 в URL
        new_url = old_url.replace('artists/Lin++/', 'artists/7/')
        
        if new_url != old_url:
            print(f"🔄 Обновляем запись {item_id}: {old_url} → {new_url}")
            
            update_response = requests.patch(
                f"{SUPABASE_URL}/rest/v1/artist_gallery?id=eq.{item_id}",
                headers=headers,
                json={'image_url': new_url}
            )
            
            if update_response.status_code == 200:
                print(f"  ✅ Успешно обновлен")
                updated_count += 1
            else:
                print(f"  ❌ Ошибка обновления: {update_response.status_code}")
        else:
            print(f"⏭️ Пропускаем запись {item_id} (URL уже правильный)")
    
    print(f"\n📊 Обновлено записей: {updated_count}/{len(gallery_items)}")
    
    if updated_count > 0:
        print("\n✅ URL галереи обновлены!")
        return True
    else:
        print("\n⚠️ Нечего обновлять")
        return True

def verify_gallery_urls():
    """Проверка доступности новых URL"""
    print("\n🔍 Проверка доступности новых URL...")
    
    for i in range(1, 9):
        url = f"https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets-public/artists/7/gallery{i}.jpg"
        
        response = requests.head(url)
        if response.status_code == 200:
            print(f"  ✅ gallery{i}.jpg доступен")
        else:
            print(f"  ❌ gallery{i}.jpg недоступен (код: {response.status_code})")

def main():
    print("🔄 Обновление галереи Lin++")
    print("=" * 50)
    
    success = update_lin_plus_gallery_urls()
    
    if success:
        verify_gallery_urls()
        print("\n✅ Галерея Lin++ обновлена! Теперь должна отображаться корректно.")
    else:
        print("\n❌ Не удалось обновить галерею")

if __name__ == "__main__":
    main() 