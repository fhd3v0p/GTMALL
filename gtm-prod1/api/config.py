# GTM API config
# Скопируйте сюда ваш config.py
#!/usr/bin/env python3
"""
GTM Project Configuration
Единый конфигурационный файл для всего проекта
"""

import os
import logging
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Настройки логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Настройки базы данных PostgreSQL (локальная)
DB_HOST = os.getenv('DB_HOST', 'postgres')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'gtm_db')
DB_USER = os.getenv('DB_USER', 'gtm_user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'gtm_secure_password_2024')
DB_SSL_MODE = os.getenv('DB_SSL_MODE', 'disable')
DB_CHANNEL_BINDING = os.getenv('DB_CHANNEL_BINDING', 'disable')

# Настройки Redis
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')
REDIS_DB = os.getenv('REDIS_DB', '0')

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '7533650686:AAEU4_nJZHGfzOv9XL4m_fDVt0q3dMDPQX8')

# Telegram папка GTM
TELEGRAM_FOLDER_LINK = os.getenv('TELEGRAM_FOLDER_LINK', 'https://t.me/addlist/qRX5VmLZF7E3M2U9')

# Настройки API
API_HOST = os.getenv('API_HOST', '0.0.0.0')
API_PORT = int(os.getenv('API_PORT', '3001'))
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Настройки CORS
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8080",
    "https://gtm.baby",
    "https://api.gtm.baby",
    "https://admin.gtm.baby"
]

# Каналы подписки для гивевея (обновленные с исправленным channel_id)
GIVEAWAY_SUBSCRIPTION_CHANNELS = [
    # Реальные каналы GTM
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

def get_database_url():
    """Получить URL для подключения к базе данных"""
    if DB_PASSWORD:
        return f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode={DB_SSL_MODE}&channel_binding={DB_CHANNEL_BINDING}"
    else:
        return f"postgresql://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode={DB_SSL_MODE}&channel_binding={DB_CHANNEL_BINDING}"

def get_redis_url():
    """Получить URL для подключения к Redis"""
    return f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

def get_moscow_time():
    """Получить текущее время по Москве"""
    moscow_tz = timezone(timedelta(hours=3))
    return datetime.now(moscow_tz)

def validate_config():
    """Проверка конфигурации"""
    required_vars = ['TELEGRAM_BOT_TOKEN']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.warning(f"Отсутствуют переменные окружения: {missing_vars}")
        return False
    return True

# URL для подключения к базе данных
DATABASE_URL = get_database_url()

# URL для подключения к Redis
REDIS_URL = get_redis_url()

# Конфигурация для Flask
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'gtm-secret-key-2025')
    DATABASE_URL = DATABASE_URL
    REDIS_URL = REDIS_URL
    TELEGRAM_BOT_TOKEN = TELEGRAM_BOT_TOKEN
    TELEGRAM_FOLDER_LINK = TELEGRAM_FOLDER_LINK
    DEBUG = DEBUG
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    UPLOAD_DIR = os.getenv('UPLOAD_DIR', '/app/uploads')
    API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:3001')
    PROJECT_NAME = 'GTM API'
    VERSION = '1.0.0'
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'production')
    CORS_ORIGINS = CORS_ORIGINS
    GIVEAWAY_SUBSCRIPTION_CHANNELS = GIVEAWAY_SUBSCRIPTION_CHANNELS
    
    # Добавляем недостающие переменные
    DB_HOST = DB_HOST
    DB_PORT = DB_PORT
    DB_NAME = DB_NAME
    DB_USER = DB_USER
    DB_PASSWORD = DB_PASSWORD
    DB_SSL_MODE = DB_SSL_MODE
    DB_CHANNEL_BINDING = DB_CHANNEL_BINDING
    REDIS_HOST = REDIS_HOST
    REDIS_PORT = REDIS_PORT
    REDIS_DB = REDIS_DB
    API_HOST = API_HOST
    API_PORT = API_PORT
    
    def validate(self):
        """Проверка конфигурации"""
        return {'valid': validate_config(), 'warnings': []}

# Экспортируем конфигурацию
config = Config()

# Экспортируем все необходимые переменные
__all__ = [
    'DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_SSL_MODE', 'DB_CHANNEL_BINDING',
    'REDIS_HOST', 'REDIS_PORT', 'REDIS_DB',
    'TELEGRAM_BOT_TOKEN', 'TELEGRAM_FOLDER_LINK',
    'API_HOST', 'API_PORT', 'DEBUG',
    'CORS_ORIGINS', 'GIVEAWAY_SUBSCRIPTION_CHANNELS',
    'DATABASE_URL', 'REDIS_URL', 'config',
    'get_database_url', 'get_redis_url', 'get_moscow_time', 'validate_config'
] 