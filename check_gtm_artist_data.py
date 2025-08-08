#!/usr/bin/env python3
"""
Скрипт для проверки данных артиста GTM в Supabase
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

def check_gtm_artist():
    """Проверяет данные артиста GTM"""
    try:
        # Получаем артиста GTM
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/artists?id=eq.14",
            headers=HEADERS
        )
        
        if response.status_code == 200:
            artists = response.json()
            if artists:
                artist = artists[0]
                print("📋 Данные артиста GTM (ID 14):")
                print(f"   Имя: {artist.get('name')}")
                print(f"   Специальности: {artist.get('specialties')}")
                print(f"   Города: {artist.get('city')}")
                print(f"   Активен: {artist.get('is_active')}")
                print(f"   Telegram: {artist.get('telegram')}")
                print(f"   Avatar URL: {artist.get('avatar_url')}")
                
                # Проверяем, есть ли категория в specialties
                specialties = artist.get('specialties', [])
                if 'GTM BRAND' in specialties:
                    print("✅ GTM BRAND найден в specialties")
                else:
                    print("❌ GTM BRAND НЕ найден в specialties")
                
                if 'Tattoo' in specialties:
                    print("❌ Tattoo найден в specialties (НЕ ДОЛЖЕН БЫТЬ)")
                else:
                    print("✅ Tattoo НЕ найден в specialties (правильно)")
                
                return artist
            else:
                print("❌ Артист GTM не найден")
                return None
        else:
            print(f"❌ Ошибка получения артиста: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка при проверке артиста: {e}")
        return None

def check_all_artists():
    """Проверяет всех артистов"""
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/artists",
            headers=HEADERS
        )
        
        if response.status_code == 200:
            artists = response.json()
            print(f"\n📋 Все артисты ({len(artists)}):")
            for artist in artists:
                name = artist.get('name', 'Unknown')
                specialties = artist.get('specialties', [])
                print(f"   {name} (ID: {artist.get('id')}): {specialties}")
            
            return artists
        else:
            print(f"❌ Ошибка получения артистов: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Ошибка при получении артистов: {e}")
        return []

def check_artist_categories():
    """Проверяет связи артиста с категориями"""
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/artist_categories?artist_id=eq.14",
            headers=HEADERS
        )
        
        if response.status_code == 200:
            categories = response.json()
            print(f"\n📋 Связи артиста GTM с категориями:")
            for cat in categories:
                print(f"   - Категория ID: {cat.get('category_id')}")
            
            return categories
        else:
            print(f"❌ Ошибка получения связей: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Ошибка при проверке связей: {e}")
        return []

def main():
    """Основная функция"""
    print("🔍 Проверяем данные артиста GTM...")
    
    # Проверяем артиста GTM
    gtm_artist = check_gtm_artist()
    
    # Проверяем все артисты
    all_artists = check_all_artists()
    
    # Проверяем связи с категориями
    categories = check_artist_categories()
    
    print("\n🎯 Вывод:")
    if gtm_artist:
        specialties = gtm_artist.get('specialties', [])
        if 'GTM BRAND' in specialties and 'Tattoo' not in specialties:
            print("✅ Артист GTM настроен правильно - только GTM BRAND")
        else:
            print("❌ Артист GTM настроен неправильно")
            if 'Tattoo' in specialties:
                print("   - Нужно убрать Tattoo из specialties")
            if 'GTM BRAND' not in specialties:
                print("   - Нужно добавить GTM BRAND в specialties")

if __name__ == "__main__":
    main() 