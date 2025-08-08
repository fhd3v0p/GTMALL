#!/usr/bin/env python3
"""
Удаление Test Artist (ID 1)
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

def delete_test_artist():
    """Удаление Test Artist (ID 1)"""
    print("🗑️ Удаление Test Artist (ID 1)...")
    
    # Удаляем Test Artist
    response = requests.delete(
        f"{SUPABASE_URL}/rest/v1/artists?id=eq.1",
        headers=headers
    )
    
    if response.status_code == 200:
        print("✅ Test Artist (ID 1) удален")
        return True
    else:
        print(f"❌ Ошибка удаления Test Artist: {response.status_code}")
        return False

def check_artists_after_deletion():
    """Проверка артистов после удаления"""
    print("\n🔍 Проверка артистов после удаления...")
    
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/artists?select=id,name,city&order=id",
        headers=headers
    )
    
    if response.status_code == 200:
        artists = response.json()
        print(f"📊 Всего артистов: {len(artists)}")
        
        for artist in artists:
            print(f"  • ID {artist['id']}: {artist['name']} - {artist['city']}")
        
        return True
    else:
        print(f"❌ Ошибка проверки артистов: {response.status_code}")
        return False

def main():
    print("🧹 Удаление Test Artist")
    print("=" * 40)
    
    # Удаляем Test Artist
    delete_test_artist()
    
    # Проверяем результат
    check_artists_after_deletion()
    
    print("\n✅ Удаление Test Artist завершено!")

if __name__ == "__main__":
    main() 