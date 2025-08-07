#!/bin/bash

echo "🧪 Тестирование чтения SSL сертификатов в Traefik..."
echo "===================================================="

# Проверить, может ли Traefik прочитать сертификаты
echo "📖 Проверка чтения сертификатов:"
docker exec gtm_traefik cat /etc/traefik/ssl/gtm.baby-ssl-bundle/domain.cert.pem | head -5

echo ""
echo "🔑 Проверка чтения ключа:"
docker exec gtm_traefik cat /etc/traefik/ssl/gtm.baby-ssl-bundle/private.key.pem | head -5

echo ""
echo "✅ Проверка валидности сертификата:"
docker exec gtm_traefik openssl x509 -in /etc/traefik/ssl/gtm.baby-ssl-bundle/domain.cert.pem -text -noout | grep -E "(Subject:|DNS:|Not After)"

echo ""
echo "🔍 Проверка конфигурации Traefik:"
docker exec gtm_traefik cat /etc/traefik/traefik.yml | grep -A 5 -B 5 "certificates"

echo ""
echo "📋 Последние логи Traefik:"
docker logs gtm_traefik --tail=20 