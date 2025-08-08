#!/usr/bin/env python3
"""
Исправление Lin++ категории - принудительное обновление
"""

import requests

# Supabase конфигурация
SUPABASE_URL = "https://rxmtovqxjsvogyywyrha.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1Mjg1NTAsImV4cCI6MjA3MDEwNDU1MH0.gDkJybktFoi486hbIVwppDfmVQlAR0fM4o4Sl1-AxhE"

def get_headers():
    """Возвращает заголовки для API запросов"""
    return {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal'
    }

def get_lin_artists():
    """Получает всех артистов с именем Lin++"""
    url = f"{SUPABASE_URL}/rest/v1/artists?name=like.*Lin*&select=*"
    headers = get_headers()
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        artists = response.json()
        print(f"Найдено артистов Lin++: {len(artists)}")
        for artist in artists:
            print(f"  ID: {artist['id']}, Name: {artist['name']}, Specialties: {artist['specialties']}")
        return artists
    else:
        print(f"❌ Ошибка получения артистов: {response.status_code} - {response.text}")
        return []

def update_artist_by_id(artist_id, updates):
    """Обновляет данные артиста по ID"""
    url = f"{SUPABASE_URL}/rest/v1/artists?id=eq.{artist_id}"
    headers = get_headers()
    
    response = requests.patch(url, json=updates, headers=headers)
    
    if response.status_code in [200, 204]:
        print(f"✅ Артист ID {artist_id} обновлен: {updates}")
        return True
    else:
        print(f"❌ Ошибка обновления артиста ID {artist_id}: {response.status_code} - {response.text}")
        return False

def main():
    """Основная функция"""
    print("🔧 Исправляем Lin++ принудительно...")
    
    # Получаем всех артистов Lin++
    lin_artists = get_lin_artists()
    
    # Обновляем каждого
    for artist in lin_artists:
        if 'Lin' in artist['name']:
            update_artist_by_id(artist['id'], {
                "specialties": ["Tattoo"]
            })
    
    print("\n✅ Lin++ исправлен принудительно!")

if __name__ == "__main__":
    main()