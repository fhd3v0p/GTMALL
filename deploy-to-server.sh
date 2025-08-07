#!/bin/bash

# ============================================================================
# GTM Server Deployment Script
# ============================================================================

set -e

echo "🚀 GTM Server Deployment Script"
echo "================================"

# ============================================================================
# Проверка аргументов
# ============================================================================
if [ $# -eq 0 ]; then
    echo "❌ Укажите IP адрес сервера"
    echo "Использование: ./deploy-to-server.sh <SERVER_IP> [SSH_KEY_PATH]"
    echo "Пример: ./deploy-to-server.sh 31.56.39.165 ~/.ssh/id_rsa_46.203.233.218"
    exit 1
fi

SERVER_IP=$1
SSH_KEY=${2:-"~/.ssh/id_rsa"}

echo "🌐 Сервер: $SERVER_IP"
echo "🔑 SSH ключ: $SSH_KEY"

# ============================================================================
# Проверка подключения к серверу
# ============================================================================
echo ""
echo "🔍 Проверка подключения к серверу..."

if ssh -i "$SSH_KEY" -o ConnectTimeout=10 -o BatchMode=yes root@"$SERVER_IP" "echo 'Connection successful'" 2>/dev/null; then
    echo "✅ Подключение к серверу успешно"
else
    echo "❌ Не удалось подключиться к серверу"
    echo "Проверьте:"
    echo "  - IP адрес сервера: $SERVER_IP"
    echo "  - SSH ключ: $SSH_KEY"
    echo "  - Доступность сервера"
    exit 1
fi

# ============================================================================
# Создание архива для деплоя
# ============================================================================
echo ""
echo "📦 Создание архива для деплоя..."

DEPLOY_ARCHIVE="gtm-nginx-deploy.tar.gz"

# Создаем архив с необходимыми файлами
tar -czf "$DEPLOY_ARCHIVE" \
    nginx.conf \
    docker-compose-simple.yml \
    setup-ssl.sh \
    deploy-nginx.sh \
    check-nginx-config.sh \
    NGINX_SETUP.md \
    web/ \
    gtm.baby-ssl-bundle/ \
    api/ \
    database/ \
    bot/

echo "✅ Архив создан: $DEPLOY_ARCHIVE"

# ============================================================================
# Загрузка файлов на сервер
# ============================================================================
echo ""
echo "📤 Загрузка файлов на сервер..."

# Создаем директорию на сервере
ssh -i "$SSH_KEY" root@"$SERVER_IP" "mkdir -p /root/gtm-nginx"

# Загружаем архив
scp -i "$SSH_KEY" "$DEPLOY_ARCHIVE" root@"$SERVER_IP":/root/gtm-nginx/

# Распаковываем на сервере
ssh -i "$SSH_KEY" root@"$SERVER_IP" "cd /root/gtm-nginx && tar -xzf $DEPLOY_ARCHIVE"

echo "✅ Файлы загружены на сервер"

# ============================================================================
# Настройка SSL на сервере
# ============================================================================
echo ""
echo "🔒 Настройка SSL на сервере..."

ssh -i "$SSH_KEY" root@"$SERVER_IP" "cd /root/gtm-nginx && chmod +x setup-ssl.sh && ./setup-ssl.sh"

# ============================================================================
# Проверка конфигурации на сервере
# ============================================================================
echo ""
echo "🔍 Проверка конфигурации на сервере..."

ssh -i "$SSH_KEY" root@"$SERVER_IP" "cd /root/gtm-nginx && chmod +x check-nginx-config.sh && ./check-nginx-config.sh"

# ============================================================================
# Деплой на сервере
# ============================================================================
echo ""
echo "🚀 Запуск деплоя на сервере..."

ssh -i "$SSH_KEY" root@"$SERVER_IP" "cd /root/gtm-nginx && chmod +x deploy-nginx.sh && ./deploy-nginx.sh"

# ============================================================================
# Проверка результата
# ============================================================================
echo ""
echo "📊 Проверка результата..."

echo "🔍 Статус контейнеров:"
ssh -i "$SSH_KEY" root@"$SERVER_IP" "cd /root/gtm-nginx && docker-compose -f docker-compose-simple.yml ps"

echo ""
echo "🔍 Проверка доступности:"
ssh -i "$SSH_KEY" root@"$SERVER_IP" "curl -I https://gtm.baby 2>/dev/null | head -1 || echo '❌ HTTPS недоступен'"

echo ""
echo "🔍 Проверка API:"
ssh -i "$SSH_KEY" root@"$SERVER_IP" "curl -I https://api.gtm.baby/health 2>/dev/null | head -1 || echo '❌ API недоступен'"

# ============================================================================
# Очистка
# ============================================================================
echo ""
echo "🧹 Очистка временных файлов..."

rm -f "$DEPLOY_ARCHIVE"

echo ""
echo "✅ Деплой завершен!"
echo "🌐 Сайт доступен на: https://gtm.baby"
echo "🔗 API доступен на: https://api.gtm.baby"
echo "📊 Админ панель: https://gtm.baby/admin/"
echo ""
echo "📋 Полезные команды для управления:"
echo "  - Проверка статуса: ssh -i $SSH_KEY root@$SERVER_IP 'cd /root/gtm-nginx && docker-compose -f docker-compose-simple.yml ps'"
echo "  - Просмотр логов: ssh -i $SSH_KEY root@$SERVER_IP 'cd /root/gtm-nginx && docker-compose -f docker-compose-simple.yml logs nginx'"
echo "  - Перезапуск: ssh -i $SSH_KEY root@$SERVER_IP 'cd /root/gtm-nginx && docker-compose -f docker-compose-simple.yml restart'"
echo "  - Остановка: ssh -i $SSH_KEY root@$SERVER_IP 'cd /root/gtm-nginx && docker-compose -f docker-compose-simple.yml down'" 