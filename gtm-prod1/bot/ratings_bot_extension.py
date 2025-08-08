#!/usr/bin/env python3
"""
Расширение для bot_main.py - команды рейтинга артистов
"""

import requests
import json
import re
from telegram import Update
from telegram.ext import ContextTypes

# Конфигурация Supabase
SUPABASE_URL = "https://rxmtovqxjsvogyywyrha.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1Mjg1NTAsImV4cCI6MjA3MDEwNDU1MH0.gDkJybktFoi486hbIVwppDfmVQlAR0fM4o4Sl1-AxhE"

headers = {
    'apikey': SUPABASE_ANON_KEY,
    'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
    'Content-Type': 'application/json'
}

class RatingService:
    """Сервис для работы с рейтингами артистов"""
    
    @staticmethod
    async def add_rating(artist_name: str, user_id: str, rating: int, comment: str = None) -> dict:
        """Добавляет или обновляет рейтинг артиста"""
        try:
            response = requests.post(
                f"{SUPABASE_URL}/rest/v1/rpc/add_artist_rating",
                headers=headers,
                json={
                    "artist_name_param": artist_name,
                    "user_id_param": str(user_id),
                    "rating_param": rating,
                    "comment_param": comment
                }
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"success": False, "error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def get_rating(artist_name: str) -> dict:
        """Получает рейтинг артиста"""
        try:
            response = requests.post(
                f"{SUPABASE_URL}/rest/v1/rpc/get_artist_rating",
                headers=headers,
                json={"artist_name_param": artist_name}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    async def get_all_artists() -> list:
        """Получает список всех артистов"""
        try:
            response = requests.get(
                f"{SUPABASE_URL}/rest/v1/artists?select=name&is_active=eq.true",
                headers=headers
            )
            
            if response.status_code == 200:
                return [artist["name"] for artist in response.json()]
            else:
                return []
                
        except Exception as e:
            return []

# Команды для добавления в GTMBot
async def rate_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для оценки артиста"""
    user = update.effective_user
    
    if not context.args or len(context.args) < 2:
        help_text = """⭐ Команда для оценки артиста

🔹 Использование:
/rate <имя_артиста> <оценка> [комментарий]

🔹 Примеры:
/rate Lin++ 5
/rate "Чучундра" 4 "Отличная работа!"
/rate EMI 5 "Супер тату!"

🔹 Оценка: от 1 до 5 звезд
🔹 Комментарий: необязательно

📋 Доступные артисты: /artists"""
        
        await update.message.reply_text(help_text)
        return
    
    try:
        # Парсим аргументы
        artist_name = context.args[0]
        rating = int(context.args[1])
        comment = " ".join(context.args[2:]) if len(context.args) > 2 else None
        
        # Валидация
        if rating < 1 or rating > 5:
            await update.message.reply_text("❌ Оценка должна быть от 1 до 5 звезд")
            return
        
        # Добавляем рейтинг
        result = await RatingService.add_rating(artist_name, user.id, rating, comment)
        
        if result.get("success"):
            stars = "⭐" * rating
            response = f"""✅ Ваша оценка сохранена!

🎨 Артист: {artist_name}
{stars} ({rating}/5)"""
            
            if comment:
                response += f"\n💬 Комментарий: {comment}"
            
            # Показываем обновленную статистику
            rating_info = await RatingService.get_rating(artist_name)
            if not rating_info.get("error"):
                avg_rating = rating_info.get("average_rating", 0)
                total_ratings = rating_info.get("total_ratings", 0)
                
                response += f"\n\n📊 Общая статистика:"
                response += f"\n⭐ Средний рейтинг: {avg_rating:.1f}/5"
                response += f"\n🗳️ Всего оценок: {total_ratings}"
            
            await update.message.reply_text(response)
        else:
            error_msg = result.get("error", "Неизвестная ошибка")
            if "Artist not found" in error_msg:
                await update.message.reply_text(f"❌ Артист '{artist_name}' не найден\n\n📋 Список артистов: /artists")
            else:
                await update.message.reply_text(f"❌ Ошибка при сохранении оценки: {error_msg}")
                
    except ValueError:
        await update.message.reply_text("❌ Оценка должна быть числом от 1 до 5")
    except Exception as e:
        await update.message.reply_text(f"❌ Произошла ошибка: {e}")

async def rating_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для просмотра рейтинга артиста"""
    
    if not context.args:
        await update.message.reply_text("📊 Использование: /rating <имя_артиста>\n\nПример: /rating Lin++")
        return
    
    artist_name = " ".join(context.args)
    
    try:
        rating_info = await RatingService.get_rating(artist_name)
        
        if rating_info.get("error"):
            await update.message.reply_text(f"❌ Артист '{artist_name}' не найден\n\n📋 Список артистов: /artists")
            return
        
        avg_rating = rating_info.get("average_rating", 0)
        total_ratings = rating_info.get("total_ratings", 0)
        
        if total_ratings == 0:
            response = f"""📊 Рейтинг артиста {artist_name}

⭐ Оценок пока нет
💭 Станьте первым, кто оценит этого артиста!

Оценить: /rate {artist_name} <1-5>"""
        else:
            stars = "⭐" * int(round(avg_rating))
            response = f"""📊 Рейтинг артиста {artist_name}

{stars} {avg_rating:.1f}/5
🗳️ Всего оценок: {total_ratings}

Оценить: /rate {artist_name} <1-5>"""
        
        await update.message.reply_text(response)
        
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка при получении рейтинга: {e}")

async def artists_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для показа списка всех артистов"""
    
    try:
        artists = await RatingService.get_all_artists()
        
        if not artists:
            await update.message.reply_text("❌ Не удалось загрузить список артистов")
            return
        
        # Группируем артистов по алфавиту
        artists_sorted = sorted(artists)
        
        response = "🎨 **Артисты GTM:**\n\n"
        
        for i, artist in enumerate(artists_sorted, 1):
            response += f"{i}. {artist}\n"
        
        response += f"\n📊 Всего артистов: {len(artists)}"
        response += f"\n\n⭐ Оценить: /rate <имя> <1-5>"
        response += f"\n📈 Рейтинг: /rating <имя>"
        
        await update.message.reply_text(response)
        
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка при получении списка артистов: {e}")

# Инструкции для интеграции в bot_main.py
"""
Для интеграции в bot_main.py добавьте в метод setup_handlers():

self.application.add_handler(CommandHandler("rate", self.rate_command))
self.application.add_handler(CommandHandler("rating", self.rating_command))  
self.application.add_handler(CommandHandler("artists", self.artists_command))

И добавьте методы в класс GTMBot:

async def rate_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    await rate_command(self, update, context)
    
async def rating_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    await rating_command(self, update, context)
    
async def artists_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    await artists_command(self, update, context)
"""