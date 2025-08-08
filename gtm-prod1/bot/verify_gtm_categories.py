#!/usr/bin/env python3
"""
Проверка категорий артиста GTM в таблице artist_categories
"""
import requests
import json

# Supabase Configuration
SUPABASE_URL = 'https://rxmtovqxjsvogyywyrha.supabase.co'
SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1Mjg1NTAsImV4cCI6MjA3MDEwNDU1MH0.gDkJybktFoi486hbIVwppDfmVQlAR0fM4o4Sl1-AxhE'

def check_gtm_categories():
    """Проверка категорий артиста GTM"""
    print("🔍 Проверка категорий артиста GTM...")
    
    # SQL запрос для получения категорий артиста GTM
    url = f'{SUPABASE_URL}/rest/v1/rpc/get_artist_categories'
    headers = {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'artist_id': 14
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        categories = response.json()
        if categories:
            print(f"📋 Категории артиста GTM (ID: 14):")
            for category in categories:
                print(f"   • {category['name']} (ID: {category['id']})")
            
            # Проверяем, что есть только GTM BRAND
            category_names = [cat['name'] for cat in categories]
            if len(category_names) == 1 and 'GTM BRAND' in category_names:
                print("✅ GTM находится только в категории GTM BRAND")
                return True
            else:
                print("❌ GTM находится в неправильных категориях")
                return False
        else:
            print("❌ Категории для GTM не найдены")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при проверке категорий: {e}")
        return False

def check_artist_categories_table():
    """Проверка таблицы artist_categories для GTM"""
    print("\n🔍 Проверка таблицы artist_categories...")
    
    url = f'{SUPABASE_URL}/rest/v1/artist_categories'
    headers = {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
        'Content-Type': 'application/json'
    }
    
    params = {
        'artist_id': 'eq.14',
        'select': 'artist_id,category_id'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        if data:
            print(f"📋 Найдено связей в artist_categories для GTM: {len(data)}")
            for record in data:
                print(f"   Artist ID: {record['artist_id']}, Category ID: {record['category_id']}")
            return data
        else:
            print("❌ Связей в artist_categories для GTM не найдено")
            return []
            
    except Exception as e:
        print(f"❌ Ошибка при проверке artist_categories: {e}")
        return []

def get_category_name(category_id):
    """Получение имени категории по ID"""
    url = f'{SUPABASE_URL}/rest/v1/categories'
    headers = {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
        'Content-Type': 'application/json'
    }
    
    params = {
        'id': f'eq.{category_id}',
        'select': 'id,name'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        if data:
            return data[0]['name']
        else:
            return f"Unknown (ID: {category_id})"
            
    except Exception as e:
        return f"Error (ID: {category_id})"

if __name__ == "__main__":
    print("🔍 Проверка категорий артиста GTM")
    print("=" * 50)
    
    # Проверяем категории через RPC функцию
    check_gtm_categories()
    
    # Проверяем таблицу artist_categories
    records = check_artist_categories_table()
    
    if records:
        print("\n📋 Детальная информация о категориях:")
        for record in records:
            category_name = get_category_name(record['category_id'])
            print(f"   Category ID {record['category_id']}: {category_name}")
    
    print("\n✅ Проверка категорий завершена!") 