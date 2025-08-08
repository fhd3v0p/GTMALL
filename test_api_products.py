#!/usr/bin/env python3
"""
Тестовый скрипт для проверки API продуктов
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
                print(f"     Master ID: {product.get('master_id')}")
                print(f"     Master Name: {product.get('master_name')}")
                print(f"     Master Telegram: {product.get('master_telegram')}")
        else:
            print(f"   Ошибка: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    # Тест 3: Получить артиста GTM
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/artists?id=eq.14",
            headers=HEADERS
        )
        
        print(f"\n📋 Тест 3 - Артист GTM (ID 14):")
        print(f"   Статус: {response.status_code}")
        if response.status_code == 200:
            artists = response.json()
            if artists:
                artist = artists[0]
                print(f"   - Имя: {artist.get('name')}")
                print(f"     ID: {artist.get('id')}")
                print(f"     Специальности: {artist.get('specialties')}")
                print(f"     Аватар: {artist.get('avatar_url')}")
            else:
                print("   ❌ Артист не найден")
        else:
            print(f"   Ошибка: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")

def test_api_endpoints():
    """Тестирует различные API endpoints"""
    print(f"\n🔍 Тестируем API endpoints...")
    
    endpoints = [
        "/rest/v1/products",
        "/rest/v1/products?master_id=eq.14",
        "/rest/v1/artists?id=eq.14",
        "/rest/v1/artists",
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(
                f"{SUPABASE_URL}{endpoint}",
                headers=HEADERS
            )
            
            print(f"📋 {endpoint}:")
            print(f"   Статус: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    print(f"   Количество записей: {len(data)}")
                else:
                    print(f"   Данные: {data}")
            else:
                print(f"   Ошибка: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")

def main():
    """Основная функция"""
    print("🧪 Начинаем тестирование API продуктов...")
    
    # Тестируем API продуктов
    test_products_api()
    
    # Тестируем API endpoints
    test_api_endpoints()
    
    print(f"\n🎯 Тестирование завершено!")

if __name__ == "__main__":
    main() 