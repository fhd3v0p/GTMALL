#!/bin/bash

echo "🔍 Диагностика 404 ошибки и SSL проблем..."
echo "==========================================="

# 1. Проверить статус контейнеров
echo "📊 Статус контейнеров:"
docker-compose -f docker-compose-fixed.yml ps

# 2. Проверить web директорию
echo ""
echo "📁 Проверка web директории:"
ls -la /root/gtmall/web/

# 3. Проверить содержимое web контейнера
echo ""
echo "🐳 Проверка web контейнера:"
docker exec gtm_web ls -la /usr/share/nginx/html/

# 4. Проверить nginx конфигурацию
echo ""
echo "⚙️ Проверка nginx конфигурации:"
docker exec gtm_web nginx -t

# 5. Проверить логи nginx
echo ""
echo "📋 Логи nginx:"
docker logs gtm_web --tail=10

# 6. Проверить логи Traefik
echo ""
echo "📋 Логи Traefik:"
docker logs gtm_traefik --tail=10

# 7. Проверить сеть
echo ""
echo "🌐 Проверка сети:"
docker network ls | grep gtmall

# 8. Проверить маршруты Traefik
echo ""
echo "🛣️ Проверка маршрутов Traefik:"
docker exec gtm_traefik traefik version

# 9. Проверить SSL сертификаты
echo ""
echo "🔒 Проверка SSL сертификатов:"
docker exec gtm_traefik ls -la /etc/traefik/ssl/gtm.baby-ssl-bundle/

# 10. Тест подключения
echo ""
echo "🧪 Тест подключения к web контейнеру:"
docker exec gtm_traefik curl -I http://gtm_web:80 