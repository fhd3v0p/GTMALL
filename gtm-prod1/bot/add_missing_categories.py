#!/usr/bin/env python3
"""
Добавление недостающих категорий из MasterCloud
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

def add_missing_categories():
    """Добавление недостающих категорий"""
    print("➕ Добавление недостающих категорий...")
    
    # Категории из MasterCloud
    master_cloud_categories = [
        # Товары (product)
        {'name': 'GTM BRAND', 'description': 'Брендовые товары GTM', 'type': 'product'},
        {'name': 'Custom', 'description': 'Индивидуальные заказы', 'type': 'product'},
        {'name': 'Second', 'description': 'Вторые руки', 'type': 'product'},
        
        # Услуги (service) - некоторые уже есть, но проверим
        {'name': 'Hair', 'description': 'Парикмахерские услуги', 'type': 'service'},
    ]
    
    # Получаем существующие категории
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/categories?select=name",
        headers=headers
    )
    
    if response.status_code != 200:
        print(f"❌ Ошибка получения категорий: {response.status_code}")
        return False
    
    existing_categories = [cat['name'] for cat in response.json()]
    print(f"📋 Существующие категории: {existing_categories}")
    
    # Добавляем недостающие категории
    added_count = 0
    for category in master_cloud_categories:
        if category['name'] not in existing_categories:
            print(f"➕ Добавляем категорию: {category['name']} ({category['type']})")
            
            category_data = {
                "name": category['name'],
                "description": category['description'],
                "type": category['type']
            }
            
            response = requests.post(
                f"{SUPABASE_URL}/rest/v1/categories",
                headers=headers,
                json=category_data
            )
            
            if response.status_code in [200, 201]:
                print(f"  ✅ Категория {category['name']} добавлена")
                added_count += 1
            else:
                print(f"  ❌ Ошибка добавления категории {category['name']}: {response.status_code}")
        else:
            print(f"✓ Категория {category['name']} уже существует")
    
    print(f"\n📊 Добавлено категорий: {added_count}")
    return True

def assign_gtm_brand_category():
    """Назначение категории GTM BRAND для артиста GTM (ID 14)"""
    print("\n🏷️ Назначение категории GTM BRAND для GTM...")
    
    # Получаем ID категории GTM BRAND
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/categories?name=eq.GTM%20BRAND&select=id",
        headers=headers
    )
    
    if response.status_code != 200:
        print(f"❌ Ошибка получения категории GTM BRAND: {response.status_code}")
        return False
    
    categories = response.json()
    if not categories:
        print("❌ Категория GTM BRAND не найдена")
        return False
    
    category_id = categories[0]['id']
    print(f"📋 Найдена категория GTM BRAND с ID: {category_id}")
    
    # Добавляем связь артиста GTM (ID 14) с категорией GTM BRAND
    artist_category_data = {
        "artist_id": 14,
        "category_id": category_id
    }
    
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/artist_categories",
        headers=headers,
        json=artist_category_data
    )
    
    if response.status_code in [200, 201]:
        print("✅ Категория GTM BRAND назначена артисту GTM")
        return True
    else:
        print(f"❌ Ошибка назначения категории: {response.status_code}")
        return False

def check_all_categories():
    """Проверка всех категорий"""
    print("\n🔍 Проверка всех категорий...")
    
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/categories?select=id,name,type&order=id",
        headers=headers
    )
    
    if response.status_code == 200:
        categories = response.json()
        print(f"📊 Всего категорий: {len(categories)}")
        
        for category in categories:
            print(f"  • ID {category['id']}: {category['name']} ({category['type']})")
        
        return True
    else:
        print(f"❌ Ошибка проверки категорий: {response.status_code}")
        return False

def main():
    print("➕ Добавление недостающих категорий и назначение GTM BRAND")
    print("=" * 60)
    
    # Добавляем недостающие категории
    add_missing_categories()
    
    # Назначаем категорию GTM BRAND
    assign_gtm_brand_category()
    
    # Проверяем результат
    check_all_categories()
    
    print("\n✅ Добавление категорий завершено!")

if __name__ == "__main__":
    main()