#!/usr/bin/env python3
"""
Добавление категории GTM BRAND и назначение её артисту GTM
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

def add_gtm_brand_category():
    """Добавление категории GTM BRAND"""
    print("➕ Добавление категории GTM BRAND...")
    
    # Проверяем, существует ли уже категория GTM BRAND
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/categories?name=eq.GTM%20BRAND&select=id",
        headers=headers
    )
    
    if response.status_code == 200:
        existing_categories = response.json()
        if existing_categories:
            print(f"✅ Категория GTM BRAND уже существует с ID: {existing_categories[0]['id']}")
            return existing_categories[0]['id']
    
    # Добавляем категорию GTM BRAND
    category_data = {
        "name": "GTM BRAND",
        "description": "Брендовые товары GTM",
        "type": "product"
    }
    
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/categories",
        headers=headers,
        json=category_data
    )
    
    if response.status_code in [200, 201]:
        new_category = response.json()
        category_id = new_category[0]['id'] if isinstance(new_category, list) else new_category['id']
        print(f"✅ Категория GTM BRAND добавлена с ID: {category_id}")
        return category_id
    else:
        print(f"❌ Ошибка добавления категории GTM BRAND: {response.status_code}")
        print(f"   Ответ: {response.text}")
        return None

def assign_gtm_brand_to_artist(category_id):
    """Назначение категории GTM BRAND артисту GTM (ID 14)"""
    print(f"\n🏷️ Назначение категории GTM BRAND (ID: {category_id}) артисту GTM...")
    
    # Проверяем, есть ли уже связь
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/artist_categories?artist_id=eq.14&category_id=eq.{category_id}",
        headers=headers
    )
    
    if response.status_code == 200:
        existing_relations = response.json()
        if existing_relations:
            print("✅ Связь артиста GTM с категорией GTM BRAND уже существует")
            return True
    
    # Добавляем связь артиста GTM с категорией GTM BRAND
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
        print(f"   Ответ: {response.text}")
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

def check_artist_categories():
    """Проверка категорий артиста GTM"""
    print("\n🔍 Проверка категорий артиста GTM...")
    
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/artist_categories?artist_id=eq.14&select=category_id",
        headers=headers
    )
    
    if response.status_code == 200:
        artist_categories = response.json()
        print(f"📊 Категорий у артиста GTM: {len(artist_categories)}")
        
        for relation in artist_categories:
            print(f"  • Категория ID: {relation['category_id']}")
        
        return True
    else:
        print(f"❌ Ошибка проверки категорий артиста: {response.status_code}")
        return False

def main():
    print("🏷️ Добавление категории GTM BRAND и назначение артисту GTM")
    print("=" * 60)
    
    # Добавляем категорию GTM BRAND
    category_id = add_gtm_brand_category()
    
    if category_id:
        # Назначаем категорию артисту GTM
        assign_gtm_brand_to_artist(category_id)
        
        # Проверяем результаты
        check_all_categories()
        check_artist_categories()
    
    print("\n✅ Добавление категории GTM BRAND завершено!")

if __name__ == "__main__":
    main() 