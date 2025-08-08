#!/usr/bin/env python3
"""
Проверка текущих категорий артистов в Supabase
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
    }

def check_artists():
    """Проверяет текущие данные артистов"""
    url = f"{SUPABASE_URL}/rest/v1/artists?select=name,specialties,city"
    headers = get_headers()
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        artists = response.json()
        print(f"📊 Найдено {len(artists)} артистов:")
        for artist in artists:
            print(f"  - {artist['name']}: {artist['specialties']} (город: {artist['city']})")
    else:
        print(f"❌ Ошибка: {response.status_code} - {response.text}")

if __name__ == "__main__":
    check_artists()