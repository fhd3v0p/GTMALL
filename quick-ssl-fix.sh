#!/bin/bash

echo "🚀 Быстрое исправление SSL..."

# Остановить контейнеры
docker-compose -f docker-compose-fixed.yml down

# Обновить конфигурацию
cp traefik/traefik-fixed.yml traefik/traefik.yml

# Запустить заново
docker-compose -f docker-compose-fixed.yml up -d

echo "✅ Готово! Проверьте https://gtm.baby" 