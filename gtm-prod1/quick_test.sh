#!/bin/bash

# GTM Quick Test Script
# Быстрый тест для проверки Supabase интеграции на Mac

set -e

echo "🚀 GTM Quick Test"
echo "================="

# Проверка .env файла
if [ ! -f "bot/.env" ]; then
    echo "❌ Файл bot/.env не найден!"
    echo "📝 Создайте файл bot/.env на основе bot/env_example.txt"
    echo "🔧 Заполните переменные окружения Supabase"
    exit 1
fi

# Переходим в директорию бота
cd bot

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не установлен!"
    echo "📦 Установите Python3: brew install python3"
    exit 1
fi

# Создание виртуального окружения
echo "🐍 Настройка Python окружения..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Активация виртуального окружения
source venv/bin/activate

# Установка минимальных зависимостей
echo "📦 Установка зависимостей..."
pip install requests python-dotenv

# Проверка telegram библиотеки
if ! python3 -c "import telegram" 2>/dev/null; then
    echo "⚠️ python-telegram-bot не установлен"
    echo "📦 Установите: pip install python-telegram-bot"
    echo "💡 Будет запущен тест только Supabase"
fi

# Запуск тестов
echo "🔍 Запуск тестов..."
python3 test_supabase.py

echo ""
echo "🎯 Тестирование завершено!"
echo ""
echo "💡 Для запуска простого бота:"
echo "   cd bot && source venv/bin/activate && python3 bot_simple.py"
echo ""
echo "💡 Для запуска полной системы:"
echo "   ./run_local_supabase.sh" 