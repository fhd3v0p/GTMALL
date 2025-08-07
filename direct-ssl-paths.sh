#!/bin/bash

echo "🔧 Применение прямых путей SSL для Traefik..."
echo "=============================================="

# Остановить контейнеры
echo "🛑 Останавливаем контейнеры..."
docker-compose -f docker-compose-fixed.yml down

# Применить финальную конфигурацию с прямыми путями
echo "📝 Применяем конфигурацию с прямыми путями..."
cp traefik/traefik-final.yml traefik/traefik.yml

# Проверить конфигурацию
echo "🔍 Проверяем конфигурацию..."
cat traefik/traefik.yml | grep -A 5 -B 5 "certificates"

# Проверить наличие сертификатов
echo "📁 Проверяем наличие сертификатов:"
ls -la /root/gtmall/ssl/

# Запустить заново
echo "🚀 Запускаем с прямыми путями..."
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
echo "✅ Прямые пути SSL применены!"
echo "🌐 Проверьте: https://gtm.baby" 