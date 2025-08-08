#!/usr/bin/env python3
"""
Настройка системы рейтингов в Supabase
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

def add_rating_columns():
    """Добавляем колонки для рейтинга в таблицу artists"""
    print("1. Добавляем колонки average_rating и total_ratings к таблице artists...")
    
    # Проверяем текущую структуру таблицы
    response = requests.get(f"{SUPABASE_URL}/rest/v1/artists?select=*&limit=1", headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data:
            sample_record = data[0]
            if 'average_rating' in sample_record:
                print("✅ Колонки уже существуют")
                return True
            else:
                print("❌ Колонки отсутствуют, но их нельзя добавить через REST API")
                print("   Нужно выполнить ALTER TABLE через SQL Editor в Supabase")
                return False
    return False

def create_rating_function():
    """Создаем RPC функцию для добавления рейтинга"""
    print("2. Создаем RPC функцию add_artist_rating...")
    
    # Создаем простую функцию через API
    function_data = {
        "artist_name": "test",
        "user_id": "123",
        "rating": 5,
        "comment": "test"
    }
    
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/rpc/add_artist_rating",
        headers=headers,
        json=function_data
    )
    
    if response.status_code == 200:
        print("✅ Функция add_artist_rating доступна")
        return True
    else:
        print(f"❌ Функция недоступна: {response.status_code}")
        print("   Нужно создать функцию через SQL Editor")
        return False

def test_ratings_functionality():
    """Тестируем функциональность рейтингов"""
    print("3. Тестируем добавление рейтинга...")
    
    # Пробуем добавить тестовый рейтинг
    test_data = {
        "artist_name": "Lin++",
        "user_id": "test_user_123",
        "rating": 5,
        "comment": "Отличная работа!"
    }
    
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/rpc/add_artist_rating",
        headers=headers,
        json=test_data
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Рейтинг добавлен: {result}")
        return True
    else:
        print(f"❌ Ошибка добавления рейтинга: {response.status_code}")
        return False

def show_manual_setup():
    """Показываем инструкции для ручной настройки"""
    print("\n" + "="*60)
    print("📋 ИНСТРУКЦИИ ДЛЯ РУЧНОЙ НАСТРОЙКИ В SUPABASE")
    print("="*60)
    print("\n1. Откройте Supabase Dashboard -> SQL Editor")
    print("2. Выполните следующий SQL код:")
    print("\n" + "-"*40)
    
    sql_code = '''
-- Добавляем колонки для рейтинга
ALTER TABLE artists ADD COLUMN IF NOT EXISTS average_rating DECIMAL(3,2) DEFAULT 0.0;
ALTER TABLE artists ADD COLUMN IF NOT EXISTS total_ratings INTEGER DEFAULT 0;

-- Создаем таблицу рейтингов
CREATE TABLE IF NOT EXISTS artist_ratings (
  id BIGSERIAL PRIMARY KEY,
  artist_id BIGINT REFERENCES artists(id) ON DELETE CASCADE,
  user_id TEXT NOT NULL,
  rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
  comment TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  UNIQUE(artist_id, user_id)
);

-- Создаем индексы
CREATE INDEX IF NOT EXISTS idx_artist_ratings_artist_id ON artist_ratings(artist_id);
CREATE INDEX IF NOT EXISTS idx_artist_ratings_user_id ON artist_ratings(user_id);

-- Функция для добавления рейтинга
CREATE OR REPLACE FUNCTION add_artist_rating(
  artist_name_param TEXT,
  user_id_param TEXT,
  rating_param INTEGER,
  comment_param TEXT DEFAULT NULL
)
RETURNS JSON AS $$
DECLARE
  target_artist_id BIGINT;
  result JSON;
BEGIN
  -- Находим ID артиста по имени
  SELECT id INTO target_artist_id FROM artists WHERE name = artist_name_param;
  
  IF target_artist_id IS NULL THEN
    RETURN JSON_BUILD_OBJECT('success', false, 'error', 'Artist not found');
  END IF;
  
  -- Добавляем или обновляем рейтинг
  INSERT INTO artist_ratings (artist_id, user_id, rating, comment)
  VALUES (target_artist_id, user_id_param, rating_param, comment_param)
  ON CONFLICT (artist_id, user_id) 
  DO UPDATE SET 
    rating = rating_param,
    comment = comment_param,
    updated_at = now();
  
  -- Пересчитываем средний рейтинг
  UPDATE artists SET 
    average_rating = (
      SELECT COALESCE(AVG(rating), 0)::DECIMAL(3,2) 
      FROM artist_ratings 
      WHERE artist_id = target_artist_id
    ),
    total_ratings = (
      SELECT COUNT(*) 
      FROM artist_ratings 
      WHERE artist_id = target_artist_id
    )
  WHERE id = target_artist_id;
  
  RETURN JSON_BUILD_OBJECT('success', true, 'artist_id', target_artist_id);
END;
$$ LANGUAGE plpgsql;

-- Функция для получения рейтинга артиста
CREATE OR REPLACE FUNCTION get_artist_rating(artist_name_param TEXT)
RETURNS JSON AS $$
DECLARE
  result JSON;
BEGIN
  SELECT JSON_BUILD_OBJECT(
    'artist_name', name,
    'average_rating', COALESCE(average_rating, 0),
    'total_ratings', COALESCE(total_ratings, 0)
  ) INTO result
  FROM artists 
  WHERE name = artist_name_param;
  
  RETURN COALESCE(result, JSON_BUILD_OBJECT('error', 'Artist not found'));
END;
$$ LANGUAGE plpgsql;
'''
    
    print(sql_code)
    print("-"*40)
    print("\n3. После выполнения SQL, запустите этот скрипт снова для тестирования")

def main():
    print("🔧 Настройка системы рейтингов GTM")
    print("="*40)
    
    # Проверяем структуру таблицы
    columns_exist = add_rating_columns()
    
    # Проверяем функции
    function_exists = create_rating_function()
    
    if not columns_exist or not function_exists:
        show_manual_setup()
        return
    
    # Тестируем функциональность
    if test_ratings_functionality():
        print("\n✅ Система рейтингов готова к использованию!")
    else:
        print("\n❌ Есть проблемы с настройкой")

if __name__ == "__main__":
    main()