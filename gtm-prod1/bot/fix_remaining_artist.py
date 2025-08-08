#!/usr/bin/env python3
"""
Исправление оставшегося артиста Lin++
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

def update_artist(artist_name, updates):
    """Обновляет данные артиста"""
    url = f"{SUPABASE_URL}/rest/v1/artists?name=eq.{artist_name}"
    headers = get_headers()
    
    response = requests.patch(url, json=updates, headers=headers)
    
    if response.status_code in [200, 204]:
        print(f"✅ Артист {artist_name} обновлен: {updates}")
        return True
    else:
        print(f"❌ Ошибка обновления артиста {artist_name}: {response.status_code} - {response.text}")
        return False

def main():
    """Основная функция"""
    print("🔧 Исправляем оставшегося артиста Lin++...")
    
    # Обновляем Lin++ - категория Tattoo
    update_artist("Lin++", {
        "specialties": ["Tattoo"]
    })
    
    print("\n✅ Lin++ исправлен!")

if __name__ == "__main__":
    main()