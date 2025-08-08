#!/usr/bin/env python3
"""
Очистка дубликатов GTM и назначение категории GTM BRAND
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

def delete_gtm_duplicates():
    """Удаление дубликатов GTM (ID 15 и 16)"""
    print("🗑️ Удаление дубликатов GTM...")
    
    duplicates_to_delete = [15, 16]  # ID дубликатов GTM
    
    for artist_id in duplicates_to_delete:
        print(f"🗑️ Удаляем артиста с ID {artist_id}...")
        
        # Удаляем артиста
        response = requests.delete(
            f"{SUPABASE_URL}/rest/v1/artists?id=eq.{artist_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            print(f"  ✅ Артист с ID {artist_id} удален")
        else:
            print(f"  ❌ Ошибка удаления артиста {artist_id}: {response.status_code}")
    
    print("✅ Удаление дубликатов завершено")

def assign_gtm_brand_category():
    """Назначение категории GTM BRAND для артиста GTM (ID 14)"""
    print("\n🏷️ Назначение категории GTM BRAND для GTM...")
    
    # Сначала получаем ID категории GTM BRAND
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

def check_artists_after_cleanup():
    """Проверка артистов после очистки"""
    print("\n🔍 Проверка артистов после очистки...")
    
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/artists?select=id,name&order=id",
        headers=headers
    )
    
    if response.status_code == 200:
        artists = response.json()
        print(f"📊 Всего артистов: {len(artists)}")
        
        for artist in artists:
            print(f"  • ID {artist['id']}: {artist['name']}")
        
        return True
    else:
        print(f"❌ Ошибка проверки артистов: {response.status_code}")
        return False

def main():
    print("🧹 Очистка дубликатов GTM и назначение категории")
    print("=" * 60)
    
    # Удаляем дубликаты
    delete_gtm_duplicates()
    
    # Назначаем категорию GTM BRAND
    assign_gtm_brand_category()
    
    # Проверяем результат
    check_artists_after_cleanup()
    
    print("\n✅ Очистка завершена!")

if __name__ == "__main__":
    main() 