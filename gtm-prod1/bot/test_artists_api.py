#!/usr/bin/env python3
"""
Тестовый скрипт для проверки API артистов в GTM
Проверяет загрузку артистов из Supabase
"""

import os
import json
import requests
from typing import Dict, List

# Конфигурация Supabase
SUPABASE_URL = "https://rxmtovqxjsvogyywyrha.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1Mjg1NTAsImV4cCI6MjA3MDEwNDU1MH0.gDkJybktFoi486hbIVwppDfmVQlAR0fM4o4Sl1-AxhE"

class SupabaseAPI:
    def __init__(self):
        self.base_url = SUPABASE_URL
        self.headers = {
            'apikey': SUPABASE_ANON_KEY,
            'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
            'Content-Type': 'application/json'
        }
    
    def test_connection(self) -> bool:
        """Тест подключения к Supabase"""
        try:
            response = requests.get(f"{self.base_url}/rest/v1/", headers=self.headers)
            print(f"✅ Подключение к Supabase: {response.status_code}")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Ошибка подключения к Supabase: {e}")
            return False
    
    def get_cities(self) -> List[Dict]:
        """Получение списка городов"""
        try:
            response = requests.get(
                f"{self.base_url}/rest/v1/cities?select=*&is_active=eq.true&order=name.asc",
                headers=self.headers
            )
            if response.status_code == 200:
                cities = response.json()
                print(f"✅ Загружено городов: {len(cities)}")
                for city in cities:
                    print(f"   - {city['name']} ({city['code']}) - население: {city.get('population', 'N/A')}")
                return cities
            else:
                print(f"❌ Ошибка загрузки городов: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Ошибка при получении городов: {e}")
            return []
    
    def get_categories(self) -> List[Dict]:
        """Получение списка категорий"""
        try:
            response = requests.get(
                f"{self.base_url}/rest/v1/categories?select=*&is_active=eq.true&order=name.asc",
                headers=self.headers
            )
            if response.status_code == 200:
                categories = response.json()
                print(f"✅ Загружено категорий: {len(categories)}")
                for cat in categories:
                    print(f"   - {cat['name']} ({cat['type']}) - {cat.get('description', '')}")
                return categories
            else:
                print(f"❌ Ошибка загрузки категорий: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Ошибка при получении категорий: {e}")
            return []
    
    def get_artists_filtered(self, city: str = '', category: str = '') -> List[Dict]:
        """Получение артистов с фильтрацией"""
        try:
            # Используем RPC функцию
            data = {
                'p_city': city,
                'p_category': category,
                'p_limit': 50,
                'p_offset': 0
            }
            
            response = requests.post(
                f"{self.base_url}/rest/v1/rpc/get_artists_filtered",
                headers=self.headers,
                json=data
            )
            
            if response.status_code == 200:
                artists = response.json()
                print(f"✅ Загружено артистов: {len(artists)} (фильтр: город='{city}', категория='{category}')")
                
                for artist in artists:
                    print(f"   - {artist['name']} ({artist.get('city_name', 'N/A')}) - {artist.get('category_name', 'N/A')}")
                    if artist.get('telegram'):
                        print(f"     Telegram: {artist['telegram']}")
                    if artist.get('gallery_urls'):
                        print(f"     Галерея: {len(artist['gallery_urls'])} изображений")
                
                return artists
            else:
                print(f"❌ Ошибка загрузки артистов: {response.status_code}")
                print(f"   Ответ: {response.text}")
                return []
        except Exception as e:
            print(f"❌ Ошибка при получении артистов: {e}")
            return []
    
    def search_chchundra(self) -> List[Dict]:
        """Поиск артиста Чучундра"""
        print("\n🔍 Поиск артиста 'Чучундра'...")
        
        # Поиск по имени через прямой запрос
        try:
            response = requests.get(
                f"{self.base_url}/rest/v1/artists?select=*,cities(name),categories(name,type)&name=ilike.*Чучундра*&is_active=eq.true",
                headers=self.headers
            )
            
            if response.status_code == 200:
                artists = response.json()
                print(f"✅ Найдено записей артиста 'Чучундра': {len(artists)}")
                
                for artist in artists:
                    print(f"   - ID: {artist['id']}")
                    print(f"   - Имя: {artist['name']}")
                    print(f"   - Username: {artist.get('username', 'N/A')}")
                    print(f"   - Город: {artist.get('cities', {}).get('name', 'N/A') if artist.get('cities') else 'N/A'}")
                    print(f"   - Категория: {artist.get('categories', {}).get('name', 'N/A') if artist.get('categories') else 'N/A'}")
                    print(f"   - Рейтинг: {artist.get('rating', 0)}")
                    print(f"   - Telegram: {artist.get('telegram', 'N/A')}")
                    print("   ---")
                
                return artists
            else:
                print(f"❌ Ошибка поиска артиста: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Ошибка при поиске артиста: {e}")
            return []

def main():
    """Главная функция тестирования"""
    print("🧪 GTM Artists API Test")
    print("=" * 50)
    
    api = SupabaseAPI()
    
    # Тест подключения
    print("\n1. Тестирование подключения...")
    if not api.test_connection():
        print("❌ Не удалось подключиться к Supabase. Завершение.")
        return
    
    # Тест городов
    print("\n2. Проверка городов...")
    cities = api.get_cities()
    
    # Тест категорий
    print("\n3. Проверка категорий...")
    categories = api.get_categories()
    
    # Тест артистов
    print("\n4. Проверка всех артистов...")
    all_artists = api.get_artists_filtered()
    
    # Тест фильтрации по Москве
    print("\n5. Проверка артистов в Москве...")
    moscow_artists = api.get_artists_filtered(city='Москва')
    
    # Тест фильтрации по категории Tattoo
    print("\n6. Проверка артистов категории Tattoo...")
    tattoo_artists = api.get_artists_filtered(category='Tattoo')
    
    # Поиск Чучундра
    print("\n7. Поиск артиста 'Чучундра'...")
    chchundra_artists = api.search_chchundra()
    
    # Итоги
    print("\n" + "=" * 50)
    print("📊 ИТОГИ ТЕСТИРОВАНИЯ:")
    print(f"   Городов в БД: {len(cities)}")
    print(f"   Категорий в БД: {len(categories)}")
    print(f"   Всего артистов: {len(all_artists)}")
    print(f"   Артистов в Москве: {len(moscow_artists)}")
    print(f"   Tattoo-артистов: {len(tattoo_artists)}")
    print(f"   Найдено 'Чучундра': {len(chchundra_artists)}")
    
    if len(chchundra_artists) > 0:
        print("✅ Артист 'Чучундра' успешно найден в системе!")
    else:
        print("❌ Артист 'Чучундра' не найден. Нужно добавить в БД.")

if __name__ == "__main__":
    main()