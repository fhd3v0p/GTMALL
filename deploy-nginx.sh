#!/bin/bash

# ============================================================================
# GTM Nginx Deployment Script
# ============================================================================

set -e

echo "🚀 GTM Nginx Deployment Script"
echo "================================"

# ============================================================================
# Проверка SSL сертификатов
# ============================================================================
echo "🔒 Проверка SSL сертификатов..."

SSL_DIR="gtm.baby-ssl-bundle"
if [ -d "$SSL_DIR" ]; then
    echo "✅ SSL директория найдена: $SSL_DIR"
    
    if [ -f "$SSL_DIR/domain.cert.pem" ] && [ -f "$SSL_DIR/private.key.pem" ]; then
        echo "✅ Сертификат и ключ найдены"
        
        if openssl x509 -in "$SSL_DIR/domain.cert.pem" -checkend 0 -noout 2>/dev/null; then
            echo "✅ Сертификат действителен"
            echo "📅 Дата истечения:"
            openssl x509 -in "$SSL_DIR/domain.cert.pem" -noout -enddate
        else
            echo "❌ Сертификат истек!"
            echo "🔄 Запустите: ./setup-ssl.sh"
            exit 1
        fi
    else
        echo "❌ Не найдены необходимые файлы сертификатов"
        echo "🔄 Запустите: ./setup-ssl.sh"
        exit 1
    fi
else
    echo "❌ Директория SSL сертификатов не найдена: $SSL_DIR"
    echo "🔄 Запустите: ./setup-ssl.sh"
    exit 1
fi

# ============================================================================
# Проверка web файлов
# ============================================================================
echo ""
echo "📁 Проверка web файлов..."

if [ -d "web" ]; then
    echo "✅ Web директория найдена"
    
    if [ -f "web/index.html" ]; then
        echo "✅ index.html найден"
    else
        echo "❌ index.html не найден в web директории"
        exit 1
    fi
else
    echo "❌ Web директория не найдена"
    echo "📝 Убедитесь что файлы Flutter web находятся в ./web/"
    exit 1
fi

# ============================================================================
# Остановка старых контейнеров
# ============================================================================
echo ""
echo "🛑 Остановка старых контейнеров..."

if [ -f "docker-compose.yml" ]; then
    docker-compose down --volumes --remove-orphans
fi

if [ -f "docker-compose-simple.yml" ]; then
    docker-compose -f docker-compose-simple.yml down --volumes --remove-orphans
fi

# Очистка Docker
docker system prune -f

# ============================================================================
# Запуск с Nginx
# ============================================================================
echo ""
echo "🚀 Запуск с Nginx..."

# Используем упрощенный docker-compose
if [ -f "docker-compose-simple.yml" ]; then
    echo "✅ Запускаем с docker-compose-simple.yml"
    docker-compose -f docker-compose-simple.yml up -d --build
else
    echo "❌ Файл docker-compose-simple.yml не найден"
    exit 1
fi

# ============================================================================
# Проверка статуса
# ============================================================================
echo ""
echo "📊 Проверка статуса контейнеров..."
sleep 10

docker-compose -f docker-compose-simple.yml ps

echo ""
echo "📋 Логи контейнеров:"
echo "===================="

echo "🔍 Nginx логи:"
docker-compose -f docker-compose-simple.yml logs nginx

echo ""
echo "🔍 API логи:"
docker-compose -f docker-compose-simple.yml logs api

echo ""
echo "🔍 PostgreSQL логи:"
docker-compose -f docker-compose-simple.yml logs postgres

echo ""
echo "🔍 Redis логи:"
docker-compose -f docker-compose-simple.yml logs redis

# ============================================================================
# Проверка доступности
# ============================================================================
echo ""
echo "🌐 Проверка доступности..."

echo "🔍 Проверка HTTP -> HTTPS редирект:"
curl -I http://gtm.baby 2>/dev/null | head -1 || echo "❌ HTTP недоступен"

echo "🔍 Проверка HTTPS:"
curl -I https://gtm.baby 2>/dev/null | head -1 || echo "❌ HTTPS недоступен"

echo "🔍 Проверка API:"
curl -I https://api.gtm.baby/health 2>/dev/null | head -1 || echo "❌ API недоступен"

echo ""
echo "✅ Деплой завершен!"
echo "🌐 Сайт должен быть доступен на: https://gtm.baby"
echo "🔗 API доступен на: https://api.gtm.baby"
echo "📊 Админ панель: https://gtm.baby/admin/"
echo ""
echo "🔍 Для проверки:"
echo "   curl -I https://gtm.baby"
echo "   curl -I https://api.gtm.baby/health" 