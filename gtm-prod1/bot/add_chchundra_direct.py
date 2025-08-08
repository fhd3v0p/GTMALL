#!/usr/bin/env python3
"""
Прямое добавление артиста Чучундра через API Supabase
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

def get_city_id(city_name):
    """Получение ID города"""
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/cities?select=id&name=eq.{city_name}",
        headers=headers
    )
    if response.status_code == 200:
        data = response.json()
        return data[0]['id'] if data else None
    return None

def get_category_id(category_name):
    """Получение ID категории"""
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/categories?select=id&name=eq.{category_name}",
        headers=headers
    )
    if response.status_code == 200:
        data = response.json()
        return data[0]['id'] if data else None
    return None

def add_artist():
    """Добавление артиста Чучундра"""
    
    # Получаем ID города и категории
    moscow_id = get_city_id("Москва")
    tattoo_id = get_category_id("Tattoo")
    
    if not moscow_id or not tattoo_id:
        print(f"❌ Не найдены ID: moscow_id={moscow_id}, tattoo_id={tattoo_id}")
        return None
    
    print(f"✅ ID найдены: Москва={moscow_id}, Tattoo={tattoo_id}")
    
    # Данные артиста (используем существующую структуру таблицы)
    artist_data = {
        "name": "Чучундра",
        "username": "chchundra_tattoo",
        "bio": "Профессиональный тату-мастер с уникальным стилем. Специализируется на черно-белых работах и минимализме.",
        "avatar_url": "https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets-public/artists/Чучундра/avatar.png",
        "city": "Москва",
        "specialties": ["Черно-белые тату", "Минимализм", "Графика", "Дотворк"],
        "rating": 4.8,
        "telegram": "@chchndra_tattoo",
        "tiktok": "@chchundra_art",
        "is_active": True
    }
    
    # Добавляем артиста
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/artists",
        headers=headers,
        json=artist_data
    )
    
    if response.status_code == 201:
        artist = response.json()[0]
        print(f"✅ Артист добавлен: ID={artist['id']}, имя='{artist['name']}'")
        return artist
    else:
        print(f"❌ Ошибка добавления артиста: {response.status_code}")
        print(f"   Ответ: {response.text}")
        return None

def add_gallery(artist_id):
    """Добавление галереи для артиста"""
    gallery_items = []
    
    for i in range(1, 11):  # 10 изображений
        gallery_item = {
            "artist_id": artist_id,
            "image_url": f"https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets-public/artists/Чучундра/gallery{i}.jpg",
            "title": f"Работа {i}",
            "display_order": i
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
    """Главная функция"""
    print("🎨 Добавление артиста 'Чучундра' в систему GTM")
    print("=" * 50)
    
    # Добавляем артиста
    artist = add_artist()
    if not artist:
        return
    
    # Добавляем галерею
    gallery = add_gallery(artist['id'])
    
    print("\n✅ Артист 'Чучундра' успешно добавлен в систему!")
    print(f"   ID: {artist['id']}")
    print(f"   Имя: {artist['name']}")
    print(f"   Галерея: {len(gallery) if gallery else 0} изображений")

if __name__ == "__main__":
    main()