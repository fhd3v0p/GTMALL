#!/usr/bin/env python3
"""
Скрипт для проверки продуктов в Supabase
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

def check_all_products():
    """Проверяет все продукты"""
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/products",
            headers=HEADERS
        )
        
        if response.status_code == 200:
            products = response.json()
            print(f"📋 Все продукты ({len(products)}):")
            for product in products:
                name = product.get('name', 'Unknown')
                master_id = product.get('master_id')
                category = product.get('category')
                price = product.get('price')
                print(f"   {name} (ID: {product.get('id')}, Master: {master_id}, Category: {category}, Price: {price})")
            
            return products
        else:
            print(f"❌ Ошибка получения продуктов: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Ошибка при получении продуктов: {e}")
        return []

def check_gtm_products():
    """Проверяет продукты артиста GTM (ID 14)"""
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/products?master_id=eq.14",
            headers=HEADERS
        )
        
        if response.status_code == 200:
            products = response.json()
            print(f"\n📋 Продукты артиста GTM (ID 14):")
            if products:
                for product in products:
                    print(f"   ✅ {product.get('name')} (ID: {product.get('id')})")
                    print(f"      Цена: {product.get('price')} ₽")
                    print(f"      Категория: {product.get('category')}")
                    print(f"      Размеры: {product.get('size')}")
                    print(f"      Описание: {product.get('description')}")
            else:
                print("   ❌ Продукты не найдены")
            
            return products
        else:
            print(f"❌ Ошибка получения продуктов GTM: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Ошибка при получении продуктов GTM: {e}")
        return []

def main():
    """Основная функция"""
    print("🔍 Проверяем продукты в базе данных...")
    
    # Проверяем все продукты
    all_products = check_all_products()
    
    # Проверяем продукты GTM
    gtm_products = check_gtm_products()
    
    print(f"\n🎯 Вывод:")
    if gtm_products:
        print(f"✅ У артиста GTM есть {len(gtm_products)} продукт(ов)")
    else:
        print("❌ У артиста GTM нет продуктов - нужно добавить")

if __name__ == "__main__":
    main() 