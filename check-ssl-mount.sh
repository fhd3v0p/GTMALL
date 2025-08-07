#!/bin/bash

echo "🔍 Проверка монтирования SSL сертификатов..."
echo "============================================="

# Проверить наличие сертификатов на хосте
echo "📁 Проверка сертификатов на хосте:"
ls -la /root/gtmall/ssl/

# Проверить монтирование в контейнере
echo ""
echo "🐳 Проверка монтирования в Traefik контейнере:"
docker exec gtm_traefik ls -la /etc/traefik/ssl/

# Проверить права доступа
echo ""
echo "🔐 Проверка прав доступа:"
docker exec gtm_traefik ls -la /etc/traefik/ssl/domain.cert.pem
docker exec gtm_traefik ls -la /etc/traefik/ssl/private.key.pem

# Проверить валидность сертификата в контейнере
echo ""
echo "✅ Проверка валидности сертификата в контейнере:"
docker exec gtm_traefik openssl x509 -in /etc/traefik/ssl/domain.cert.pem -text -noout | grep -E "(Subject:|DNS:|Not After)"

echo ""
echo "📋 Логи Traefik:"
docker-compose -f docker-compose-fixed.yml logs traefik --tail=10 