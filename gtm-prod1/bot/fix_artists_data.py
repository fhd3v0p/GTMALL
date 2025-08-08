#!/usr/bin/env python3
"""
Скрипт для исправления данных артистов в Supabase
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
    print("🔧 Исправляем данные артистов...")
    
    # Обновляем Blodivamp - категория Piercing
    update_artist("Blodivamp", {
        "specialties": ["Пирсинг ушей", "Боди пирсинг", "Классический пирсинг", "Piercing"]
    })
    
    # Обновляем Aspergill - категория Hair  
    update_artist("Aspergill", {
        "specialties": ["Стрижки", "Окрашивание", "Укладки", "Мужские стрижки", "Hair"]
    })
    
    # Обновляем EMI - добавляем Москву в города
    update_artist("EMI", {
        "city": "Санкт-Петербург, Москва"
    })
    
    # Обновляем Чучундра - добавляем Москву в города  
    update_artist("Чучундра", {
        "city": "Санкт-Петербург, Москва"
    })
    
    print("\n✅ Исправления завершены!")

if __name__ == "__main__":
    main()