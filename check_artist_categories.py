#!/usr/bin/env python3
"""
Скрипт для проверки связей артиста GTM с категориями
"""

import requests
import json

# Supabase Configuration
SUPABASE_URL = "https://rxmtovqxjsvogyywyrha.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1Mjg1NTAsImV4cCI6MjA3MDEwNDU1MH0.gDkJybktFoi486hbIVwppDfmVQlAR0fM4o4Sl1-AxhE"

# Headers for Supabase API
HEADERS = {
    'apikey': SUPABASE_ANON_KEY,
    'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
    'Content-Type': 'application/json',
}

def check_artist_categories(artist_id: int):
    """Проверяет связи артиста с категориями"""
    try:
        # Получаем артиста
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/artists?id=eq.{artist_id}",
            headers=HEADERS
        )
        
        if response.status_code == 200:
            artists = response.json()
            if artists:
                artist = artists[0]
                print(f"📋 Артист ID {artist_id}:")
                print(f"   Имя: {artist.get('name')}")
                print(f"   Специальности: {artist.get('specialties')}")
                print(f"   Города: {artist.get('city')}")
                print(f"   Активен: {artist.get('is_active')}")
                return artist
            else:
                print(f"❌ Артист с ID {artist_id} не найден")
                return None
        else:
            print(f"❌ Ошибка получения артиста: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка при проверке артиста: {e}")
        return None

def check_artist_categories_table(artist_id: int):
    """Проверяет таблицу artist_categories"""
    try:
        # Получаем связи артиста с категориями
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/artist_categories?artist_id=eq.{artist_id}",
            headers=HEADERS
        )
        
        if response.status_code == 200:
            categories = response.json()
            print(f"📋 Связи артиста {artist_id} с категориями:")
            for cat in categories:
                print(f"   - Категория ID: {cat.get('category_id')}")
            return categories
        else:
            print(f"❌ Ошибка получения связей: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Ошибка при проверке связей: {e}")
        return []

def check_all_categories():
    """Проверяет все категории"""
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/categories",
            headers=HEADERS
        )
        
        if response.status_code == 200:
            categories = response.json()
            print(f"📋 Все категории:")
            for cat in categories:
                print(f"   - ID {cat.get('id')}: {cat.get('name')} ({cat.get('type')})")
            return categories
        else:
            print(f"❌ Ошибка получения категорий: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Ошибка при получении категорий: {e}")
        return []

def main():
    """Основная функция"""
    print("🔍 Проверяем связи артиста GTM с категориями...")
    
    # Проверяем артиста GTM (ID 14)
    artist = check_artist_categories(14)
    
    if artist:
        print("\n📋 Проверяем таблицу artist_categories...")
        categories = check_artist_categories_table(14)
        
        print("\n📋 Проверяем все категории...")
        all_categories = check_all_categories()
        
        # Находим ID категории GTM BRAND
        gtm_brand_id = None
        for cat in all_categories:
            if cat.get('name') == 'GTM BRAND':
                gtm_brand_id = cat.get('id')
                break
        
        if gtm_brand_id:
            print(f"\n✅ ID категории GTM BRAND: {gtm_brand_id}")
        else:
            print("\n❌ Категория GTM BRAND не найдена")

if __name__ == "__main__":
    main() 