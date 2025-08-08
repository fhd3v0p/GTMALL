#!/usr/bin/env python3
"""
Исправление категорий артиста GTM - убираем из Tattoo, оставляем только GTM BRAND
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

def get_category_id(category_name):
    """Получение ID категории по имени"""
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/categories?name=eq.{category_name}&select=id",
        headers=headers
    )
    
    if response.status_code == 200:
        categories = response.json()
        if categories:
            return categories[0]['id']
    return None

def get_artist_categories(artist_id):
    """Получение всех категорий артиста"""
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/artist_categories?artist_id=eq.{artist_id}&select=category_id",
        headers=headers
    )
    
    if response.status_code == 200:
        return response.json()
    return []

def remove_artist_from_category(artist_id, category_id):
    """Удаление артиста из категории"""
    response = requests.delete(
        f"{SUPABASE_URL}/rest/v1/artist_categories?artist_id=eq.{artist_id}&category_id=eq.{category_id}",
        headers=headers
    )
    
    return response.status_code == 200

def add_artist_to_category(artist_id, category_id):
    """Добавление артиста в категорию"""
    artist_category_data = {
        "artist_id": artist_id,
        "category_id": category_id
    }
    
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/artist_categories",
        headers=headers,
        json=artist_category_data
    )
    
    return response.status_code in [200, 201]

def fix_gtm_artist_categories():
    """Исправление категорий артиста GTM"""
    print("🔧 Исправление категорий артиста GTM...")
    
    artist_id = 14  # ID артиста GTM
    
    # Получаем ID категорий
    tattoo_category_id = get_category_id("Tattoo")
    gtm_brand_category_id = get_category_id("GTM BRAND")
    
    print(f"📋 ID категории Tattoo: {tattoo_category_id}")
    print(f"📋 ID категории GTM BRAND: {gtm_brand_category_id}")
    
    if not tattoo_category_id:
        print("❌ Категория Tattoo не найдена")
        return False
    
    if not gtm_brand_category_id:
        print("❌ Категория GTM BRAND не найдена")
        return False
    
    # Получаем текущие категории артиста GTM
    current_categories = get_artist_categories(artist_id)
    print(f"📊 Текущие категории артиста GTM: {len(current_categories)}")
    
    # Удаляем из категории Tattoo
    if tattoo_category_id in [cat['category_id'] for cat in current_categories]:
        print(f"🗑️ Удаляем GTM из категории Tattoo...")
        if remove_artist_from_category(artist_id, tattoo_category_id):
            print("✅ GTM удален из категории Tattoo")
        else:
            print("❌ Ошибка удаления из категории Tattoo")
    else:
        print("ℹ️ GTM уже не в категории Tattoo")
    
    # Добавляем в категорию GTM BRAND (если еще не добавлен)
    if gtm_brand_category_id not in [cat['category_id'] for cat in current_categories]:
        print(f"➕ Добавляем GTM в категорию GTM BRAND...")
        if add_artist_to_category(artist_id, gtm_brand_category_id):
            print("✅ GTM добавлен в категорию GTM BRAND")
        else:
            print("❌ Ошибка добавления в категорию GTM BRAND")
    else:
        print("ℹ️ GTM уже в категории GTM BRAND")
    
    return True

def check_artist_categories_after_fix():
    """Проверка категорий артиста GTM после исправления"""
    print("\n🔍 Проверка категорий артиста GTM после исправления...")
    
    artist_id = 14
    
    # Получаем все категории артиста GTM с названиями
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/artist_categories?artist_id=eq.{artist_id}&select=category_id",
        headers=headers
    )
    
    if response.status_code == 200:
        artist_categories = response.json()
        print(f"📊 Категорий у артиста GTM: {len(artist_categories)}")
        
        for relation in artist_categories:
            category_id = relation['category_id']
            # Получаем название категории
            cat_response = requests.get(
                f"{SUPABASE_URL}/rest/v1/categories?id=eq.{category_id}&select=name",
                headers=headers
            )
            if cat_response.status_code == 200:
                categories = cat_response.json()
                if categories:
                    print(f"  • {categories[0]['name']} (ID: {category_id})")
        
        return True
    else:
        print(f"❌ Ошибка проверки категорий артиста: {response.status_code}")
        return False

def main():
    print("🔧 Исправление категорий артиста GTM")
    print("=" * 50)
    
    # Исправляем категории
    fix_gtm_artist_categories()
    
    # Проверяем результат
    check_artist_categories_after_fix()
    
    print("\n✅ Исправление категорий GTM завершено!")

if __name__ == "__main__":
    main() 