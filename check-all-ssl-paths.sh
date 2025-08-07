#!/bin/bash

echo "🔍 Проверка всех SSL путей в конфигурации..."
echo "=============================================="

# Проверить все файлы на наличие старых путей
echo "📋 Поиск старых путей gtm.baby-ssl-bundle:"
grep -r "gtm.baby-ssl-bundle" . --exclude-dir=.git 2>/dev/null || echo "✅ Старых путей не найдено"

echo ""
echo "📋 Поиск правильных путей ssl:"
grep -r "/root/gtmall/ssl" . --exclude-dir=.git 2>/dev/null || echo "❌ Правильных путей не найдено"

echo ""
echo "📋 Поиск путей /etc/traefik/ssl:"
grep -r "/etc/traefik/ssl" . --exclude-dir=.git 2>/dev/null || echo "❌ Путей /etc/traefik/ssl не найдено"

echo ""
echo "🔍 Проверка основных конфигурационных файлов:"

echo ""
echo "📄 docker-compose-fixed.yml:"
grep -n "ssl" docker-compose-fixed.yml

echo ""
echo "📄 traefik/traefik-final.yml:"
grep -n "ssl" traefik/traefik-final.yml

echo ""
echo "📄 traefik/traefik.yml:"
grep -n "ssl" traefik/traefik.yml

echo ""
echo "✅ Проверка завершена!" 