#!/bin/bash

echo "🚀 Запуск с Nginx вместо Traefik..."
echo "===================================="

# Остановить старые контейнеры
echo "🛑 Останавливаем старые контейнеры..."
docker-compose -f docker-compose-fixed.yml down 2>/dev/null || true

# Очистить Docker
echo "🧹 Очищаем Docker..."
docker system prune -f

# Проверить SSL сертификаты
echo "🔒 Проверяем SSL сертификаты..."
if [ -f "/root/gtmall/ssl/domain.cert.pem" ] && [ -f "/root/gtmall/ssl/private.key.pem" ]; then
    echo "✅ SSL сертификаты найдены"
else
    echo "❌ SSL сертификаты не найдены!"
    exit 1
fi

# Проверить web директорию
echo "📁 Проверяем web директорию..."
if [ -d "/root/gtmall/web" ]; then
    echo "✅ Web директория найдена"
else
    echo "❌ Web директория не найдена!"
    exit 1
fi

# Проверить nginx конфигурацию
echo "⚙️ Проверяем nginx конфигурацию..."
nginx -t -c /root/gtmall/nginx.conf 2>/dev/null || echo "⚠️ Nginx конфигурация будет проверена в контейнере"

# Запустить с Nginx
echo "🚀 Запускаем с Nginx..."
docker-compose -f docker-compose-fixed.yml up -d

# Ждать запуска
echo "⏳ Ждем запуска..."
sleep 10

# Проверить статус
echo "📊 Проверка статуса:"
docker-compose -f docker-compose-fixed.yml ps

# Проверить логи
echo "📋 Логи Nginx:"
docker logs gtm_nginx --tail=10

# Тест SSL
echo "🧪 Тест SSL сертификата:"
echo "Q" | openssl s_client -connect gtm.baby:443 -servername gtm.baby 2>/dev/null | grep -E "(subject=|issuer=|DNS:)"

echo ""
echo "✅ Nginx запущен!"
echo "🌐 Доступные URL:"
echo "   - Основной сайт: https://gtm.baby"
echo "   - API: https://api.gtm.baby" 