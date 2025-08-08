#!/usr/bin/env python3
"""
GTM Supabase Debug Script
Скрипт для диагностики подключения к Supabase
"""
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# Конфигурация
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

def test_supabase_connection():
    print("🔍 Диагностика Supabase подключения...")
    print(f"URL: {SUPABASE_URL}")
    print(f"Anon Key: {SUPABASE_ANON_KEY[:20]}...")
    print(f"Service Key: {SUPABASE_SERVICE_ROLE_KEY[:20]}...")
    
    # Тест 1: Проверка API с anon key
    print("\n📡 Тест 1: API с anon key")
    headers = {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(f'{SUPABASE_URL}/rest/v1/', headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    # Тест 2: Проверка таблицы users с anon key
    print("\n👥 Тест 2: Таблица users (anon key)")
    try:
        response = requests.get(f'{SUPABASE_URL}/rest/v1/users?select=*&limit=1', headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    # Тест 3: Проверка с service role key
    print("\n🔐 Тест 3: API с service role key")
    service_headers = {
        'apikey': SUPABASE_SERVICE_ROLE_KEY,
        'Authorization': f'Bearer {SUPABASE_SERVICE_ROLE_KEY}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(f'{SUPABASE_URL}/rest/v1/users?select=*&limit=1', headers=service_headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    # Тест 4: Проверка Storage
    print("\n📦 Тест 4: Storage bucket")
    try:
        response = requests.get(f'{SUPABASE_URL}/storage/v1/bucket/list', headers=service_headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    test_supabase_connection() 