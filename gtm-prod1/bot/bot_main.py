#!/usr/bin/env python3
"""
GTM Telegram Bot
Проверка подписок на каналы и управление билетами
"""

import os
import logging
import asyncio
import random
import string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from dotenv import load_dotenv
import psycopg2
import redis
import json
from webapp_handler import WebAppHandler

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Конфигурация
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '7533650686:AAEU4_nJZHGfzOv9XL4m_fDVt0q3dMDPQX8')
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://gtm_user:gtm_secure_password_2024@postgres:5432/gtm_db')
REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
TELEGRAM_FOLDER_LINK = os.getenv('TELEGRAM_FOLDER_LINK', 'https://t.me/addlist/qRX5VmLZF7E3M2U9')
WEBAPP_URL = os.getenv('WEBAPP_URL', 'https://gtm.baby')

# Каналы подписки (9 каналов)
SUBSCRIPTION_CHANNELS = [
    {'channel_id': -1002088959587, 'channel_username': 'rejmenyavseryoz', 'channel_name': 'Режь меня всерьёз'},
    {'channel_id': -1001971855072, 'channel_username': 'chchndra_tattoo', 'channel_name': 'Чучундра'},
    {'channel_id': -1002133674248, 'channel_username': 'naidenka_tattoo', 'channel_name': 'naidenka_tattoo'},
    {'channel_id': -1001508215942, 'channel_username': 'l1n_ttt', 'channel_name': 'Lin++'},
    {'channel_id': -1001555462429, 'channel_username': 'murderd0lll', 'channel_name': 'MurderdOll'},
    {'channel_id': -1002132954014, 'channel_username': 'poteryashkatattoo', 'channel_name': 'Потеряшка'},
    {'channel_id': -1001689395571, 'channel_username': 'EMI3MO', 'channel_name': 'EMI'},
    {'channel_id': -1001767997947, 'channel_username': 'bloodivamp', 'channel_name': 'bloodivamp'},
    {'channel_id': -1001973736826, 'channel_username': 'G_T_MODEL', 'channel_name': 'Gothams top model'},
]

class GTMBot:
    def __init__(self):
        self.application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        self.webapp_handler = WebAppHandler()
        self.setup_handlers()
        
    def setup_handlers(self):
        """Настройка обработчиков команд"""
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("check", self.check_subscription))
        self.application.add_handler(CommandHandler("tickets", self.show_tickets))
        self.application.add_handler(CommandHandler("folder", self.show_folder))
        self.application.add_handler(CommandHandler("invite", self.invite_command))
        self.application.add_handler(CommandHandler("stats", self.stats_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CallbackQueryHandler(self.handle_callback))
        self.application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^🃏 Пригласить друзей$'), self.handle_invite_button))
        
    def get_webapp_keyboard(self):
        """Создать клавиатуру с кнопками"""
        keyboard = [
            [
                InlineKeyboardButton(
                    text="🔮 Open GTM",
                    web_app=WebAppInfo(url=WEBAPP_URL)
                ),
                InlineKeyboardButton(
                    text="💭 CHAT",
                    url="https://t.me/G_T_MODEL/10"
                )
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user = update.effective_user
        
        # Проверяем реферальную ссылку
        referral_code = None
        if context.args and len(context.args) > 0:
            referral_code = context.args[0]
            # Начисляем билет рефереру, если это новый пользователь
            if await self.is_new_user(user.id):
                await self.webapp_handler.add_referral_ticket_by_code(referral_code)
        
        welcome_message = f"""☠️ Привет, {user.first_name}! ☠️

👄 Добро пожаловать во Gotham's Top Model — платформу для поиска и бронирования лучших артистов в твоем городе!

Что у нас есть:
🤖 AI-поиск услуг по референсам
🃏 Каталог топовых артистов
🎰 Розыгрыш призов на >130,000₽
🎱 Скидка 8% на услуги всех резидентов GTM
💞 Щедрая реферальная система

Нажми «🔮 Open GTM», чтобы ворваться!"""
        
        await update.message.reply_text(
            welcome_message,
            reply_markup=self.get_webapp_keyboard()
        )
        
        # Сохраняем пользователя в БД
        await self.save_user(user)
        
    async def check_subscription(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Проверка подписки на каналы"""
        user = update.effective_user
        chat_id = update.effective_chat.id
        
        await update.message.reply_text("🔍 Проверяю подписки на каналы...")
        
        subscribed_channels = []
        not_subscribed_channels = []
        
        for channel in SUBSCRIPTION_CHANNELS:
            try:
                member = await context.bot.get_chat_member(
                    chat_id=channel['channel_id'],
                    user_id=user.id
                )
                
                if member.status in ['member', 'administrator', 'creator']:
                    subscribed_channels.append(channel)
                else:
                    not_subscribed_channels.append(channel)
                    
            except Exception as e:
                logger.error(f"Ошибка проверки канала {channel['channel_name']}: {e}")
                not_subscribed_channels.append(channel)
        
        # Формируем ответ
        response = "📊 Результаты проверки подписок:\n\n"
        
        if subscribed_channels:
            response += "✅ Подписан на:\n"
            for channel in subscribed_channels:
                response += f"• {channel['channel_name']}\n"
            response += "\n"
        
        if not_subscribed_channels:
            response += "❌ Не подписан на:\n"
            for channel in not_subscribed_channels:
                response += f"• {channel['channel_name']}\n"
            response += "\n"
        
        # Проверяем, подписан ли на все 9 каналов
        if len(subscribed_channels) == 9:
            # Проверяем, не начисляли ли уже билет за подписки
            if not await self.has_subscription_ticket(user.id):
                await self.add_subscription_ticket(user.id)
                response += "🎫 Начислено билетов: +1 (за подписку на все каналы)"
            else:
                response += "✅ Билет за подписки уже начислен"
        else:
            response += f"⚠️ Для получения билета нужно подписаться на все {len(SUBSCRIPTION_CHANNELS)} каналов\n\n"
            response += f"📁 Подпишитесь на папку GTM: {TELEGRAM_FOLDER_LINK}\n"
            response += "🔒 Не отписывайтесь до конца розыгрыша!"
        
        # Показываем текущие билеты пользователя
        user_tickets = await self.get_user_tickets(user.id)
        total_tickets = await self.get_total_tickets()
        response += f"\n🎫 Ваши билеты: {user_tickets}/{total_tickets}"
        
        await update.message.reply_text(response)
        
    async def show_tickets(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать количество билетов"""
        user = update.effective_user
        user_tickets = await self.get_user_tickets(user.id)
        total_tickets = await self.get_total_tickets()
        
        message = f"""🎫 Билеты пользователя {user.first_name}

📊 Ваши билеты: {user_tickets}/{total_tickets}

🎁 Участвуйте в розыгрыше GTM!"""
        await update.message.reply_text(message)
        
    async def show_folder(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать ссылку на папку GTM"""
        message = f"""📁 Telegram папка GTM

🔗 Ссылка на папку: {TELEGRAM_FOLDER_LINK}

📋 В папке собраны все каналы GTM:
• Режь меня всерьёз
• Чучундра
• naidenka_tattoo
• Lin++
• MurderdOll
• Потеряшка
• EMI
• bloodivamp
• Gothams top model

🎫 Подпишитесь на папку для получения билетов!"""
        await update.message.reply_text(message)
        
    async def invite_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда для приглашения друзей"""
        user = update.effective_user
        
        # Получаем или создаем реферальный код
        referral_code = await self.webapp_handler.get_or_create_referral_code(user.id)
        
        # Создаем сообщение для приглашения
        invite_text = self.webapp_handler.get_invite_message(user.first_name, referral_code)
        
        # Отправляем сообщение с клавиатурой
        await update.message.reply_text(
            invite_text,
            reply_markup=self.webapp_handler.get_invite_keyboard(referral_code),
            parse_mode='HTML'
        )
        
    async def handle_invite_button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка кнопки 'Пригласить друзей'"""
        user = update.effective_user
        
        # Получаем или создаем реферальный код
        referral_code = await self.webapp_handler.get_or_create_referral_code(user.id)
        
        # Создаем сообщение для приглашения
        invite_text = self.webapp_handler.get_invite_message(user.first_name, referral_code)
        
        # Отправляем сообщение с клавиатурой
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=invite_text,
            reply_markup=self.webapp_handler.get_invite_keyboard(referral_code),
            parse_mode='HTML'
        )
        
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Помощь"""
        help_text = f"""🤖 GTM Bot - Помощь

📋 Команды:
/start - Начать работу с ботом
/check - Проверить подписки на каналы
/tickets - Показать количество билетов
/folder - Ссылка на папку GTM
/invite - Пригласить друзей
/help - Показать эту справку

🎫 Как получить билеты:
• Подпишитесь на все 9 каналов GTM (+1 билет)
• За каждого друга по реферальной ссылке (+1 билет)

🎁 Розыгрыш GTM - главный приз 20000₽!"""
        await update.message.reply_text(help_text)
        
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда статистики (только для админа)"""
        user = update.effective_user
        
        # Проверяем, является ли пользователь админом
        if user.id != 6358105675:  # ID админа
            await update.message.reply_text("❌ У вас нет доступа к этой команде")
            return
            
        # Получаем общую статистику из БД
        total_tickets_data = await self.webapp_handler.get_total_tickets_from_db()
        total_tickets = total_tickets_data.get('total_tickets', 0)
        
        stats_text = f"""🎰 <b>СТАТИСТИКА GTM БОТА</b>

🎫 Всего билетов: {total_tickets}

📅 Обновлено: {datetime.now().strftime('%d.%m.%Y %H:%M')}"""
        
        await update.message.reply_text(stats_text, parse_mode='HTML')
        
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка callback кнопок"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "my_stats":
            user = query.from_user
            stats = await self.webapp_handler.get_user_stats(user.id)
            
            stats_text = f"""🎰 Твоя статистика

🃏 Профиль:
• User ID: {user.id}
• Подписка на все каналы: {'✅' if stats['subscription_tickets'] > 0 else '❌'}

🎫 Билеты:
• Всего билетов: {stats['total_tickets']}
• За подписку на каналы: {stats['subscription_tickets']}/1
• За приглашенных друзей: {stats['referral_tickets']}

🎰 Реферальная ссылка:
<code>https://t.me/GTM_ROBOT?start={stats['referral_code']}</code>"""
            
            await query.edit_message_text(stats_text, parse_mode='HTML')
        
    async def save_user(self, user):
        """Сохранить пользователя в БД"""
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO users (telegram_id, username, first_name, last_name)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (telegram_id) 
                DO UPDATE SET 
                    username = EXCLUDED.username,
                    first_name = EXCLUDED.first_name,
                    last_name = EXCLUDED.last_name
            """, (user.id, user.username, user.first_name, user.last_name))
            
            conn.commit()
            cursor.close()
            conn.close()
            
        except Exception as e:
            logger.error(f"Ошибка сохранения пользователя: {e}")
            
    async def add_subscription_ticket(self, user_id: int):
        """Добавить билет за подписку на все каналы"""
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            
            # Добавляем билет
            cursor.execute("""
                UPDATE users 
                SET tickets_count = tickets_count + 1
                WHERE telegram_id = %s
            """, (user_id,))
            
            # Отмечаем, что билет за подписки уже начислен
            cursor.execute("""
                UPDATE users 
                SET has_subscription_ticket = TRUE
                WHERE telegram_id = %s
            """, (user_id,))
            
            conn.commit()
            cursor.close()
            conn.close()
            
        except Exception as e:
            logger.error(f"Ошибка добавления билета за подписки: {e}")
            
    async def has_subscription_ticket(self, user_id: int) -> bool:
        """Проверить, начисляли ли уже билет за подписки"""
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT has_subscription_ticket FROM users WHERE telegram_id = %s
            """, (user_id,))
            
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            
            return result[0] if result else False
            
        except Exception as e:
            logger.error(f"Ошибка проверки билета за подписки: {e}")
            return False
            
    async def is_new_user(self, user_id: int) -> bool:
        """Проверить, новый ли это пользователь"""
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT created_at FROM users WHERE telegram_id = %s
            """, (user_id,))
            
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            
            # Если пользователь не найден, считаем его новым
            return result is None
            
        except Exception as e:
            logger.error(f"Ошибка проверки нового пользователя: {e}")
            return False
            

            
    async def get_user_tickets(self, user_id: int) -> int:
        """Получить количество билетов пользователя"""
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT tickets_count FROM users WHERE telegram_id = %s
            """, (user_id,))
            
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            
            return result[0] if result else 0
            
        except Exception as e:
            logger.error(f"Ошибка получения билетов: {e}")
            return 0
            
    async def get_total_tickets(self) -> int:
        """Получить общее количество билетов"""
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT SUM(tickets_count) FROM users
            """)
            
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            
            return result[0] if result and result[0] else 0
            
        except Exception as e:
            logger.error(f"Ошибка получения общего количества билетов: {e}")
            return 0
            
    def run(self):
        """Запуск бота"""
        logger.info("🚀 Запуск GTM Bot...")
        self.application.run_polling()

if __name__ == "__main__":
    bot = GTMBot()
    bot.run() 