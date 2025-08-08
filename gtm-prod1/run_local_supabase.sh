#!/bin/bash

# GTM Local Supabase Runner (без Docker)
# Скрипт для локального запуска GTM проекта с Supabase на Mac

set -e

echo "🚀 GTM Local Supabase Runner"
echo "============================"

# Проверка наличия .env файла
if [ ! -f "bot/.env" ]; then
    echo "❌ Файл bot/.env не найден!"
    echo "📝 Создайте файл bot/.env на основе bot/env_example.txt"
    echo "🔧 Заполните переменные окружения Supabase"
    exit 1
fi

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не установлен!"
    echo "📦 Установите Python3: brew install python3"
    exit 1
fi

# Проверка Flutter
if ! command -v flutter &> /dev/null; then
    echo "❌ Flutter не установлен!"
    echo "📦 Установите Flutter: https://flutter.dev/docs/get-started/install"
    exit 1
fi

# Проверка переменных окружения
echo "🔍 Проверка конфигурации..."

# Загружаем переменные окружения
source bot/.env

# Проверяем обязательные переменные
required_vars=(
    "TELEGRAM_BOT_TOKEN"
    "SUPABASE_URL"
    "SUPABASE_ANON_KEY"
    "SUPABASE_SERVICE_ROLE_KEY"
)

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "❌ Переменная $var не установлена!"
        exit 1
    fi
done

echo "✅ Конфигурация проверена"

# Создание виртуального окружения Python
echo "🐍 Настройка Python окружения..."
cd bot
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Активация виртуального окружения
source venv/bin/activate

# Установка зависимостей
echo "📦 Установка Python зависимостей..."
pip install -r requirements_supabase.txt

echo "✅ Python окружение настроено"

# Сборка Flutter приложения
echo "📱 Сборка Flutter приложения..."
cd ..
flutter build web --release
cp -r build/web/* gtm-prod1/web/
echo "✅ Flutter приложение собрано"

# Возвращаемся в директорию проекта
cd gtm-prod1

# Запуск Telegram бота в фоне
echo "🤖 Запуск Telegram бота..."
cd bot
source venv/bin/activate
python3 bot_main_supabase.py &
BOT_PID=$!
cd ..

# Запуск простого HTTP сервера для Flutter app
echo "🌐 Запуск веб-сервера..."
cd web
python3 -m http.server 8080 &
WEB_PID=$!
cd ..

echo "✅ GTM Local Supabase запущен!"
echo ""
echo "🌐 Доступные URL:"
echo "   - Веб-приложение: http://localhost:8080"
echo "   - Telegram Bot: @GTM_ROBOT"
echo ""
echo "📊 Мониторинг:"
echo "   - Бот PID: $BOT_PID"
echo "   - Web PID: $WEB_PID"
echo ""
echo "🛑 Для остановки:"
echo "   kill $BOT_PID $WEB_PID"
echo ""
echo "📝 Логи бота будут отображаться в терминале"
echo "💡 Для остановки нажмите Ctrl+C"

# Ожидание сигнала для остановки
trap "echo '🛑 Остановка сервисов...'; kill $BOT_PID $WEB_PID 2>/dev/null; exit 0" INT TERM

# Ожидание завершения
wait 