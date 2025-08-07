#!/bin/bash

echo "🔄 Принудительный перезапуск Traefik с SSL сертификатами..."
echo "=========================================================="

# Остановить все контейнеры
echo "🛑 Останавливаем контейнеры..."
docker-compose -f docker-compose-fixed.yml down

# Удалить старые тома
echo "🧹 Очищаем старые тома..."
docker volume rm gtmall_traefik_acme gtmall_traefik_logs 2>/dev/null || true

# Проверить конфигурацию
echo "🔍 Проверяем конфигурацию Traefik..."
cat traefik/traefik.yml | grep -A 5 -B 5 "certificates"

# Запустить заново
echo "🚀 Запускаем контейнеры..."
docker-compose -f docker-compose-fixed.yml up -d

# Подождать запуска
echo "⏳ Ждем запуска Traefik..."
sleep 10

# Проверить статус
echo "📊 Проверка статуса:"
docker-compose -f docker-compose-fixed.yml ps

# Проверить логи
echo "📋 Логи Traefik:"
docker-compose -f docker-compose-fixed.yml logs traefik

echo ""
echo "✅ Перезапуск завершен!"
echo "🌐 Проверьте: https://gtm.baby" 