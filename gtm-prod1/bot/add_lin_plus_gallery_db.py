#!/usr/bin/env python3
"""
Добавление записей галереи Lin++ в таблицу artist_gallery
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

def add_lin_plus_gallery():
    """Добавление галереи для артиста Lin++ (ID=7)"""
    artist_id = 7  # ID артиста Lin++
    
    gallery_items = []
    
    # Создаем записи для 8 изображений галереи
    for i in range(1, 9):
        gallery_item = {
            "artist_id": artist_id,
            "image_url": f"https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets-public/artists/Lin++/gallery{i}.jpg",
            "title": f"Работа {i}"
        }
        gallery_items.append(gallery_item)
    
    print(f"🖼️ Добавляем {len(gallery_items)} записей галереи для Lin++...")
    
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

def check_existing_gallery():
    """Проверка существующей галереи для Lin++"""
    print("🔍 Проверка существующей галереи для Lin++...")
    
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/artist_gallery?artist_id=eq.7",
        headers=headers
    )
    
    if response.status_code == 200:
        existing_gallery = response.json()
        if existing_gallery:
            print(f"⚠️ Найдено {len(existing_gallery)} существующих записей галереи")
            return existing_gallery
        else:
            print("✅ Существующих записей галереи не найдено")
            return []
    else:
        print(f"❌ Ошибка проверки галереи: {response.status_code}")
        return []

def main():
    print("🖼️ Добавление галереи Lin++ в базу данных")
    print("=" * 50)
    
    # Проверяем существующую галерею
    existing_gallery = check_existing_gallery()
    
    if existing_gallery:
        print(f"\n⚠️ У Lin++ уже есть {len(existing_gallery)} записей в галерее")
        print("Хотите продолжить и добавить новые записи? (y/n): ", end="")
        # Для автоматизации продолжаем
        print("y")
    
    # Добавляем галерею
    gallery = add_lin_plus_gallery()
    
    if gallery:
        print(f"\n✅ Галерея Lin++ успешно добавлена!")
        print(f"   Добавлено записей: {len(gallery)}")
        
        # Показываем добавленные записи
        print("\n📋 Добавленные записи:")
        for i, item in enumerate(gallery, 1):
            print(f"   {i}. {item.get('title', 'Без названия')} - {item.get('image_url', 'Нет URL')}")
    else:
        print("\n❌ Не удалось добавить галерею в базу данных")

if __name__ == "__main__":
    main() 