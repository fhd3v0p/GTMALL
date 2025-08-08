#!/usr/bin/env python3
"""
Тестовый скрипт для проверки загрузки продуктов
"""

import requests
import json

# Supabase Configuration
SUPABASE_URL = "https://rxmtovqxjsvogyywyrha.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1Mjg1NTAsImV4cCI6MjA3MDEwNDU1MH0.gDkJybktFoi486hbIVwppDfmVQlAR0fM4o4Sl1-AxhE"

# Headers for Supabase API
HEADERS = {
    'apikey': SUPABASE_ANON_KEY,
    'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
    'Content-Type': 'application/json',
}

def test_products_api():
    """Тестирует API продуктов"""
    print("🔍 Тестируем API продуктов...")
    
    # Тест 1: Получить все продукты
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/products",
            headers=HEADERS
        )
        
        print(f"📋 Тест 1 - Все продукты:")
        print(f"   Статус: {response.status_code}")
        if response.status_code == 200:
            products = response.json()
            print(f"   Количество: {len(products)}")
            for product in products:
                print(f"   - {product.get('name')} (ID: {product.get('id')}, Master: {product.get('master_id')})")
        else:
            print(f"   Ошибка: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    # Тест 2: Получить продукты артиста GTM (ID 14)
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/products?master_id=eq.14",
            headers=HEADERS
        )
        
        print(f"\n📋 Тест 2 - Продукты артиста GTM (ID 14):")
        print(f"   Статус: {response.status_code}")
        if response.status_code == 200:
            products = response.json()
            print(f"   Количество: {len(products)}")
            for product in products:
                print(f"   - {product.get('name')} (ID: {product.get('id')})")
                print(f"     Цена: {product.get('price')} ₽")
                print(f"     Категория: {product.get('category')}")
                print(f"     Аватар: {product.get('avatar')}")
                print(f"     Галерея: {product.get('gallery')}")
        else:
            print(f"   Ошибка: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")

def test_storage_bucket():
    """Тестирует доступ к Storage bucket"""
    print(f"\n🔍 Тестируем Storage bucket...")
    
    bucket_name = "gtm-assets-public"
    
    # Тест 1: Проверить аватар артиста GTM
    try:
        avatar_url = f"{SUPABASE_URL}/storage/v1/object/public/{bucket_name}/artists/14/avatar.png"
        response = requests.head(avatar_url)
        
        print(f"📋 Тест 1 - Аватар артиста GTM:")
        print(f"   URL: {avatar_url}")
        print(f"   Статус: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Аватар доступен")
        else:
            print("   ❌ Аватар недоступен")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    # Тест 2: Проверить аватар продукта GTM
    try:
        product_avatar_url = f"{SUPABASE_URL}/storage/v1/object/public/{bucket_name}/products/GTM_Tshirt/avatar.jpg"
        response = requests.head(product_avatar_url)
        
        print(f"\n📋 Тест 2 - Аватар продукта GTM:")
        print(f"   URL: {product_avatar_url}")
        print(f"   Статус: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Аватар продукта доступен")
        else:
            print("   ❌ Аватар продукта недоступен")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    # Тест 3: Проверить галерею продукта
    try:
        gallery_url = f"{SUPABASE_URL}/storage/v1/object/public/{bucket_name}/products/GTM_Tshirt/gallery1.jpg"
        response = requests.head(gallery_url)
        
        print(f"\n📋 Тест 3 - Галерея продукта GTM:")
        print(f"   URL: {gallery_url}")
        print(f"   Статус: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Галерея доступна")
        else:
            print("   ❌ Галерея недоступна")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")

def test_artists_loading():
    """Тестирует загрузку артистов"""
    print(f"\n🔍 Тестируем загрузку артистов...")
    
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/artists",
            headers=HEADERS
        )
        
        print(f"📋 Статус: {response.status_code}")
        if response.status_code == 200:
            artists = response.json()
            print(f"   Количество артистов: {len(artists)}")
            
            # Найти артиста GTM
            gtm_artist = None
            for artist in artists:
                if artist.get('name') == 'GTM':
                    gtm_artist = artist
                    break
            
            if gtm_artist:
                print(f"   ✅ Артист GTM найден (ID: {gtm_artist.get('id')})")
                print(f"      Аватар URL: {gtm_artist.get('avatar_url')}")
                print(f"      Специальности: {gtm_artist.get('specialties')}")
            else:
                print("   ❌ Артист GTM не найден")
        else:
            print(f"   ❌ Ошибка: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")

def main():
    """Основная функция"""
    print("🧪 Начинаем тестирование...")
    
    # Тестируем API продуктов
    test_products_api()
    
    # Тестируем Storage bucket
    test_storage_bucket()
    
    # Тестируем загрузку артистов
    test_artists_loading()
    
    print(f"\n🎯 Тестирование завершено!")

if __name__ == "__main__":
    main() 