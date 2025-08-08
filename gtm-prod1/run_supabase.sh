#!/bin/bash

# GTM Supabase Runner
# Скрипт для запуска GTM проекта с Supabase

set -e

echo "🚀 GTM Supabase Runner"
echo "======================"

# Проверка наличия .env файла
if [ ! -f "bot/.env" ]; then
    echo "❌ Файл bot/.env не найден!"
    echo "📝 Создайте файл bot/.env на основе bot/env_example.txt"
    echo "🔧 Заполните переменные окружения Supabase"
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

# Сборка Flutter приложения
echo "📱 Сборка Flutter приложения..."
cd ..
flutter build web --release
cp -r build/web/* gtm-prod1/web/
echo "✅ Flutter приложение собрано"

# Возвращаемся в директорию проекта
cd gtm-prod1

# Сборка и запуск Docker контейнеров
echo "🐳 Запуск Docker контейнеров..."
docker-compose -f docker-compose.supabase.yml down
docker-compose -f docker-compose.supabase.yml build
docker-compose -f docker-compose.supabase.yml up -d

echo "✅ GTM Supabase запущен!"
echo ""
echo "🌐 Доступные URL:"
echo "   - Веб-приложение: http://localhost"
echo "   - Telegram Bot: @GTM_ROBOT"
echo ""
echo "📊 Мониторинг:"
echo "   - Логи бота: docker-compose -f docker-compose.supabase.yml logs -f bot"
echo "   - Логи nginx: docker-compose -f docker-compose.supabase.yml logs -f nginx"
echo ""
echo "🛑 Для остановки: docker-compose -f docker-compose.supabase.yml down" 