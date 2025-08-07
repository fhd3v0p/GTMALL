#!/bin/bash

echo "🔍 Проверка монтирования SSL сертификатов..."
echo "============================================="

# Проверить наличие сертификатов на хосте
echo "📁 Проверка сертификатов на хосте:"
ls -la /root/gtmall/gtm.baby-ssl-bundle/

# Проверить монтирование в контейнере
echo ""
echo "🐳 Проверка монтирования в Traefik контейнере:"
docker exec gtm_traefik ls -la /etc/traefik/ssl/gtm.baby-ssl-bundle/

# Проверить права доступа
echo ""
echo "🔐 Проверка прав доступа:"
docker exec gtm_traefik ls -la /etc/traefik/ssl/gtm.baby-ssl-bundle/domain.cert.pem
docker exec gtm_traefik ls -la /etc/traefik/ssl/gtm.baby-ssl-bundle/private.key.pem

# Проверить валидность сертификата в контейнере
echo ""
echo "✅ Проверка валидности сертификата в контейнере:"
docker exec gtm_traefik openssl x509 -in /etc/traefik/ssl/gtm.baby-ssl-bundle/domain.cert.pem -text -noout | grep -E "(Subject:|DNS:|Not After)"

echo ""
echo "📋 Логи Traefik:"
docker-compose -f docker-compose-fixed.yml logs traefik --tail=10 