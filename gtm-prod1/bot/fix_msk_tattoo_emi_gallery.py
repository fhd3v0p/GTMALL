#!/usr/bin/env python3
"""
Исправление URL галереи msk_tattoo_EMI с относительных путей на полные URL
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

def fix_msk_tattoo_emi_gallery_urls():
    """Обновление URL галереи msk_tattoo_EMI на полные URL с бакетом"""
    
    print("🔄 Обновление URL галереи msk_tattoo_EMI")
    print("=" * 50)
    
    # Получаем записи с относительными путями msk_tattoo_EMI
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/artist_gallery?image_url=like.*msk_tattoo_EMI*",
        headers=headers
    )
    
    if response.status_code != 200:
        print(f"❌ Ошибка получения галереи: {response.status_code}")
        return False
    
    gallery_items = response.json()
    print(f"📋 Найдено {len(gallery_items)} записей галереи msk_tattoo_EMI")
    
    if not gallery_items:
        print("❌ Записи галереи не найдены")
        return False
    
    # Обновляем URL для каждой записи
    updated_count = 0
    for item in gallery_items:
        item_id = item['id']
        old_url = item['image_url']
        
        # Проверяем, что это относительный путь
        if old_url.startswith('/assets/artists/msk_tattoo_EMI/'):
            # Заменяем на полный URL с бакетом
            new_url = old_url.replace('/assets/artists/msk_tattoo_EMI/', 'https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets-public/artists/msk_tattoo_EMI/')
            
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
            print(f"⏭️ Пропускаем запись {item_id} (уже полный URL)")
    
    print(f"\n📊 Обновлено записей: {updated_count}/{len(gallery_items)}")
    
    if updated_count > 0:
        print("\n✅ URL галереи msk_tattoo_EMI обновлены!")
        return True
    else:
        print("\n⚠️ Нечего обновлять")
        return True

def check_msk_tattoo_emi_gallery_after_update():
    """Проверка галереи msk_tattoo_EMI после обновления"""
    print("\n🔍 Проверка галереи msk_tattoo_EMI после обновления...")
    
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/artist_gallery?image_url=like.*msk_tattoo_EMI*&select=id,title,image_url",
        headers=headers
    )
    
    if response.status_code == 200:
        gallery_items = response.json()
        print(f"📋 Найдено {len(gallery_items)} записей галереи msk_tattoo_EMI:")
        
        for item in gallery_items:
            print(f"  - {item.get('title', 'Без названия')}: {item.get('image_url', 'Нет URL')}")
        
        return True
    else:
        print(f"❌ Ошибка проверки галереи: {response.status_code}")
        return False

def main():
    print("🔄 Исправление галереи msk_tattoo_EMI")
    print("=" * 50)
    
    # Обновляем URL галереи
    if fix_msk_tattoo_emi_gallery_urls():
        print("\n✅ Галерея msk_tattoo_EMI обновлена!")
        
        # Проверяем результат
        check_msk_tattoo_emi_gallery_after_update()
    else:
        print("\n❌ Не удалось обновить галерею msk_tattoo_EMI")

if __name__ == "__main__":
    main() 