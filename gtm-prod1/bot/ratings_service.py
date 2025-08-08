#!/usr/bin/env python3
"""
Сервис для работы с рейтингами артистов в Supabase
"""

import requests
import json
from typing import Optional, Dict, Any

# Supabase конфигурация
SUPABASE_URL = "https://rxmtovqxjsvogyywyrha.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1Mjg1NTAsImV4cCI6MjA3MDEwNDU1MH0.gDkJybktFoi486hbIVwppDfmVQlAR0fM4o4Sl1-AxhE"

class RatingsService:
    """Сервис для работы с рейтингами"""
    
    def __init__(self):
        self.base_url = SUPABASE_URL
        self.headers = {
            'apikey': SUPABASE_ANON_KEY,
            'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
            'Content-Type': 'application/json',
        }
    
    def add_or_update_rating(self, artist_name: str, user_id: str, rating: int, comment: str = None) -> Dict[str, Any]:
        """
        Добавляет или обновляет оценку артиста
        
        Args:
            artist_name: Имя артиста
            user_id: Telegram ID пользователя  
            rating: Оценка от 1 до 5
            comment: Комментарий (опционально)
        
        Returns:
            Результат операции
        """
        try:
            # Сначала найдем ID артиста по имени
            artist_id = self._get_artist_id_by_name(artist_name)
            if not artist_id:
                return {
                    'success': False,
                    'error': f'Артист {artist_name} не найден'
                }
            
            # Вызываем RPC функцию для добавления/обновления оценки
            url = f"{self.base_url}/rest/v1/rpc/add_or_update_rating"
            
            payload = {
                'artist_id_param': artist_id,
                'user_id_param': str(user_id),
                'rating_param': rating,
                'comment_param': comment
            }
            
            response = requests.post(url, json=payload, headers=self.headers)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Рейтинг добавлен/обновлен для {artist_name}: {rating}/5")
                return result
            else:
                error_msg = f"Ошибка API: {response.status_code} - {response.text}"
                print(f"❌ {error_msg}")
                return {
                    'success': False,
                    'error': error_msg
                }
                
        except Exception as e:
            error_msg = f"Ошибка при добавлении рейтинга: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                'success': False,
                'error': error_msg
            }
    
    def get_artist_ratings(self, artist_name: str) -> Dict[str, Any]:
        """
        Получает рейтинги артиста
        
        Args:
            artist_name: Имя артиста
        
        Returns:
            Данные о рейтингах
        """
        try:
            # Найдем ID артиста по имени
            artist_id = self._get_artist_id_by_name(artist_name)
            if not artist_id:
                return {
                    'success': False,
                    'error': f'Артист {artist_name} не найден'
                }
            
            # Вызываем RPC функцию для получения рейтингов
            url = f"{self.base_url}/rest/v1/rpc/get_artist_ratings"
            
            payload = {
                'artist_id_param': artist_id
            }
            
            response = requests.post(url, json=payload, headers=self.headers)
            
            if response.status_code == 200:
                result = response.json()
                print(f"📊 Рейтинг {artist_name}: {result.get('average_rating', 0)}/5 ({result.get('total_ratings', 0)} оценок)")
                return {
                    'success': True,
                    'data': result
                }
            else:
                error_msg = f"Ошибка API: {response.status_code} - {response.text}"
                print(f"❌ {error_msg}")
                return {
                    'success': False,
                    'error': error_msg
                }
                
        except Exception as e:
            error_msg = f"Ошибка при получении рейтингов: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                'success': False,
                'error': error_msg
            }
    
    def _get_artist_id_by_name(self, artist_name: str) -> Optional[int]:
        """
        Получает ID артиста по имени
        
        Args:
            artist_name: Имя артиста
        
        Returns:
            ID артиста или None если не найден
        """
        try:
            url = f"{self.base_url}/rest/v1/artists?select=id&name=eq.{artist_name}"
            
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    return data[0]['id']
            
            return None
            
        except Exception as e:
            print(f"❌ Ошибка при поиске артиста {artist_name}: {str(e)}")
            return None
    
    def get_top_rated_artists(self, limit: int = 10) -> Dict[str, Any]:
        """
        Получает топ артистов по рейтингу
        
        Args:
            limit: Количество артистов
        
        Returns:
            Список топ артистов
        """
        try:
            url = f"{self.base_url}/rest/v1/artists?select=name,average_rating,total_ratings&order=average_rating.desc,total_ratings.desc&limit={limit}"
            
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                artists = response.json()
                print(f"🏆 Топ {len(artists)} артистов по рейтингу:")
                for i, artist in enumerate(artists, 1):
                    print(f"  {i}. {artist['name']} - {artist['average_rating']}/5 ({artist['total_ratings']} оценок)")
                
                return {
                    'success': True,
                    'data': artists
                }
            else:
                error_msg = f"Ошибка API: {response.status_code} - {response.text}"
                print(f"❌ {error_msg}")
                return {
                    'success': False,
                    'error': error_msg
                }
                
        except Exception as e:
            error_msg = f"Ошибка при получении топа: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                'success': False,
                'error': error_msg
            }

# Функция для интеграции в бота
def handle_rating_command(user_id: str, artist_name: str, rating: int, comment: str = None) -> str:
    """
    Обработчик команды оценки для бота
    
    Args:
        user_id: Telegram ID пользователя
        artist_name: Имя артиста
        rating: Оценка от 1 до 5
        comment: Комментарий
    
    Returns:
        Текст ответа для пользователя
    """
    service = RatingsService()
    
    # Валидация рейтинга
    if not 1 <= rating <= 5:
        return "❌ Оценка должна быть от 1 до 5 звезд"
    
    # Добавляем/обновляем оценку
    result = service.add_or_update_rating(artist_name, user_id, rating, comment)
    
    if result.get('success'):
        action = result.get('action', 'unknown')
        if action == 'created':
            response = f"✅ Спасибо за оценку! Вы поставили {rating}⭐ артисту {artist_name}"
        else:
            prev_rating = result.get('previous_rating', 0)
            response = f"✅ Оценка обновлена! Было {prev_rating}⭐, стало {rating}⭐ для {artist_name}"
        
        if comment:
            response += f"\nКомментарий: {comment}"
        
        # Получаем обновленную статистику
        ratings_data = service.get_artist_ratings(artist_name)
        if ratings_data.get('success'):
            data = ratings_data['data']
            avg_rating = data.get('average_rating', 0)
            total_ratings = data.get('total_ratings', 0)
            response += f"\n\n📊 Текущий рейтинг {artist_name}: {avg_rating:.1f}⭐ ({total_ratings} оценок)"
        
        return response
    else:
        error = result.get('error', 'Неизвестная ошибка')
        return f"❌ Не удалось добавить оценку: {error}"

# Тестирование
if __name__ == "__main__":
    service = RatingsService()
    
    print("🧪 Тестирование системы рейтингов...")
    
    # Тест 1: Добавление оценки
    print("\n1. Добавление оценки для Чучундра...")
    result1 = service.add_or_update_rating("Чучундра", "123456789", 5, "Отличная работа!")
    print(f"Результат: {result1}")
    
    # Тест 2: Получение рейтингов
    print("\n2. Получение рейтингов Чучундра...")
    result2 = service.get_artist_ratings("Чучундра")
    print(f"Результат: {result2}")
    
    # Тест 3: Обновление оценки
    print("\n3. Обновление оценки для Чучундра...")
    result3 = service.add_or_update_rating("Чучундра", "123456789", 4, "Хорошо, но можно лучше")
    print(f"Результат: {result3}")
    
    # Тест 4: Топ артистов
    print("\n4. Топ артистов...")
    result4 = service.get_top_rated_artists(5)
    print(f"Результат: {result4}")
    
    print("\n✅ Тестирование завершено!")