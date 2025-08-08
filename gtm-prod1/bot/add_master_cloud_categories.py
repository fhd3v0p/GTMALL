#!/usr/bin/env python3
"""
Добавление всех категорий из MasterCloudCategories в Supabase
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

def get_existing_categories():
    """Получает существующие категории"""
    url = f"{SUPABASE_URL}/rest/v1/categories?select=name"
    headers = get_headers()
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        categories = response.json()
        return [cat['name'] for cat in categories]
    else:
        print(f"❌ Ошибка получения категорий: {response.status_code}")
        return []

def add_category(name, description, category_type):
    """Добавляет новую категорию"""
    url = f"{SUPABASE_URL}/rest/v1/categories"
    headers = get_headers()
    
    category_data = {
        "name": name,
        "description": description,
        "type": category_type,
        "is_active": True
    }
    
    response = requests.post(url, json=category_data, headers=headers)
    
    if response.status_code in [200, 201]:
        print(f"✅ Категория {name} добавлена")
        return True
    else:
        print(f"❌ Ошибка добавления категории {name}: {response.status_code} - {response.text}")
        return False

def main():
    """Основная функция"""
    print("🔧 Добавляем все категории из MasterCloudCategories...")
    
    # Категории из MasterCloudCategories
    master_cloud_categories = [
        # Товары (product)
        {'name': 'GTM BRAND', 'description': 'Брендовые товары GTM', 'type': 'product'},
        {'name': 'Jewelry', 'description': 'Украшения', 'type': 'product'},
        {'name': 'Custom', 'description': 'Индивидуальные заказы', 'type': 'product'},
        {'name': 'Second', 'description': 'Вторые руки', 'type': 'product'},
        
        # Услуги (service)
        {'name': 'Tattoo', 'description': 'Татуировки', 'type': 'service'},
        {'name': 'Hair', 'description': 'Парикмахерские услуги', 'type': 'service'},
        {'name': 'Nails', 'description': 'Маникюр и педикюр', 'type': 'service'},
        {'name': 'Piercing', 'description': 'Пирсинг', 'type': 'service'},
    ]
    
    # Получаем существующие категории
    existing_categories = get_existing_categories()
    print(f"📊 Существующие категории: {existing_categories}")
    
    # Добавляем недостающие категории
    for category in master_cloud_categories:
        if category['name'] not in existing_categories:
            add_category(category['name'], category['description'], category['type'])
        else:
            print(f"✓ Категория {category['name']} уже существует")
    
    print("\n✅ Все категории из MasterCloudCategories добавлены в Supabase!")

if __name__ == "__main__":
    main()