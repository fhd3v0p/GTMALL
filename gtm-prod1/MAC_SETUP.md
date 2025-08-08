# 🍎 GTM Supabase Setup для Mac (без Docker)

Пошаговая инструкция по настройке GTM проекта с Supabase на Mac без использования Docker.

## 📋 Требования

- macOS (любая версия)
- Python 3.8+ (уже установлен на большинстве Mac)
- Flutter (для веб-приложения)

## 🚀 Быстрый старт

### 1. Подготовка проекта

```bash
# Перейдите в директорию проекта
cd gtm-prod1

# Создайте .env файл
cp bot/env_example.txt bot/.env
```

### 2. Настройка Supabase

1. Откройте `bot/.env` и заполните переменные:
```bash
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=7533650686:AAEU4_nJZHGfzOv9XL4m_fDVt0q3dMDPQX8
TELEGRAM_FOLDER_LINK=https://t.me/addlist/qRX5VmLZF7E3M2U9
WEBAPP_URL=https://gtm.baby

# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here
SUPABASE_STORAGE_BUCKET=gtm-assets
```

### 3. Быстрый тест

```bash
# Запустите быстрый тест
./quick_test.sh
```

### 4. Запуск системы

```bash
# Полный запуск (с Flutter)
./run_local_supabase.sh

# Или только бот
cd bot
source venv/bin/activate
python3 bot_simple.py
```

## 🔧 Подробная настройка

### Шаг 1: Проверка Python

```bash
# Проверьте версию Python
python3 --version

# Если не установлен
brew install python3
```

### Шаг 2: Настройка Supabase

1. **Создайте проект на Supabase:**
   - Перейдите на [supabase.com](https://supabase.com)
   - Создайте новый проект
   - Запишите URL и ключи API

2. **Настройте базу данных:**
   - Откройте SQL Editor в Supabase Dashboard
   - Выполните SQL скрипт из `bot/supabase_schema.sql`

3. **Настройте Storage:**
   - Перейдите в Storage → Buckets
   - Создайте bucket `gtm-assets`
   - Загрузите папку assets

### Шаг 3: Конфигурация

1. **Создайте .env файл:**
```bash
cd gtm-prod1/bot
cp env_example.txt .env
```

2. **Заполните переменные в .env:**
```bash
# Откройте .env в редакторе
nano .env

# Заполните ваши данные Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

### Шаг 4: Установка зависимостей

```bash
# Создайте виртуальное окружение
cd gtm-prod1/bot
python3 -m venv venv
source venv/bin/activate

# Установите зависимости
pip install requests python-dotenv

# Для полного бота (опционально)
pip install python-telegram-bot
```

### Шаг 5: Тестирование

```bash
# Быстрый тест
cd gtm-prod1
./quick_test.sh

# Или вручную
cd bot
source venv/bin/activate
python3 test_supabase.py
```

## 🎯 Варианты запуска

### Вариант 1: Только тест Supabase
```bash
cd gtm-prod1/bot
source venv/bin/activate
python3 test_supabase.py
```

### Вариант 2: Простой бот
```bash
cd gtm-prod1/bot
source venv/bin/activate
python3 bot_simple.py
```

### Вариант 3: Полная система
```bash
cd gtm-prod1
./run_local_supabase.sh
```

## 📱 Flutter приложение

### Сборка для веб
```bash
# В корневой директории проекта
flutter build web --release
cp -r build/web/* gtm-prod1/web/
```

### Запуск веб-сервера
```bash
cd gtm-prod1/web
python3 -m http.server 8080
# Откройте http://localhost:8080
```

## 🔍 Мониторинг

### Логи бота
```bash
# Логи будут отображаться в терминале
# Для сохранения в файл:
python3 bot_simple.py > bot.log 2>&1 &
```

### Проверка статуса
```bash
# Проверка процессов
ps aux | grep python

# Проверка портов
lsof -i :8080
```

## 🚨 Устранение неполадок

### Проблема: Python не найден
```bash
# Установите Python
brew install python3

# Проверьте путь
which python3
```

### Проблема: Модули не установлены
```bash
# Активируйте виртуальное окружение
source venv/bin/activate

# Установите зависимости
pip install -r requirements_supabase.txt
```

### Проблема: Supabase подключение
```bash
# Проверьте .env файл
cat bot/.env

# Проверьте URL и ключи
python3 test_supabase.py
```

### Проблема: Telegram бот
```bash
# Проверьте токен
curl "https://api.telegram.org/botYOUR_TOKEN/getMe"

# Установите библиотеку
pip install python-telegram-bot
```

## 📊 Структура файлов

```
gtm-prod1/
├── bot/
│   ├── .env                    # Конфигурация
│   ├── venv/                   # Виртуальное окружение
│   ├── bot_simple.py           # Простой бот
│   ├── test_supabase.py        # Тесты
│   └── requirements_supabase.txt
├── web/                        # Flutter веб-приложение
├── quick_test.sh               # Быстрый тест
├── run_local_supabase.sh       # Полный запуск
└── MAC_SETUP.md               # Эта инструкция
```

## 🎉 Готово!

После настройки у вас будет:

- ✅ Telegram бот с Supabase интеграцией
- ✅ Flutter веб-приложение
- ✅ База данных PostgreSQL в Supabase
- ✅ Storage для файлов
- ✅ Система билетов и рефералов

### Следующие шаги:

1. **Протестируйте бота** - отправьте `/start` в Telegram
2. **Проверьте веб-приложение** - откройте http://localhost:8080
3. **Настройте мониторинг** - добавьте логирование
4. **Деплой на сервер** - когда будете готовы к продакшену

## 💡 Полезные команды

```bash
# Остановка процессов
pkill -f "python3 bot_simple.py"
pkill -f "http.server"

# Очистка виртуального окружения
rm -rf bot/venv

# Пересоздание окружения
cd bot && python3 -m venv venv && source venv/bin/activate && pip install -r requirements_supabase.txt
``` 