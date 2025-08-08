#!/usr/bin/env python3
"""
Добавление галереи для артиста Чучундра
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

def add_gallery():
    """Добавление галереи для артиста Чучундра (ID=2)"""
    artist_id = 2  # ID артиста Чучундра
    
    gallery_items = []
    
    for i in range(1, 11):  # 10 изображений
        gallery_item = {
            "artist_id": artist_id,
            "image_url": f"https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets-public/artists/Чучундра/gallery{i}.jpg",
            "title": f"Работа {i}"
        }
        gallery_items.append(gallery_item)
    
    # Добавляем галерею
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/artist_gallery",
        headers=headers,
        json=gallery_items
    )
    
    if response.status_code == 201:
        gallery = response.json()
        print(f"✅ Галерея добавлена: {len(gallery)} изображений")
        return gallery
    else:
        print(f"❌ Ошибка добавления галереи: {response.status_code}")
        print(f"   Ответ: {response.text}")
        return None

def main():
    print("🖼️ Добавление галереи для артиста 'Чучундра'")
    print("=" * 40)
    
    gallery = add_gallery()
    
    if gallery:
        print(f"✅ Галерея успешно добавлена: {len(gallery)} изображений")
    else:
        print("❌ Не удалось добавить галерею")

if __name__ == "__main__":
    main()