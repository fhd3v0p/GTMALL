#!/usr/bin/env python3
"""
Простой тест для проверки таблиц Supabase без RPC функций
"""

import requests
import json

# Конфигурация
SUPABASE_URL = "https://rxmtovqxjsvogyywyrha.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1Mjg1NTAsImV4cCI6MjA3MDEwNDU1MH0.gDkJybktFoi486hbIVwppDfmVQlAR0fM4o4Sl1-AxhE"

headers = {
    'apikey': SUPABASE_ANON_KEY,
    'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
    'Content-Type': 'application/json'
}

def test_table(table_name):
    """Тест таблицы"""
    try:
        response = requests.get(f"{SUPABASE_URL}/rest/v1/{table_name}?select=*", headers=headers)
        print(f"\n🔍 Таблица {table_name}:")
        print(f"   Статус: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Записей: {len(data)}")
            if data:
                print(f"   Пример записи: {data[0]}")
            return data
        else:
            print(f"   Ошибка: {response.text}")
            return []
    except Exception as e:
        print(f"   Исключение: {e}")
        return []

def main():
    print("🧪 Простой тест Supabase таблиц")
    print("=" * 40)
    
    # Тестируем основные таблицы
    cities = test_table("cities")
    categories = test_table("categories") 
    artists = test_table("artists")
    
    print(f"\n📊 ИТОГИ:")
    print(f"   Городов: {len(cities)}")
    print(f"   Категорий: {len(categories)}")
    print(f"   Артистов: {len(artists)}")

if __name__ == "__main__":
    main()