#!/usr/bin/env python3
"""
GTM Telegram Bot с Supabase интеграцией
Проверка подписок на каналы и управление билетами через Supabase
"""

import os
import logging
import asyncio
import random
import string
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from dotenv import load_dotenv

# Импортируем Supabase клиент
from supabase_client import supabase_client
from supabase_config import validate_supabase_config

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

class GTMSupabaseBot:
    def __init__(self):
        # Проверяем конфигурацию Supabase
        if not validate_supabase_config():
            logger.error("❌ Неверная конфигурация Supabase")
            raise ValueError("Проверьте переменные окружения Supabase")
        
        self.application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        self.setup_handlers()
        logger.info("✅ GTM Supabase Bot инициализирован")
        
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
                await self.add_referral_ticket_by_code(referral_code)
        
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
        
        # Сохраняем пользователя в Supabase
        await self.save_user(user)
        
    async def check_subscription(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Проверка подписки на каналы"""
        user = update.effective_user
        
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
        
        # Проверяем, подписан ли на все 9 каналов
        is_subscribed_to_all = len(subscribed_channels) == 9
        
        # Вызываем функцию проверки подписки и начисления билета
        result = await supabase_client.check_subscription_and_award_ticket(user.id, is_subscribed_to_all)
        
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
        
        # Добавляем информацию о билетах
        if result.get('ticket_awarded', False):
            response += "🎫 Билет начислен за подписку на папку!\n"
        else:
            if not is_subscribed_to_all:
                response += f"⚠️ Для получения билета нужно подписаться на все {len(SUBSCRIPTION_CHANNELS)} каналов\n\n"
                response += f"📁 Подпишитесь на папку GTM: {TELEGRAM_FOLDER_LINK}\n"
                response += "🔒 Не отписывайтесь до конца розыгрыша!"
            else:
                response += "✅ Билет за подписки уже начислен\n"
        
        # Показываем текущие билеты пользователя
        user_tickets = result.get('total_tickets', 0)
        total_tickets = await supabase_client.get_total_tickets()
        response += f"\n🎫 Ваши билеты: {user_tickets}/{total_tickets}"
        
        await update.message.reply_text(response)
        
    async def show_tickets(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать количество билетов"""
        user = update.effective_user
        user_stats = await supabase_client.get_user_stats(user.id)
        
        subscription_tickets = user_stats.get('subscription_tickets', 0)
        referral_tickets = user_stats.get('referral_tickets', 0)
        total_tickets = user_stats.get('total_tickets', 0)
        
        message = f"""🎫 Билеты пользователя {user.first_name}

📊 Детализация билетов:
• За подписку на папку: {subscription_tickets}/1
• За приглашенных друзей: {referral_tickets}/10
• Всего билетов: {total_tickets}

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
        referral_code = await self.get_or_create_referral_code(user.id)
        
        # Создаем сообщение для приглашения
        invite_text = self.get_invite_message(user.first_name, referral_code)
        
        # Отправляем сообщение с клавиатурой
        await update.message.reply_text(
            invite_text,
            reply_markup=self.get_invite_keyboard(referral_code),
            parse_mode='HTML'
        )
        
    async def handle_invite_button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка кнопки 'Пригласить друзей'"""
        user = update.effective_user
        
        # Получаем или создаем реферальный код
        referral_code = await self.get_or_create_referral_code(user.id)
        
        # Создаем сообщение для приглашения
        invite_text = self.get_invite_message(user.first_name, referral_code)
        
        # Отправляем сообщение с клавиатурой
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=invite_text,
            reply_markup=self.get_invite_keyboard(referral_code),
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
• За каждого друга по реферальной ссылке (+1 билет, максимум 10)

🎁 Розыгрыш GTM - главный приз 20000₽!"""
        await update.message.reply_text(help_text)
        
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда статистики (только для админа)"""
        user = update.effective_user
        
        # Проверяем, является ли пользователь админом
        if user.id != 6358105675:  # ID админа
            await update.message.reply_text("❌ У вас нет доступа к этой команде")
            return
            
        # Получаем общую статистику из Supabase
        stats = await supabase_client.get_tickets_stats()
        
        total_subscription_tickets = stats.get('total_subscription_tickets', 0)
        total_referral_tickets = stats.get('total_referral_tickets', 0)
        total_user_tickets = stats.get('total_user_tickets', 0)
        
        stats_text = f"""🎰 <b>СТАТИСТИКА GTM БОТА (Supabase)</b>

🎫 Общая статистика билетов:
• За подписки на папку: {total_subscription_tickets}
• За рефералов: {total_referral_tickets}
• Всего билетов: {total_user_tickets}

📅 Обновлено: {datetime.now().strftime('%d.%m.%Y %H:%M')}"""
        
        await update.message.reply_text(stats_text, parse_mode='HTML')
        
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка callback кнопок"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "my_stats":
            user = query.from_user
            stats = await supabase_client.get_user_stats(user.id)
            
            subscription_tickets = stats.get('subscription_tickets', 0)
            referral_tickets = stats.get('referral_tickets', 0)
            total_tickets = stats.get('total_tickets', 0)
            
            stats_text = f"""🎰 Твоя статистика

🃏 Профиль:
• User ID: {user.id}
• Подписка на все каналы: {'✅' if subscription_tickets > 0 else '❌'}

🎫 Билеты:
• За подписку на папку: {subscription_tickets}/1
• За приглашенных друзей: {referral_tickets}/10
• Всего билетов: {total_tickets}

🎰 Реферальная ссылка:
<code>https://t.me/GTM_ROBOT?start={stats.get('referral_code', '')}</code>"""
            
            await query.edit_message_text(stats_text, parse_mode='HTML')
    
    # === Supabase методы ===
    async def save_user(self, user):
        """Сохранить пользователя в Supabase"""
        try:
            user_data = {
                'telegram_id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'subscription_tickets': 0,
                'referral_tickets': 0,
                'total_tickets': 0
            }
            
            # Проверяем, существует ли пользователь
            existing_user = await supabase_client.get_user(user.id)
            if existing_user:
                # Обновляем существующего пользователя
                await supabase_client.update_user(user.id, user_data)
            else:
                # Создаем нового пользователя
                await supabase_client.create_user(user_data)
                
        except Exception as e:
            logger.error(f"Ошибка сохранения пользователя в Supabase: {e}")
    
    async def is_new_user(self, user_id: int) -> bool:
        """Проверить, новый ли это пользователь"""
        try:
            user = await supabase_client.get_user(user_id)
            return user is None
        except Exception as e:
            logger.error(f"Ошибка проверки нового пользователя: {e}")
            return False
    
    async def add_referral_ticket_by_code(self, referral_code: str):
        """Добавить билет за реферала по коду"""
        try:
            await supabase_client.add_referral_ticket(referral_code)
        except Exception as e:
            logger.error(f"Ошибка добавления билета за реферала: {e}")
    
    async def get_or_create_referral_code(self, telegram_id: int) -> str:
        """Получить или создать реферальный код"""
        try:
            user = await supabase_client.get_user(telegram_id)
            if user and user.get('referral_code'):
                return user['referral_code']
            
            # Создаем новый реферальный код
            referral_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            
            # Обновляем пользователя с новым кодом
            await supabase_client.update_user(telegram_id, {'referral_code': referral_code})
            
            return referral_code
        except Exception as e:
            logger.error(f"Ошибка создания реферального кода: {e}")
            return "ERROR"
    
    def get_invite_message(self, user_name: str, referral_code: str) -> str:
        """Создать сообщение для приглашения"""
        return f"""🎰 <b>Приглашение в GTM</b>

👋 Привет! {user_name} приглашает тебя в Gotham's Top Model!

🎁 Что ты получишь:
• 🃏 Каталог топовых артистов
• 🤖 AI-поиск услуг
• 🎰 Розыгрыш призов на >130,000₽
• 🎱 Скидка 8% на услуги
• 💞 Реферальная система

🎫 За регистрацию по ссылке {user_name} получит +1 билет!

🔗 <a href="https://t.me/GTM_ROBOT?start={referral_code}">Присоединиться к GTM</a>"""
    
    def get_invite_keyboard(self, referral_code: str):
        """Создать клавиатуру для приглашения"""
        keyboard = [
            [
                InlineKeyboardButton(
                    text="🎰 Присоединиться к GTM",
                    url=f"https://t.me/GTM_ROBOT?start={referral_code}"
                )
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def run(self):
        """Запуск бота"""
        logger.info("🚀 Запуск GTM Supabase Bot...")
        self.application.run_polling()

if __name__ == "__main__":
    bot = GTMSupabaseBot()
    bot.run() 