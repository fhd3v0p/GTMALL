# 📊 Анализ развертывания GTM

## 🔍 Анализ файлов и зависимостей

### Telegram Bot (`bot_main.py`)

**Зависимости:**
- `python-telegram-bot==20.6` - Telegram Bot API
- `psycopg2-binary==2.9.7` - PostgreSQL драйвер
- `redis==4.6.0` - Redis клиент
- `python-dotenv==1.0.0` - Загрузка переменных окружения
- `requests==2.31.0` - HTTP клиент
- `aiohttp==3.9.1` - Асинхронный HTTP клиент

**Переменные окружения:**
- `TELEGRAM_BOT_TOKEN` - Токен бота
- `DATABASE_URL` - URL базы данных (опционально)
- `REDIS_URL` - URL Redis (опционально)
- `SUPABASE_URL` - URL Supabase
- `SUPABASE_ANON_KEY` - Анонимный ключ Supabase
- `SUPABASE_SERVICE_ROLE_KEY` - Сервисный ключ Supabase
- `TELEGRAM_FOLDER_LINK` - Ссылка на папку Telegram
- `WEBAPP_URL` - URL веб-приложения

**Функциональность:**
- Проверка подписок на каналы
- Управление билетами
- Интеграция с Supabase
- WebApp интеграция

### API Server (`api_server.py`)

**Зависимости:**
- `flask==2.3.3` - Веб-фреймворк
- `flask-cors==4.0.0` - CORS поддержка
- `python-telegram-bot==20.7` - Telegram Bot API
- `python-dotenv==1.0.0` - Загрузка переменных окружения
- `requests==2.31.0` - HTTP клиент
- `psycopg2-binary==2.9.9` - PostgreSQL драйвер
- `redis==5.0.1` - Redis клиент
- `gunicorn==21.2.0` - WSGI сервер

**Переменные окружения:**
- `API_PORT` - Порт API (5000)
- `API_HOST` - Хост API (0.0.0.0)
- `FLASK_ENV` - Окружение Flask
- `SUPABASE_URL` - URL Supabase
- `SUPABASE_ANON_KEY` - Анонимный ключ Supabase
- `SUPABASE_SERVICE_ROLE_KEY` - Сервисный ключ Supabase
- `TELEGRAM_BOT_TOKEN` - Токен бота
- `DATABASE_URL` - URL базы данных (опционально)
- `REDIS_URL` - URL Redis (опционально)

**Эндпоинты:**
- `GET /api/health` - Проверка здоровья
- `POST /api/check_subscription` - Проверка подписки
- `GET /api/user_tickets/<telegram_id>` - Получение билетов пользователя
- `GET /api/total_tickets_stats` - Статистика билетов
- `POST /api/telegram_bot/check` - Вызов команды бота

### Supabase Client (`supabase_client.py`)

**Функциональность:**
- CRUD операции с пользователями
- Управление подписками
- Управление билетами
- Работа с артистами
- Загрузка файлов в Storage
- Статистика

**Требования:**
- Supabase проект настроен
- Таблицы: `users`, `subscriptions`, `artists`, `artist_gallery`
- Storage bucket: `gtm-assets-public`

## 🐳 Docker конфигурация

### Сеть
- `traefik` - внешняя сеть для Traefik

### Volumes
- `traefik_acme` - SSL сертификаты
- `traefik_logs` - Логи Traefik
- `redis_data` - Данные Redis
- `postgres_data` - Данные PostgreSQL (опционально)

### Порты
- `80` - HTTP (редирект на HTTPS)
- `443` - HTTPS
- `8080` - Traefik Dashboard

## 🔒 Безопасность

### Traefik Middleware
- `secure-headers` - Безопасные заголовки
- `cors` - CORS настройки
- `rate-limit` - Ограничение запросов
- `auth` - Базовая аутентификация для dashboard

### SSL
- Автоматическое получение сертификатов через Let's Encrypt
- Поддержка пользовательских сертификатов в `traefik/ssl/`

## 📊 Мониторинг

### Health Checks
- API: `https://api.gtm.baby/api/health`
- Traefik Dashboard: `https://traefik.gtm.baby`

### Логирование
- Traefik: `/var/log/traefik/`
- Приложения: Docker logs

## 🚀 Развертывание

### Требования
1. Docker и Docker Compose
2. Домен `gtm.baby` с DNS записями:
   - `gtm.baby` → сервер
   - `api.gtm.baby` → сервер
   - `traefik.gtm.baby` → сервер
3. SSL сертификаты (опционально)

### Шаги развертывания
1. Клонировать репозиторий
2. Запустить `./setup.sh`
3. Отредактировать `.env`
4. Запустить `docker-compose up -d`
5. Проверить `docker-compose ps`

## 🔧 Масштабирование

### Горизонтальное масштабирование
- API: `docker-compose up --scale api=3`
- Redis кластер (опционально)
- PostgreSQL репликация (опционально)

### Вертикальное масштабирование
- Увеличение ресурсов контейнеров
- Оптимизация Gunicorn workers
- Настройка кэширования

## 📝 Примечания

1. **Supabase**: Основная база данных, PostgreSQL опционально
2. **Redis**: Кэширование и сессии
3. **Traefik**: Обратный прокси и SSL
4. **Масштабируемость**: Готова к горизонтальному масштабированию
5. **Безопасность**: Настроены заголовки безопасности и rate limiting 