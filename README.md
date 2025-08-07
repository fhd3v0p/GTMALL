# 🏗️ GTM Deployment Structure

Структура для развертывания GTM с Docker и Traefik.

## 📁 Структура проекта

```
@GTMALL/
├── bot/                    # Telegram Bot
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── bot_main.py
│   ├── supabase_client.py
│   ├── webapp_handler.py
│   └── .env.example
├── api/                    # API Server
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── api_server.py
│   ├── supabase_client.py
│   └── .env.example
├── web/                    # Flutter Web App (будет добавлено позже)
│   └── README.md
├── traefik/                # Traefik Configuration
│   ├── traefik.yml
│   ├── ssl/
│   │   └── gtm.baby-ssl-bundle/
│   └── config/
│       └── dynamic.yml
├── docker-compose.yml      # Основной compose файл
├── .env.example           # Общие переменные окружения
└── README.md
```

## 🚀 Быстрый старт

1. Скопируйте `.env.example` в `.env` и заполните переменные
2. Запустите: `docker-compose up -d`
3. Проверьте: `docker-compose ps`

## 🔧 Конфигурация

### Переменные окружения

Создайте файл `.env` в корне проекта:

```bash
# Общие настройки
ENVIRONMENT=production
DOMAIN=gtm.baby

# Supabase
SUPABASE_URL=https://rxmtovqxjsvogyywyrha.supabase.co
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_FOLDER_LINK=https://t.me/addlist/qRX5VmLZF7E3M2U9
WEBAPP_URL=https://gtm.baby

# API Server
API_PORT=5000
API_HOST=0.0.0.0

# Redis (опционально)
REDIS_URL=redis://redis:6379/0

# Database (если используется локальная БД)
DATABASE_URL=postgresql://user:password@postgres:5432/dbname
```

## 🌐 Доступные сервисы

- **API**: https://api.gtm.baby
- **Web App**: https://gtm.baby (будет добавлено)
- **Bot**: @your_bot_username

## 📊 Мониторинг

- Traefik Dashboard: https://traefik.gtm.baby
- API Health: https://api.gtm.baby/api/health

## 🔒 SSL

SSL сертификаты должны быть размещены в `traefik/ssl/gtm.baby-ssl-bundle/` 