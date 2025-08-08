#!/usr/bin/env python3
"""
Скрипт для обновления базы данных GTM Bot
"""

import os
import psycopg2
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Конфигурация
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://gtm_user:gtm_secure_password_2024@postgres:5432/gtm_db')

def update_database():
    """Обновление структуры базы данных"""
    try:
        # Подключаемся к базе данных
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        print("🔄 Обновление базы данных...")
        
        # Добавляем поле для отслеживания билета за подписки
        cursor.execute("""
            ALTER TABLE users ADD COLUMN IF NOT EXISTS has_subscription_ticket BOOLEAN DEFAULT FALSE
        """)
        print("✅ Добавлено поле has_subscription_ticket")
        
        # Добавляем поле для времени создания пользователя
        cursor.execute("""
            ALTER TABLE users ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        """)
        print("✅ Добавлено поле created_at")
        
        # Добавляем поле для реферального кода
        cursor.execute("""
            ALTER TABLE users ADD COLUMN IF NOT EXISTS referral_code VARCHAR(20) UNIQUE
        """)
        print("✅ Добавлено поле referral_code")
        
        # Обновляем существующие записи
        cursor.execute("""
            UPDATE users 
            SET has_subscription_ticket = TRUE 
            WHERE tickets_count > 0 AND has_subscription_ticket IS NULL
        """)
        print("✅ Обновлены существующие записи")
        
        # Создаем индексы
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_users_has_subscription_ticket ON users(has_subscription_ticket)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_users_referral_code ON users(referral_code)
        """)
        print("✅ Созданы индексы")
        
        # Проверяем структуру таблицы
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default 
            FROM information_schema.columns 
            WHERE table_name = 'users' 
            ORDER BY ordinal_position
        """)
        
        columns = cursor.fetchall()
        print("\n📋 Структура таблицы users:")
        for column in columns:
            print(f"  • {column[0]} ({column[1]}) - {'NULL' if column[2] == 'YES' else 'NOT NULL'}")
        
        # Сохраняем изменения
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n✅ База данных успешно обновлена!")
        
    except Exception as e:
        print(f"❌ Ошибка обновления базы данных: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()

if __name__ == "__main__":
    update_database() 