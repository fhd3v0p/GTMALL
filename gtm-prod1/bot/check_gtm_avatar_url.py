#!/usr/bin/env python3
"""
Проверка avatar_url артиста GTM в базе данных
"""
import requests
import json

# Supabase Configuration
SUPABASE_URL = 'https://rxmtovqxjsvogyywyrha.supabase.co'
SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1Mjg1NTAsImV4cCI6MjA3MDEwNDU1MH0.gDkJybktFoi486hbIVwppDfmVQlAR0fM4o4Sl1-AxhE'

def check_gtm_artist():
    """Проверка данных артиста GTM"""
    url = f'{SUPABASE_URL}/rest/v1/artists'
    headers = {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
        'Content-Type': 'application/json'
    }
    
    params = {
        'id': 'eq.14',
        'select': 'id,name,avatar_url,specialties'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        if data:
            artist = data[0]
            print(f"🔍 Данные артиста GTM (ID: {artist['id']}):")
            print(f"   Имя: {artist['name']}")
            print(f"   Avatar URL: {artist['avatar_url']}")
            print(f"   Specialties: {artist.get('specialties', [])}")
            
            # Проверяем, что avatar_url использует правильный путь
            if artist['avatar_url'] and 'artists/GTM/' in artist['avatar_url']:
                print("❌ Проблема: avatar_url использует 'artists/GTM/' вместо 'artists/14/'")
                return True
            else:
                print("✅ Avatar URL выглядит корректно")
                return False
        else:
            print("❌ Артист GTM не найден")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при получении данных: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Проверка данных артиста GTM")
    print("=" * 50)
    
    has_problem = check_gtm_artist()
    
    if has_problem:
        print("\n🔧 Нужно исправить avatar_url в базе данных")
        print("   Должно быть: artists/14/avatar.png")
        print("   Сейчас: artists/GTM/avatar.png")
    else:
        print("\n✅ Данные артиста GTM корректны") 