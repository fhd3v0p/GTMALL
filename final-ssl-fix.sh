#!/bin/bash

echo "🔧 Финальное исправление SSL сертификатов..."
echo "============================================="

# Остановить контейнеры
echo "🛑 Останавливаем контейнеры..."
docker-compose -f docker-compose-fixed.yml down

# Очистить тома
echo "🧹 Очищаем тома..."
docker volume rm gtmall_traefik_acme gtmall_traefik_logs 2>/dev/null || true

# Применить финальную конфигурацию
echo "📝 Применяем финальную конфигурацию..."
cp traefik/traefik-final.yml traefik/traefik.yml

# Проверить конфигурацию
echo "🔍 Проверяем конфигурацию..."
cat traefik/traefik.yml | grep -A 5 -B 5 "certificates"

# Запустить заново
echo "🚀 Запускаем с финальной конфигурацией..."
docker-compose -f docker-compose-fixed.yml up -d

# Ждать запуска
echo "⏳ Ждем запуска..."
sleep 15

# Проверить статус
echo "📊 Проверка статуса:"
docker-compose -f docker-compose-fixed.yml ps

# Проверить логи
echo "📋 Логи Traefik:"
docker logs gtm_traefik --tail=10

# Тест SSL
echo "🧪 Тест SSL сертификата:"
echo "Q" | openssl s_client -connect gtm.baby:443 -servername gtm.baby 2>/dev/null | grep -E "(subject=|issuer=|DNS:)"

echo ""
echo "✅ Финальное исправление завершено!"
echo "🌐 Проверьте: https://gtm.baby" 