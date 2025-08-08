#!/usr/bin/env python3
"""
GTM Supabase Test Script
Простой тест для проверки подключения к Supabase
"""

import os
import sys
import requests
import json
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def test_supabase_connection():
    """Тест подключения к Supabase"""
    print("🔍 Тестирование подключения к Supabase...")
    
    # Получаем конфигурацию
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_anon_key = os.getenv('SUPABASE_ANON_KEY')
    supabase_service_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
    
    if not all([supabase_url, supabase_anon_key, supabase_service_key]):
        print("❌ Не все переменные окружения установлены!")
        print("📝 Проверьте файл .env")
        return False
    
    headers = {
        'apikey': supabase_anon_key,
        'Authorization': f'Bearer {supabase_anon_key}',
        'Content-Type': 'application/json'
    }
    
    try:
        # Тест 1: Проверка подключения к API
        print("📡 Тест 1: Проверка API подключения...")
        response = requests.get(f"{supabase_url}/rest/v1/", headers=headers)
        
        if response.status_code == 200:
            print("✅ API подключение успешно")
        else:
            print(f"❌ API ошибка: {response.status_code}")
            return False
        
        # Тест 2: Проверка таблицы users
        print("👥 Тест 2: Проверка таблицы users...")
        response = requests.get(f"{supabase_url}/rest/v1/users?select=count", headers=headers)
        
        if response.status_code == 200:
            print("✅ Таблица users доступна")
        else:
            print(f"❌ Ошибка таблицы users: {response.status_code}")
            return False
        
        # Тест 3: Проверка Storage
        print("📁 Тест 3: Проверка Storage...")
        response = requests.get(f"{supabase_url}/storage/v1/bucket/gtm-assets", headers=headers)
        
        if response.status_code == 200:
            print("✅ Storage bucket gtm-assets доступен")
        else:
            print(f"❌ Ошибка Storage: {response.status_code}")
            return False
        
        print("🎉 Все тесты прошли успешно!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False

def test_telegram_bot():
    """Тест Telegram бота"""
    print("\n🤖 Тестирование Telegram бота...")
    
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        print("❌ TELEGRAM_BOT_TOKEN не установлен!")
        return False
    
    try:
        # Проверка бота через API
        response = requests.get(f"https://api.telegram.org/bot{bot_token}/getMe")
        
        if response.status_code == 200:
            bot_info = response.json()
            if bot_info.get('ok'):
                print(f"✅ Бот подключен: @{bot_info['result']['username']}")
                return True
            else:
                print("❌ Ошибка бота")
                return False
        else:
            print(f"❌ Ошибка API Telegram: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка подключения к Telegram: {e}")
        return False

def create_test_data():
    """Создание тестовых данных"""
    print("\n📝 Создание тестовых данных...")
    
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_service_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
    
    headers = {
        'apikey': supabase_service_key,
        'Authorization': f'Bearer {supabase_service_key}',
        'Content-Type': 'application/json'
    }
    
    try:
        # Создание тестового пользователя
        test_user = {
            'telegram_id': 123456789,
            'username': 'test_user',
            'first_name': 'Test',
            'last_name': 'User',
            'tickets_count': 0,
            'has_subscription_ticket': False
        }
        
        response = requests.post(
            f"{supabase_url}/rest/v1/users",
            headers=headers,
            json=test_user
        )
        
        if response.status_code == 201:
            print("✅ Тестовый пользователь создан")
        else:
            print(f"❌ Ошибка создания пользователя: {response.status_code}")
            return False
        
        # Создание тестового артиста
        test_artist = {
            'name': 'Test Artist',
            'username': 'test_artist',
            'bio': 'Тестовый артист для проверки',
            'avatar_url': f"{supabase_url}/storage/v1/object/public/gtm-assets/avatars/test.jpg",
            'city': 'Москва',
            'specialties': ['Тату', 'Пирсинг'],
            'rating': 4.5,
            'is_active': True
        }
        
        response = requests.post(
            f"{supabase_url}/rest/v1/artists",
            headers=headers,
            json=test_artist
        )
        
        if response.status_code == 201:
            print("✅ Тестовый артист создан")
        else:
            print(f"❌ Ошибка создания артиста: {response.status_code}")
            return False
        
        print("🎉 Тестовые данные созданы успешно!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка создания тестовых данных: {e}")
        return False

def main():
    """Основная функция"""
    print("🚀 GTM Supabase Test Suite")
    print("==========================")
    
    # Проверка .env файла
    if not os.path.exists('.env'):
        print("❌ Файл .env не найден!")
        print("📝 Создайте .env файл на основе env_example.txt")
        return
    
    # Тесты
    tests = [
        test_supabase_connection,
        test_telegram_bot,
        create_test_data
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("📊 Результаты тестов:")
    print(f"✅ Пройдено: {passed}/{total}")
    
    if passed == total:
        print("🎉 Все тесты прошли успешно!")
        print("\n🚀 Система готова к запуску!")
        print("💡 Запустите: ./run_local_supabase.sh")
    else:
        print("❌ Некоторые тесты не прошли")
        print("🔧 Проверьте конфигурацию и попробуйте снова")

if __name__ == "__main__":
    main() 