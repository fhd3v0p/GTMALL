#!/bin/bash

echo "🚀 Запуск GTM с Nginx и SSL"
echo "============================"

# Остановить старые контейнеры
echo "🛑 Останавливаем старые контейнеры..."
docker-compose down 2>/dev/null || true
docker-compose -f docker-compose-simple.yml down 2>/dev/null || true

# Очистить Docker
echo "🧹 Очищаем Docker..."
docker system prune -f

# Проверить SSL сертификаты
echo "🔒 Проверяем SSL сертификаты..."
if [ -f "gtm.baby-ssl-bundle/domain.cert.pem" ] && [ -f "gtm.baby-ssl-bundle/private.key.pem" ]; then
    echo "✅ SSL сертификаты найдены"
else
    echo "❌ SSL сертификаты не найдены!"
    exit 1
fi

# Проверить web директорию
echo "📁 Проверяем web директорию..."
if [ -d "/root/gtmall/web" ]; then
    echo "✅ Web директория найдена: /root/gtmall/web"
else
    echo "❌ Web директория не найдена: /root/gtmall/web"
    exit 1
fi

# Запустить с Nginx
echo "🚀 Запускаем с Nginx..."
docker-compose -f docker-compose-simple.yml up -d --build

# Подождать и проверить статус
echo "⏳ Ждем запуска контейнеров..."
sleep 15

echo "📊 Статус контейнеров:"
docker-compose -f docker-compose-simple.yml ps

echo ""
echo "🔍 Логи Nginx:"
docker-compose -f docker-compose-simple.yml logs nginx

echo ""
echo "✅ Готово! Сайт должен быть доступен на:"
echo "🌐 https://gtm.baby"
echo "🔍 Проверьте: curl -I https://gtm.baby" 