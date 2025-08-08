#!/usr/bin/env python3
"""
Скрипт для проверки структуры таблиц в Supabase
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

def check_table_structure(table_name: str):
    """Проверяет структуру таблицы"""
    try:
        # Получаем информацию о таблице
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/{table_name}?limit=1",
            headers=HEADERS
        )
        
        if response.status_code == 200:
            print(f"✅ Таблица {table_name} доступна")
            # Пытаемся получить данные
            data_response = requests.get(
                f"{SUPABASE_URL}/rest/v1/{table_name}",
                headers=HEADERS
            )
            
            if data_response.status_code == 200:
                data = data_response.json()
                if data:
                    print(f"   Структура полей: {list(data[0].keys())}")
                else:
                    print(f"   Таблица пустая")
            else:
                print(f"   Ошибка получения данных: {data_response.status_code}")
        else:
            print(f"❌ Таблица {table_name} недоступна: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ошибка при проверке таблицы {table_name}: {e}")

def check_storage_bucket():
    """Проверяет доступ к Storage bucket"""
    try:
        response = requests.get(
            f"{SUPABASE_URL}/storage/v1/bucket/gtm-assets-public",
            headers=HEADERS
        )
        
        if response.status_code == 200:
            print("✅ Storage bucket gtm-assets-public доступен")
        else:
            print(f"❌ Storage bucket недоступен: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ошибка при проверке Storage: {e}")

def main():
    """Основная функция"""
    print("🔍 Проверяем структуру Supabase...")
    
    # Проверяем основные таблицы
    tables = ['artists', 'products', 'users', 'categories']
    
    for table in tables:
        print(f"\n📋 Проверяем таблицу {table}...")
        check_table_structure(table)
    
    print(f"\n📦 Проверяем Storage...")
    check_storage_bucket()

if __name__ == "__main__":
    main() 