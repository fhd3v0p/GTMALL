#!/usr/bin/env python3
"""
Скрипт для добавления артиста GTM и продукта GOTHAM'S TOP MODEL CROP FIT T-SHIRT в Supabase
"""

import requests
import json
import os
from typing import Dict, List, Any

# Supabase Configuration
SUPABASE_URL = "https://rxmtovqxjsvogyywyrha.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1Mjg1NTAsImV4cCI6MjA3MDEwNDU1MH0.gDkJybktFoi486hbIVwppDfmVQlAR0fM4o4Sl1-AxhE"
STORAGE_BUCKET = "gtm-assets-public"

# Headers for Supabase API
HEADERS = {
    'apikey': SUPABASE_ANON_KEY,
    'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
    'Content-Type': 'application/json',
}

def add_artist_to_supabase() -> str:
    """Добавляет артиста GTM в Supabase"""
    
    # Данные артиста GTM (без загрузки файлов пока)
    artist_data = {
        "name": "GTM",
        "username": "gtm_brand",
        "bio": "GOTHAM'S TOP MODEL - неформальный маркетплейс внутри Telegram. Тату, пирсинг, окрашивания, секонд-хенд и мерч. Записывайся к мастерам, продавай и покупай! Следи за дропами, апдейтами и движем GTM.",
        "avatar_url": "https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets-public/artists/GTM/avatar.png",
        "city": "Санкт-Петербург, Москва, Екатеринбург, Новосибирск, Казань",
        "specialties": ["GTM BRAND"],
        "rating": 5.0,
        "is_active": True,
        "telegram": "@G_T_MODEL",
        "telegram_url": "https://t.me/G_T_MODEL",
        "tiktok": "@gothamstopmodel",
        "tiktok_url": "https://www.tiktok.com/@gothamstopmodel",
        "pinterest": "@gothamstopmodel",
        "pinterest_url": "https://ru.pinterest.com/gothamstopmodel",
        "booking_url": "https://t.me/GTM_ADM",
        "location_html": "Base:Saint-P, MSC",
        "gallery_html": "",
        "subscription_channels": [],
        "average_rating": 5.0,
        "total_ratings": 1
    }
    
    try:
        print(f"📤 Отправляем данные артиста: {json.dumps(artist_data, indent=2)}")
        
        # Добавляем артиста в таблицу artists
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/artists",
            headers=HEADERS,
            json=artist_data
        )
        
        print(f"📥 Получен ответ: {response.status_code}")
        print(f"📥 Текст ответа: {response.text}")
        
        if response.status_code == 201:
            try:
                response_data = response.json()
                if response_data and 'id' in response_data:
                    artist_id = response_data['id']
                    print(f"✅ Артист GTM добавлен с ID: {artist_id}")
                    return str(artist_id)
                else:
                    # Если ответ пустой, попробуем получить ID через GET запрос
                    print("📋 Ответ пустой, получаем ID артиста через GET запрос...")
                    get_response = requests.get(
                        f"{SUPABASE_URL}/rest/v1/artists?name=eq.GTM&select=id",
                        headers=HEADERS
                    )
                    if get_response.status_code == 200:
                        artists = get_response.json()
                        if artists:
                            artist_id = artists[0]['id']
                            print(f"✅ Артист GTM найден с ID: {artist_id}")
                            return str(artist_id)
                        else:
                            print("❌ Артист GTM не найден в базе")
                            return ""
                    else:
                        print(f"❌ Ошибка получения артиста: {get_response.status_code}")
                        return ""
            except json.JSONDecodeError as e:
                print(f"📋 Ответ пустой, получаем ID артиста через GET запрос...")
                # Если JSON пустой, попробуем получить ID через GET запрос
                get_response = requests.get(
                    f"{SUPABASE_URL}/rest/v1/artists?name=eq.GTM&select=id",
                    headers=HEADERS
                )
                if get_response.status_code == 200:
                    artists = get_response.json()
                    if artists:
                        artist_id = artists[0]['id']
                        print(f"✅ Артист GTM найден с ID: {artist_id}")
                        return str(artist_id)
                    else:
                        print("❌ Артист GTM не найден в базе")
                        return ""
                else:
                    print(f"❌ Ошибка получения артиста: {get_response.status_code}")
                    return ""
        else:
            print(f"❌ Ошибка добавления артиста: {response.status_code} - {response.text}")
            return ""
            
    except Exception as e:
        print(f"❌ Ошибка при добавлении артиста: {e}")
        import traceback
        traceback.print_exc()
        return ""

def create_products_table():
    """Создает таблицу products если её нет"""
    print("📋 Проверяем наличие таблицы products...")
    
    try:
        # Пытаемся получить данные из таблицы products
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/products",
            headers=HEADERS
        )
        
        if response.status_code == 404:
            print("❌ Таблица products не существует")
            print("💡 Нужно создать таблицу products в Supabase Dashboard")
            return False
        elif response.status_code == 200:
            print("✅ Таблица products существует")
            return True
        else:
            print(f"❌ Неизвестная ошибка: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при проверке таблицы products: {e}")
        return False

def add_product_to_supabase(artist_id: str) -> str:
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
        "size_clothing": "XS S M L XL XXL",
        "size_pants": "",
        "size_shoes_eu": None,
        "size": "XS S M L XL XXL",
        "color": "Черный",
        "master_id": artist_id,
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
        # Добавляем продукт в таблицу products
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/products",
            headers=HEADERS,
            json=product_data
        )
        
        if response.status_code == 201:
            product_id = response.json()['id']
            print(f"✅ Продукт GOTHAM'S TOP MODEL CROP FIT T-SHIRT добавлен с ID: {product_id}")
            return str(product_id)
        else:
            print(f"❌ Ошибка добавления продукта: {response.status_code} - {response.text}")
            return ""
            
    except Exception as e:
        print(f"❌ Ошибка при добавлении продукта: {e}")
        return ""

def main():
    """Основная функция"""
    print("🚀 Начинаем добавление артиста GTM и продукта в Supabase...")
    
    # Проверяем наличие файлов
    required_files = [
        "assets/artists/GTM/avatar.png",
        "assets/artists/GTM/gallery1.jpg",
        "assets/artists/GTM/gallery2.jpg", 
        "assets/artists/GTM/gallery3.jpg",
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
    
    # Добавляем артиста
    print("\n📝 Добавляем артиста GTM...")
    artist_id = add_artist_to_supabase()
    
    if not artist_id:
        print("❌ Не удалось добавить артиста")
        return
    
    # Проверяем таблицу products
    if not create_products_table():
        print("❌ Таблица products не существует. Создайте её в Supabase Dashboard")
        return
    
    # Добавляем продукт
    print("\n📦 Добавляем продукт GOTHAM'S TOP MODEL CROP FIT T-SHIRT...")
    product_id = add_product_to_supabase(artist_id)
    
    if not product_id:
        print("❌ Не удалось добавить продукт")
        return
    
    print("\n🎉 Успешно добавлены:")
    print(f"   - Артист GTM (ID: {artist_id})")
    print(f"   - Продукт GOTHAM'S TOP MODEL CROP FIT T-SHIRT (ID: {product_id})")
    print("\n📱 Теперь Flutter приложение сможет загрузить эти данные из Supabase!")

if __name__ == "__main__":
    main() 