#!/usr/bin/env python3
"""
GTM Simple Bot для локального тестирования
Упрощенная версия без сложных зависимостей
"""

import os
import logging
import asyncio
import random
import string
from datetime import datetime
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Конфигурация
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

# Проверка конфигурации
if not all([TELEGRAM_BOT_TOKEN, SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY]):
    print("❌ Не все переменные окружения установлены!")
    print("📝 Проверьте файл .env")
    exit(1)

# Импорт telegram только если доступен
try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
    TELEGRAM_AVAILABLE = True
except ImportError:
    print("⚠️ python-telegram-bot не установлен")
    print("📦 Установите: pip install python-telegram-bot")
    TELEGRAM_AVAILABLE = False

# Импорт requests для Supabase
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    print("⚠️ requests не установлен")
    print("📦 Установите: pip install requests")
    REQUESTS_AVAILABLE = False

class SimpleSupabaseClient:
    """Упрощенный клиент для Supabase"""
    
    def __init__(self):
        self.base_url = SUPABASE_URL
        self.service_key = SUPABASE_SERVICE_ROLE_KEY
        self.headers = {
            'apikey': self.service_key,
            'Authorization': f'Bearer {self.service_key}',
            'Content-Type': 'application/json'
        }
    
    def create_user(self, user_data):
        """Создание пользователя"""
        try:
            response = requests.post(
                f"{self.base_url}/rest/v1/users",
                headers=self.headers,
                json=user_data
            )
            return response.status_code == 201
        except Exception as e:
            logger.error(f"Ошибка создания пользователя: {e}")
            return False
    
    def get_user(self, telegram_id):
        """Получение пользователя"""
        try:
            response = requests.get(
                f"{self.base_url}/rest/v1/users?telegram_id=eq.{telegram_id}",
                headers=self.headers
            )
            if response.status_code == 200:
                data = response.json()
                return data[0] if data else None
            return None
        except Exception as e:
            logger.error(f"Ошибка получения пользователя: {e}")
            return None
    
    def update_user(self, telegram_id, user_data):
        """Обновление пользователя"""
        try:
            response = requests.patch(
                f"{self.base_url}/rest/v1/users?telegram_id=eq.{telegram_id}",
                headers=self.headers,
                json=user_data
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Ошибка обновления пользователя: {e}")
            return False
    
    def add_user_ticket(self, telegram_id):
        """Добавление билета пользователю"""
        user = self.get_user(telegram_id)
        if user:
            new_tickets = user.get('tickets_count', 0) + 1
            return self.update_user(telegram_id, {'tickets_count': new_tickets})
        return False
    
    def get_user_tickets(self, telegram_id):
        """Получение количества билетов"""
        user = self.get_user(telegram_id)
        return user.get('tickets_count', 0) if user else 0

class SimpleGTMBot:
    """Упрощенный GTM бот"""
    
    def __init__(self):
        if not TELEGRAM_AVAILABLE:
            print("❌ Telegram библиотека недоступна")
            return
        
        self.application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        self.supabase = SimpleSupabaseClient()
        self.setup_handlers()
        
    def setup_handlers(self):
        """Настройка обработчиков команд"""
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("tickets", self.show_tickets))
        self.application.add_handler(CommandHandler("test", self.test_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user = update.effective_user
        
        welcome_message = f"""☠️ Привет, {user.first_name}! ☠️

👄 Добро пожаловать во Gotham's Top Model!

Это тестовая версия бота с Supabase интеграцией.

Команды:
/tickets - Показать билеты
/test - Тест Supabase
/help - Помощь"""
        
        await update.message.reply_text(welcome_message)
        
        # Сохраняем пользователя в Supabase
        user_data = {
            'telegram_id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'tickets_count': 0,
            'has_subscription_ticket': False
        }
        
        if self.supabase.create_user(user_data):
            await update.message.reply_text("✅ Пользователь сохранен в Supabase")
        else:
            await update.message.reply_text("❌ Ошибка сохранения в Supabase")
    
    async def show_tickets(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать количество билетов"""
        user = update.effective_user
        tickets = self.supabase.get_user_tickets(user.id)
        
        message = f"""🎫 Билеты пользователя {user.first_name}

📊 Ваши билеты: {tickets}

🎁 Участвуйте в розыгрыше GTM!"""
        await update.message.reply_text(message)
    
    async def test_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Тестовая команда"""
        user = update.effective_user
        
        # Добавляем тестовый билет
        if self.supabase.add_user_ticket(user.id):
            await update.message.reply_text("✅ Тестовый билет добавлен!")
        else:
            await update.message.reply_text("❌ Ошибка добавления билета")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Помощь"""
        help_text = """🤖 GTM Simple Bot - Помощь

📋 Команды:
/start - Начать работу с ботом
/tickets - Показать количество билетов
/test - Добавить тестовый билет
/help - Показать эту справку

🎫 Это тестовая версия с Supabase интеграцией!"""
        await update.message.reply_text(help_text)
    
    def run(self):
        """Запуск бота"""
        if not TELEGRAM_AVAILABLE:
            print("❌ Telegram библиотека недоступна")
            return
        
        logger.info("🚀 Запуск GTM Simple Bot...")
        self.application.run_polling()

def test_supabase_connection():
    """Тест подключения к Supabase"""
    print("🔍 Тестирование Supabase подключения...")
    
    try:
        response = requests.get(f"{SUPABASE_URL}/rest/v1/", headers={
            'apikey': SUPABASE_ANON_KEY,
            'Authorization': f'Bearer {SUPABASE_ANON_KEY}'
        })
        
        if response.status_code == 200:
            print("✅ Supabase подключение успешно")
            return True
        else:
            print(f"❌ Supabase ошибка: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка подключения к Supabase: {e}")
        return False

def main():
    """Основная функция"""
    print("🚀 GTM Simple Bot")
    print("=================")
    
    # Проверка зависимостей
    if not REQUESTS_AVAILABLE:
        print("❌ requests не установлен")
        return
    
    # Тест Supabase
    if not test_supabase_connection():
        print("❌ Не удалось подключиться к Supabase")
        return
    
    # Запуск бота
    if TELEGRAM_AVAILABLE:
        bot = SimpleGTMBot()
        bot.run()
    else:
        print("❌ Telegram библиотека недоступна")
        print("📦 Установите: pip install python-telegram-bot")

if __name__ == "__main__":
    main() 