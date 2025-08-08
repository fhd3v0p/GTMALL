#!/usr/bin/env python3
"""
Скрипт для проверки загруженных файлов в Supabase Storage
"""

import requests

# Supabase Configuration
SUPABASE_URL = "https://rxmtovqxjsvogyywyrha.supabase.co"
BUCKET_NAME = "gtm-assets-public"

def test_storage_files():
    """Проверяет доступность файлов в Storage"""
    print("🔍 Проверяем файлы в Storage...")
    
    # Список файлов для проверки
    files_to_check = [
        "products/GTM_Tshirt/avatar.jpg",
        "products/GTM_Tshirt/gallery1.jpg", 
        "products/GTM_Tshirt/gallery2.jpg",
        "products/GTM_Tshirt/gallery3.jpg",
        "artists/14/avatar.png"
    ]
    
    for file_path in files_to_check:
        url = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{file_path}"
        try:
            response = requests.head(url)
            status = "✅ Доступен" if response.status_code == 200 else "❌ Недоступен"
            print(f"📋 {file_path}: {status} (статус: {response.status_code})")
        except Exception as e:
            print(f"📋 {file_path}: ❌ Ошибка - {e}")

def test_product_data():
    """Проверяет данные продукта в базе"""
    print(f"\n🔍 Проверяем данные продукта...")
    
    SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1Mjg1NTAsImV4cCI6MjA3MDEwNDU1MH0.gDkJybktFoi486hbIVwppDfmVQlAR0fM4o4Sl1-AxhE"
    
    HEADERS = {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
        'Content-Type': 'application/json',
    }
    
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/products?master_id=eq.14",
            headers=HEADERS
        )
        
        if response.status_code == 200:
            products = response.json()
            if products:
                product = products[0]
                print(f"📋 Продукт: {product.get('name')}")
                print(f"   Аватар: {product.get('avatar')}")
                print(f"   Галерея: {product.get('gallery')}")
                
                # Проверяем каждый файл из галереи
                gallery = product.get('gallery', [])
                for i, url in enumerate(gallery):
                    try:
                        response = requests.head(url)
                        status = "✅ Доступен" if response.status_code == 200 else "❌ Недоступен"
                        print(f"   Галерея {i+1}: {status}")
                    except Exception as e:
                        print(f"   Галерея {i+1}: ❌ Ошибка - {e}")
            else:
                print("❌ Продукты не найдены")
        else:
            print(f"❌ Ошибка получения продуктов: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def main():
    """Основная функция"""
    print("🧪 Проверяем загруженные файлы...")
    
    # Проверяем файлы в Storage
    test_storage_files()
    
    # Проверяем данные продукта
    test_product_data()
    
    print(f"\n🎯 Проверка завершена!")

if __name__ == "__main__":
    main() 