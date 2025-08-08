#!/usr/bin/env python3
"""
GTM WebApp Handler
Обработка взаимодействий с веб-приложением
"""

import os
import logging
import random
import string
import aiohttp
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from dotenv import load_dotenv
import psycopg2

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Конфигурация
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://gtm_user:gtm_secure_password_2024@postgres:5432/gtm_db')
WEBAPP_URL = os.getenv('WEBAPP_URL', 'https://gtm.baby')
API_BASE_URL = os.getenv('API_BASE_URL', 'http://api:8000')
TELEGRAM_FOLDER_LINK = os.getenv('TELEGRAM_FOLDER_LINK', 'https://t.me/addlist/qRX5VmLZF7E3M2U9')

class WebAppHandler:
    def __init__(self):
        self.database_url = DATABASE_URL
        self.webapp_url = WEBAPP_URL
        self.api_base_url = API_BASE_URL
        self.telegram_folder_link = TELEGRAM_FOLDER_LINK
        
    async def get_total_tickets_from_db(self) -> dict:
        """Получить общее количество билетов из БД"""
        try:
            conn = psycopg2.connect(self.database_url)
            cursor = conn.cursor()
            
            # Получаем общее количество билетов из таблицы users
            cursor.execute("""
                SELECT SUM(tickets_count) as total_tickets FROM users
            """)
            
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            
            total_tickets = result[0] if result and result[0] else 0
            
            return {'total_tickets': total_tickets}
            
        except Exception as e:
            logger.error(f"Ошибка получения общего количества билетов из БД: {e}")
            return {'total_tickets': 0}
            
    async def get_user_tickets_from_api(self, user_id: int) -> dict:
        """Получить билеты пользователя из API"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.api_base_url}/api/tickets/user/{user_id}") as response:
                    if response.status == 200:
                        data = await response.json()
                        return data
                    else:
                        logger.error(f"API вернул статус {response.status} для пользователя {user_id}")
                        return None
        except Exception as e:
            logger.error(f"Ошибка получения билетов пользователя: {e}")
            return None
            
    def get_telegram_folder_link(self) -> str:
        """Получить ссылку на Telegram папку"""
        return self.telegram_folder_link
        
    def generate_referral_code(self) -> str:
        """Генерировать уникальный реферальный код"""
        # Генерируем код в формате: refGTM + 7 случайных символов
        random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
        return f"refGTM{random_chars}"
        
    async def get_or_create_referral_code(self, user_id: int) -> str:
        """Получить или создать реферальный код для пользователя"""
        try:
            conn = psycopg2.connect(self.database_url)
            cursor = conn.cursor()
            
            # Проверяем, есть ли уже код у пользователя
            cursor.execute("""
                SELECT referral_code FROM users WHERE telegram_id = %s
            """, (user_id,))
            
            result = cursor.fetchone()
            
            if result and result[0]:
                # Код уже существует
                referral_code = result[0]
            else:
                # Генерируем новый код
                referral_code = self.generate_referral_code()
                
                # Проверяем уникальность кода
                while True:
                    cursor.execute("""
                        SELECT telegram_id FROM users WHERE referral_code = %s
                    """, (referral_code,))
                    
                    if not cursor.fetchone():
                        break
                    referral_code = self.generate_referral_code()
                
                # Сохраняем код
                cursor.execute("""
                    UPDATE users SET referral_code = %s WHERE telegram_id = %s
                """, (referral_code, user_id))
                
                conn.commit()
            
            cursor.close()
            conn.close()
            
            return referral_code
            
        except Exception as e:
            logger.error(f"Ошибка получения/создания реферального кода: {e}")
            return f"refGTM{user_id}"  # Fallback
            
    def get_invite_keyboard(self, referral_code: str):
        """Создать клавиатуру для приглашения друзей"""
        keyboard = [
            [
                InlineKeyboardButton(
                    text="🃏 Пригласить друзей",
                    web_app=WebAppInfo(url=f"{self.webapp_url}/invite?ref={referral_code}")
                ),
                InlineKeyboardButton(
                    text="🎰 Моя статистика",
                    callback_data="my_stats"
                )
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
        
    def get_invite_message(self, user_first_name: str, referral_code: str) -> str:
        """Создать сообщение для приглашения друзей"""
        invite_text = f"""🎰 <b>Пригласи друзей в GTM!</b>

👋 Привет, {user_first_name}! 

🎲 Присоединяйся — и будь в игре 🎲
#GTM #GothamsTopModel #Giveaway

🎫 За каждого приглашенного друга ты получишь +1 билет в розыгрыш!

🔗 Твоя реферальная ссылка:
<pre>https://t.me/GTM_ROBOT?start={referral_code}</pre>"""
        
        return invite_text
        
    async def add_referral_ticket_by_code(self, referral_code: str):
        """Добавить билет за реферала по коду"""
        try:
            conn = psycopg2.connect(self.database_url)
            cursor = conn.cursor()
            
            # Находим пользователя по реферальному коду
            cursor.execute("""
                SELECT telegram_id, tickets_count FROM users WHERE referral_code = %s
            """, (referral_code,))
            
            result = cursor.fetchone()
            
            if result:
                referrer_id, current_tickets = result
                
                # Проверяем, не превышает ли количество билетов лимит (10 реферальных + 1 за подписку)
                if current_tickets < 11:  # Максимум 11 билетов (10 реферальных + 1 за подписку)
                    # Добавляем билет рефереру
                    cursor.execute("""
                        UPDATE users 
                        SET tickets_count = tickets_count + 1
                        WHERE telegram_id = %s
                    """, (referrer_id,))
                    
                    conn.commit()
                    logger.info(f"Начислен билет за реферала по коду {referral_code}: {referrer_id}")
                else:
                    logger.info(f"Пользователь {referrer_id} уже имеет максимальное количество билетов")
            else:
                logger.warning(f"Реферальный код не найден: {referral_code}")
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            logger.error(f"Ошибка добавления билета за реферала по коду: {e}")
            
    async def get_user_stats(self, user_id: int) -> dict:
        """Получить статистику пользователя"""
        try:
            conn = psycopg2.connect(self.database_url)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT tickets_count, has_subscription_ticket, referral_code 
                FROM users WHERE telegram_id = %s
            """, (user_id,))
            
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if result:
                tickets_count, has_subscription_ticket, referral_code = result
                referral_tickets = max(0, tickets_count - (1 if has_subscription_ticket else 0))
                
                return {
                    'total_tickets': tickets_count,
                    'subscription_tickets': 1 if has_subscription_ticket else 0,
                    'referral_tickets': referral_tickets,
                    'referral_code': referral_code or f"refGTM{user_id}"
                }
            else:
                return {
                    'total_tickets': 0,
                    'subscription_tickets': 0,
                    'referral_tickets': 0,
                    'referral_code': f"refGTM{user_id}"
                }
                
        except Exception as e:
            logger.error(f"Ошибка получения статистики пользователя: {e}")
            return {
                'total_tickets': 0,
                'subscription_tickets': 0,
                'referral_tickets': 0,
                'referral_code': f"refGTM{user_id}"
            }
            
    async def simulate_ai_search(self, category: str) -> dict:
        """Имитация AI поиска по фото"""
        # Список артистов по категориям
        artists_by_category = {
            'tattoo': [
                {'name': 'Alena'},
                {'name': 'EMI'},
                {'name': 'Lin++'},
                {'name': 'MurderDoll'},
                {'name': 'BloodiVamp'}
            ],
            'piercing': [
                {'name': 'Чучундра'},
                {'name': 'naidenka'},
                {'name': 'Потеряшка'}
            ],
            'hair': [
                {'name': 'Gothams Top Model'},
                {'name': 'Режь меня всерьёз'}
            ]
        }
        
        # Выбираем случайного артиста из категории
        if category in artists_by_category:
            artist = random.choice(artists_by_category[category])
            return {
                'success': True,
                'artist': artist,
                'category': category,
                'message': f"AI нашел идеального артиста для вашего запроса!"
            }
        else:
            return {
                'success': False,
                'message': f"Категория '{category}' не найдена"
            } 