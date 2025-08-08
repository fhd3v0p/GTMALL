#!/usr/bin/env python3
"""
Поиск всех доступных buckets в Supabase
"""

import requests
import json

# Попробуем разные варианты API ключей
API_KEYS = [
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1Mjg1NTAsImV4cCI6MjA3MDEwNDU1MH0.gDkJybktFoi486hbIVwppDfmVQlAR0fM4o4Sl1-AxhE",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzM0MTY5MDcsImV4cCI6MjA0ODk5MjkwN30.B3H8x3q3lPEj7L3lEiOHVWLBNgGEF9bxk3IUJUITpTs"
]

SUPABASE_URL = "https://rxmtovqxjsvogyywyrha.supabase.co"

def try_access_with_key(api_key):
    """Попытка доступа с определенным ключом"""
    headers = {
        'apikey': api_key,
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    print(f"\n🔑 Тестирование ключа: {api_key[:20]}...")
    
    # Проверяем доступ к REST API
    try:
        response = requests.get(f"{SUPABASE_URL}/rest/v1/", headers=headers)
        print(f"   REST API: {response.status_code}")
        if response.status_code != 200:
            return False
    except Exception as e:
        print(f"   REST API ошибка: {e}")
        return False
    
    # Проверяем доступ к Storage API
    try:
        response = requests.get(f"{SUPABASE_URL}/storage/v1/bucket", headers=headers)
        print(f"   Storage API: {response.status_code}")
        
        if response.status_code == 200:
            buckets = response.json()
            print(f"   Buckets найдено: {len(buckets)}")
            for bucket in buckets:
                print(f"      - {bucket['name']} (public: {bucket.get('public', False)})")
            return buckets
        else:
            print(f"   Storage недоступен: {response.text}")
            return False
    except Exception as e:
        print(f"   Storage ошибка: {e}")
        return False

def test_direct_access():
    """Прямое тестирование известных bucket имен"""
    possible_buckets = [
        "gtm-assets",
        "gtm-assets-public", 
        "assets",
        "public",
        "images",
        "uploads"
    ]
    
    print(f"\n🧪 Тестирование прямого доступа к файлам...")
    
    for bucket in possible_buckets:
        test_url = f"{SUPABASE_URL}/storage/v1/object/public/{bucket}/test"
        
        try:
            response = requests.head(test_url)
            print(f"   {bucket}: {response.status_code}")
            if response.status_code != 404:  # Если не 404, возможно bucket существует
                print(f"      ✅ Bucket {bucket} может существовать!")
        except Exception as e:
            print(f"   {bucket}: ошибка {e}")

def main():
    print("🔍 Поиск Supabase Storage buckets")
    print("=" * 40)
    
    # Пробуем разные API ключи
    for api_key in API_KEYS:
        buckets = try_access_with_key(api_key)
        if buckets:
            print(f"\n✅ Найдены buckets с ключом {api_key[:20]}...")
            break
    else:
        print("\n❌ Ни один ключ не дал доступ к buckets")
    
    # Тестируем прямой доступ
    test_direct_access()
    
    print("\n💡 Рекомендации:")
    print("   1. Создать bucket через Supabase Dashboard")
    print("   2. Настроить публичный доступ")
    print("   3. Загрузить файлы через Dashboard")

if __name__ == "__main__":
    main()