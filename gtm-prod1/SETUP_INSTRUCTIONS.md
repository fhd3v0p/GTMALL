# 🚀 GTM Supabase Setup Instructions

Пошаговая инструкция по настройке GTM проекта с вашими Supabase данными.

## 📋 Ваши данные Supabase

**Project URL:** `https://rxmtovqxjsvogyywyrha.supabase.co`

**Anon Key (для Flutter):**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1Mjg1NTAsImV4cCI6MjA3MDEwNDU1MH0.gDkJybktFoi486hbIVwppDfmVQlAR0fM4o4Sl1-AxhE
```

**Service Role Key (для бота):**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NDUyODU1MCwiZXhwIjoyMDcwMTA0NTUwfQ.BshdguBUaGJhB-LGpKmGAHEfmFTHw-iC6PYDmagJiR4
```

## 🗄️ Шаг 1: Настройка базы данных

### 1.1 Выполнение SQL схемы

1. Перейдите в [Supabase Dashboard](https://supabase.com/dashboard/project/rxmtovqxjsvogyywyrha)
2. Откройте **SQL Editor**
3. Создайте новый запрос
4. Скопируйте содержимое файла `gtm-prod1/bot/setup_database.sql`
5. Нажмите "Run" для выполнения

### 1.2 Проверка создания таблиц

1. Перейдите в **Database** → **Tables**
2. Убедитесь, что созданы таблицы:
   - ✅ `users`
   - ✅ `subscriptions`
   - ✅ `referrals`
   - ✅ `artists`
   - ✅ `artist_gallery`
   - ✅ `giveaways`
   - ✅ `giveaway_tickets`

## 📁 Шаг 2: Проверка Storage

### 2.1 Проверка bucket

1. Перейдите в **Storage** → **Buckets**
2. Убедитесь, что bucket `gtm-assets` существует
3. Проверьте, что он публичный

### 2.2 Проверка папок

В bucket `gtm-assets` должны быть папки:
- ✅ `avatars/` - для аватаров артистов
- ✅ `gallery/` - для галереи работ
- ✅ `artists/` - для файлов артистов
- ✅ `banners/` - для баннеров

### 2.3 Тест доступа к файлам

Проверьте доступ к файлу:
```
https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets/banners/city_selection_banner.png
```

## ⚙️ Шаг 3: Настройка конфигурации

### 3.1 Создание .env файла

```bash
cd gtm-prod1/bot
cp env_configured.txt .env
```

### 3.2 Проверка .env файла

Убедитесь, что в `gtm-prod1/bot/.env` содержится:

```bash
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=7533650686:AAEU4_nJZHGfzOv9XL4m_fDVt0q3dMDPQX8
TELEGRAM_FOLDER_LINK=https://t.me/addlist/qRX5VmLZF7E3M2U9
WEBAPP_URL=https://gtm.baby

# Supabase Configuration
SUPABASE_URL=https://rxmtovqxjsvogyywyrha.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1Mjg1NTAsImV4cCI6MjA3MDEwNDU1MH0.gDkJybktFoi486hbIVwppDfmVQlAR0fM4o4Sl1-AxhE
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NDUyODU1MCwiZXhwIjoyMDcwMTA0NTUwfQ.BshdguBUaGJhB-LGpKmGAHEfmFTHw-iC6PYDmagJiR4

# Supabase Storage Configuration
SUPABASE_STORAGE_BUCKET=gtm-assets

# Logging Configuration
LOG_LEVEL=INFO
```

## 🧪 Шаг 4: Тестирование

### 4.1 Быстрый тест

```bash
cd gtm-prod1
./quick_test.sh
```

### 4.2 Ручной тест

```bash
cd gtm-prod1/bot
source venv/bin/activate
python3 test_supabase.py
```

### 4.3 Тест простого бота

```bash
cd gtm-prod1/bot
source venv/bin/activate
python3 bot_simple.py
```

## 🚀 Шаг 5: Запуск системы

### 5.1 Полный запуск

```bash
cd gtm-prod1
./run_local_supabase.sh
```

### 5.2 Проверка работы

1. **Telegram бот**: отправьте `/start` в @GTM_ROBOT
2. **Веб-приложение**: откройте http://localhost:8080
3. **Supabase Dashboard**: проверьте данные в таблицах

## 📊 Мониторинг

### Проверка логов

```bash
# Логи бота
tail -f gtm-prod1/logs/bot.log

# Проверка процессов
ps aux | grep python
```

### Проверка Supabase

1. **Database** → **Tables** - просмотр данных
2. **Storage** → **Buckets** - управление файлами
3. **Logs** → **API** - мониторинг запросов

## 🔧 Устранение неполадок

### Проблема: Ошибка подключения к Supabase

```bash
# Проверьте .env файл
cat gtm-prod1/bot/.env

# Проверьте URL и ключи
curl "https://rxmtovqxjsvogyywyrha.supabase.co/rest/v1/"
```

### Проблема: Ошибка Telegram бота

```bash
# Проверьте токен
curl "https://api.telegram.org/bot7533650686:AAEU4_nJZHGfzOv9XL4m_fDVt0q3dMDPQX8/getMe"
```

### Проблема: Ошибка Storage

```bash
# Проверьте доступ к файлу
curl "https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets/banners/city_selection_banner.png"
```

## ✅ Чек-лист настройки

- [ ] SQL схема выполнена в Supabase
- [ ] Таблицы созданы (7 таблиц)
- [ ] Storage bucket `gtm-assets` создан
- [ ] Папки в Storage созданы (4 папки)
- [ ] .env файл настроен
- [ ] Тест подключения прошел
- [ ] Telegram бот работает
- [ ] Веб-приложение доступно

## 🎯 Следующие шаги

1. **Протестируйте бота** - отправьте команды в Telegram
2. **Проверьте веб-приложение** - откройте localhost:8080
3. **Добавьте тестовые данные** - создайте артистов
4. **Настройте мониторинг** - добавьте логирование
5. **Деплой на сервер** - когда будете готовы

## 📞 Поддержка

Если возникли проблемы:

1. Проверьте логи в терминале
2. Проверьте Supabase Dashboard
3. Убедитесь в правильности ключей
4. Проверьте подключение к интернету

**Удачи с настройкой! 🚀** 