# 🚀 GTM Supabase Integration

Полная интеграция GTM проекта с Supabase для Telegram бота и Flutter мини-приложения.

## 📋 Архитектура

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Telegram Bot  │    │  Flutter App    │    │   Supabase      │
│   (Python)      │    │   (Dart)        │    │   (Backend)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   PostgreSQL    │
                    │   Database      │
                    └─────────────────┘
```

## 🛠️ Настройка Supabase

### 1. Создание проекта Supabase

1. Перейдите на [supabase.com](https://supabase.com)
2. Создайте новый проект
3. Запишите URL и ключи API

### 2. Настройка базы данных

1. Откройте SQL Editor в Supabase Dashboard
2. Выполните SQL скрипт из `gtm-prod1/bot/supabase_schema.sql`
3. Проверьте создание таблиц в Database → Tables

### 3. Настройка Storage

1. Перейдите в Storage → Buckets
2. Создайте bucket `gtm-assets`
3. Настройте RLS политики для публичного доступа к файлам

## 🔧 Конфигурация

### Telegram Bot

1. Скопируйте `gtm-prod1/bot/env_example.txt` в `gtm-prod1/bot/.env`
2. Заполните переменные окружения:

```bash
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_FOLDER_LINK=https://t.me/addlist/qRX5VmLZF7E3M2U9
WEBAPP_URL=https://your-domain.com

# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
SUPABASE_STORAGE_BUCKET=gtm-assets
```

### Flutter App

1. Откройте `lib/supabase_config.dart`
2. Замените конфигурацию:

```dart
static const String supabaseUrl = 'https://your-project.supabase.co';
static const String supabaseAnonKey = 'your-anon-key';
```

## 🚀 Запуск

### Telegram Bot

```bash
cd gtm-prod1/bot
pip install -r requirements_supabase.txt
python bot_main_supabase.py
```

### Flutter App

```bash
flutter pub get
flutter run
```

## 📊 Структура базы данных

### Таблицы

- **users** - Пользователи Telegram бота
- **subscriptions** - Подписки на каналы
- **referrals** - Реферальные коды
- **artists** - Артисты/мастера
- **artist_gallery** - Галерея работ артистов
- **giveaways** - Розыгрыши призов
- **giveaway_tickets** - Билеты пользователей

### Основные поля

```sql
-- Пользователи
telegram_id BIGINT UNIQUE
tickets_count INTEGER
referral_code VARCHAR(20)

-- Подписки
telegram_id BIGINT
channel_id BIGINT
channel_name VARCHAR(200)

-- Артисты
name VARCHAR(200)
avatar_url VARCHAR(500)
specialties TEXT[]
rating DECIMAL(3,2)
```

## 🔄 API Endpoints

### Supabase REST API

```
GET /rest/v1/users?telegram_id=eq.123456789
POST /rest/v1/users
PATCH /rest/v1/users?telegram_id=eq.123456789

GET /rest/v1/artists
GET /rest/v1/artists?id=eq.1

GET /rest/v1/subscriptions?telegram_id=eq.123456789
POST /rest/v1/subscriptions
```

### Storage API

```
GET /storage/v1/object/public/gtm-assets/avatars/artist1.jpg
POST /storage/v1/object/gtm-assets/avatars/artist1.jpg
```

## 🔐 Безопасность

### RLS (Row Level Security)

- Пользователи видят только свои данные
- Артисты и галерея доступны публично
- Розыгрыши доступны только активные

### API Keys

- **anon key** - для Flutter приложения
- **service role key** - для Telegram бота

## 📱 Flutter интеграция

### Использование SupabaseService

```dart
import 'package:your_app/services/supabase_service.dart';

final supabaseService = SupabaseService();

// Получение артистов
final artists = await supabaseService.getArtists();

// Получение пользователя
final user = await supabaseService.getUser(telegramId);

// Получение статистики
final stats = await supabaseService.getUserStats(telegramId);
```

### Отображение изображений

```dart
String imageUrl = supabaseService.getFileUrl('avatars', 'artist1.jpg');
```

## 🤖 Telegram Bot интеграция

### Использование SupabaseClient

```python
from supabase_client import supabase_client

# Создание пользователя
await supabase_client.create_user(user_data)

# Проверка подписки
is_subscribed = await supabase_client.check_subscription(telegram_id, channel_id)

# Добавление билета
await supabase_client.add_user_ticket(telegram_id)
```

## 🔍 Мониторинг

### Логи

```bash
# Telegram Bot
tail -f gtm-prod1/logs/bot.log

# Flutter App
flutter logs
```

### Supabase Dashboard

- Database → Tables - просмотр данных
- Storage → Buckets - управление файлами
- Logs → API - мониторинг запросов

## 🚨 Устранение неполадок

### Проблемы с подключением

1. Проверьте URL и ключи Supabase
2. Убедитесь в правильности RLS политик
3. Проверьте логи в Supabase Dashboard

### Проблемы с Storage

1. Проверьте права доступа к bucket
2. Убедитесь в правильности путей к файлам
3. Проверьте размер загружаемых файлов

### Проблемы с API

1. Проверьте заголовки запросов
2. Убедитесь в правильности формата данных
3. Проверьте статус коды ответов

## 📈 Оптимизация

### Производительность

- Используйте индексы для часто запрашиваемых полей
- Кэшируйте данные в Flutter приложении
- Используйте пагинацию для больших списков

### Масштабируемость

- Supabase автоматически масштабируется
- Используйте connection pooling
- Оптимизируйте запросы к базе данных

## 🔄 Миграции

### Обновление схемы

1. Измените SQL схему в `supabase_schema.sql`
2. Выполните миграцию в Supabase Dashboard
3. Обновите код при необходимости

### Обновление данных

```sql
-- Пример миграции данных
UPDATE users SET tickets_count = 0 WHERE tickets_count IS NULL;
```

## 📚 Дополнительные ресурсы

- [Supabase Documentation](https://supabase.com/docs)
- [Flutter HTTP Package](https://pub.dev/packages/http)
- [Python Telegram Bot](https://python-telegram-bot.readthedocs.io/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## 🎯 Следующие шаги

1. Настройте CI/CD для автоматического деплоя
2. Добавьте мониторинг и алерты
3. Реализуйте кэширование данных
4. Добавьте аналитику и метрики
5. Настройте backup стратегию 