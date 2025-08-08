#!/usr/bin/env python3
"""
Скрипт для добавления продукта GOTHAM'S TOP MODEL CROP FIT T-SHIRT в Supabase
(артист GTM уже добавлен с ID 14)
"""

import requests
import json
import os

# Supabase Configuration
SUPABASE_URL = "https://rxmtovqxjsvogyywyrha.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1Mjg1NTAsImV4cCI6MjA3MDEwNDU1MH0.gDkJybktFoi486hbIVwppDfmVQlAR0fM4o4Sl1-AxhE"

# Headers for Supabase API
HEADERS = {
    'apikey': SUPABASE_ANON_KEY,
    'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
    'Content-Type': 'application/json',
}

def add_product_to_supabase() -> str:
    """Добавляет продукт GOTHAM'S TOP MODEL CROP FIT T-SHIRT в Supabase"""
    
    # Данные продукта
    product_data = {
        "name": "GOTHAM'S TOP MODEL CROP FIT T-SHIRT",
        "category": "GTM BRAND",
        "subcategory": "tshirt",
        "brand": "GTM",
        "description": "Укороченная футболка GTM. Футболка выполнена из мягкого хлопкового материала, который приятно ощущается на теле. Фирменный принт проекта GTM добавляет уникальности и делает образ запоминающимся. Модель укороченная — отлично сидит как кроп-топ на девушках, а парням подойдёт, если вы не боитесь выделяться и цените стильные нестандартные силуэты.",
        "summary": "Укороченная футболка GTM с фирменным принтом",
        "price": 3799.00,
        "old_price": None,
        "discount_percent": 0,
        "size_type": "clothing",
        "size_clothing": "M",
        "size_pants": "",
        "size_shoes_eu": None,
        "size": "XS S M L XL XXL",
        "color": "Черный",
        "master_id": 14,  # ID артиста GTM
        "master_telegram": "@G_T_MODEL",
        "avatar": "https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets-public/products/GTM_Tshirt/avatar.jpg",
        "gallery": [
            "https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets-public/products/GTM_Tshirt/gallery1.jpg",
            "https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets-public/products/GTM_Tshirt/gallery2.jpg",
            "https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets-public/products/GTM_Tshirt/gallery3.jpg"
        ],
        "is_new": True,
        "is_available": True
    }
    
    try:
        print(f"📤 Отправляем данные продукта: {json.dumps(product_data, indent=2)}")
        
        # Добавляем продукт в таблицу products
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/products",
            headers=HEADERS,
            json=product_data
        )
        
        print(f"📥 Получен ответ: {response.status_code}")
        print(f"📥 Текст ответа: {response.text}")
        
        if response.status_code == 201:
            try:
                response_data = response.json()
                if response_data and 'id' in response_data:
                    product_id = response_data['id']
                    print(f"✅ Продукт GOTHAM'S TOP MODEL CROP FIT T-SHIRT добавлен с ID: {product_id}")
                    return str(product_id)
                else:
                    # Если ответ пустой, попробуем получить ID через GET запрос
                    print("📋 Ответ пустой, получаем ID продукта через GET запрос...")
                    get_response = requests.get(
                        f"{SUPABASE_URL}/rest/v1/products?name=eq.GOTHAM'S TOP MODEL CROP FIT T-SHIRT&select=id",
                        headers=HEADERS
                    )
                    if get_response.status_code == 200:
                        products = get_response.json()
                        if products:
                            product_id = products[0]['id']
                            print(f"✅ Продукт найден с ID: {product_id}")
                            return str(product_id)
                        else:
                            print("❌ Продукт не найден в базе")
                            return ""
                    else:
                        print(f"❌ Ошибка получения продукта: {get_response.status_code}")
                        return ""
            except json.JSONDecodeError as e:
                print(f"📋 Ответ пустой, получаем ID продукта через GET запрос...")
                # Если JSON пустой, попробуем получить ID через GET запрос
                get_response = requests.get(
                    f"{SUPABASE_URL}/rest/v1/products?name=eq.GOTHAM'S TOP MODEL CROP FIT T-SHIRT&select=id",
                    headers=HEADERS
                )
                if get_response.status_code == 200:
                    products = get_response.json()
                    if products:
                        product_id = products[0]['id']
                        print(f"✅ Продукт найден с ID: {product_id}")
                        return str(product_id)
                    else:
                        print("❌ Продукт не найден в базе")
                        return ""
                else:
                    print(f"❌ Ошибка получения продукта: {get_response.status_code}")
                    return ""
        else:
            print(f"❌ Ошибка добавления продукта: {response.status_code} - {response.text}")
            return ""
            
    except Exception as e:
        print(f"❌ Ошибка при добавлении продукта: {e}")
        import traceback
        traceback.print_exc()
        return ""

def main():
    """Основная функция"""
    print("🚀 Добавляем продукт GOTHAM'S TOP MODEL CROP FIT T-SHIRT в Supabase...")
    
    # Проверяем наличие файлов
    required_files = [
        "assets/products/GTM_Tshirt/avatar.jpg",
        "assets/products/GTM_Tshirt/gallery1.jpg",
        "assets/products/GTM_Tshirt/gallery2.jpg",
        "assets/products/GTM_Tshirt/gallery3.jpg"
    ]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"❌ Файл не найден: {file_path}")
            return
    
    print("✅ Все необходимые файлы найдены")
    
    # Добавляем продукт
    print("\n📦 Добавляем продукт GOTHAM'S TOP MODEL CROP FIT T-SHIRT...")
    product_id = add_product_to_supabase()
    
    if not product_id:
        print("❌ Не удалось добавить продукт")
        return
    
    print("\n🎉 Успешно добавлен:")
    print(f"   - Продукт GOTHAM'S TOP MODEL CROP FIT T-SHIRT (ID: {product_id})")
    print(f"   - Привязан к артисту GTM (ID: 14)")
    print("\n📱 Теперь Flutter приложение сможет загрузить этот продукт из Supabase!")

if __name__ == "__main__":
    main() 