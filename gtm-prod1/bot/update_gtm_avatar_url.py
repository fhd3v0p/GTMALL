#!/usr/bin/env python3
"""
Обновление avatar_url артиста GTM в базе данных
"""
import requests
import json

# Supabase Configuration
SUPABASE_URL = 'https://rxmtovqxjsvogyywyrha.supabase.co'
SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1Mjg1NTAsImV4cCI6MjA3MDEwNDU1MH0.gDkJybktFoi486hbIVwppDfmVQlAR0fM4o4Sl1-AxhE'

def update_gtm_avatar_url():
    """Обновление avatar_url артиста GTM"""
    print("🔧 Обновление avatar_url артиста GTM...")
    
    url = f'{SUPABASE_URL}/rest/v1/artists'
    headers = {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal'
    }
    
    # Новый avatar_url с правильным путем
    new_avatar_url = f'{SUPABASE_URL}/storage/v1/object/public/gtm-assets-public/artists/14/avatar.png'
    
    data = {
        'avatar_url': new_avatar_url
    }
    
    params = {
        'id': 'eq.14'
    }
    
    try:
        response = requests.patch(url, headers=headers, params=params, json=data)
        response.raise_for_status()
        
        print("✅ Avatar URL обновлен в базе данных")
        print(f"🔗 Новый URL: {new_avatar_url}")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка обновления avatar_url: {e}")
        return False

def verify_update():
    """Проверка обновления"""
    print("\n🔍 Проверка обновления...")
    
    url = f'{SUPABASE_URL}/rest/v1/artists'
    headers = {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
        'Content-Type': 'application/json'
    }
    
    params = {
        'id': 'eq.14',
        'select': 'id,name,avatar_url'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        if data:
            artist = data[0]
            print(f"📋 Данные артиста GTM (ID: {artist['id']}):")
            print(f"   Имя: {artist['name']}")
            print(f"   Avatar URL: {artist['avatar_url']}")
            
            if 'artists/14/' in artist['avatar_url']:
                print("✅ Avatar URL обновлен корректно!")
                return True
            else:
                print("❌ Avatar URL не обновлен")
                return False
        else:
            print("❌ Артист GTM не найден")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при проверке: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Обновление avatar_url артиста GTM")
    print("=" * 50)
    
    # Обновляем avatar_url
    success = update_gtm_avatar_url()
    
    if success:
        # Проверяем обновление
        verify_update()
        
        print("\n✅ Обновление завершено!")
        print("🔗 Теперь GTM использует правильный путь: artists/14/")
    else:
        print("\n❌ Не удалось обновить avatar_url") 