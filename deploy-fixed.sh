#!/bin/bash

# ============================================================================
# GTM Fixed Deployment Script
# ============================================================================

set -e

echo "🚀 GTM Fixed Deployment Script"
echo "==============================="
echo "Components: Traefik + API + Bot + Web"
echo "SSL: gtm.baby-ssl-bundle"
echo "API Port: 5000"
echo ""

# ============================================================================
# Проверка SSL сертификатов
# ============================================================================
echo "🔒 Проверка SSL сертификатов..."

SSL_DIR="gtm.baby-ssl-bundle"
if [ -d "$SSL_DIR" ]; then
    echo "✅ SSL сертификаты найдены в $SSL_DIR"
    
    if [ -f "$SSL_DIR/domain.cert.pem" ] && [ -f "$SSL_DIR/private.key.pem" ]; then
        echo "✅ Сертификат и ключ найдены"
        
        if openssl x509 -in "$SSL_DIR/domain.cert.pem" -checkend 0 -noout 2>/dev/null; then
            echo "✅ Сертификат действителен"
        else
            echo "❌ Сертификат истек!"
            exit 1
        fi
    else
        echo "❌ Не найдены необходимые файлы сертификатов"
        exit 1
    fi
else
    echo "❌ Директория SSL сертификатов не найдена: $SSL_DIR"
    exit 1
fi

# ============================================================================
# Проверка web директории
# ============================================================================
echo ""
echo "📁 Проверка web директории..."

if [ -d "/root/gtmall/web" ]; then
    echo "✅ Web директория найдена: /root/gtmall/web"
    ls -la /root/gtmall/web/ | head -5
else
    echo "❌ Web директория не найдена: /root/gtmall/web"
    exit 1
fi

# ============================================================================
# Остановка старых контейнеров
# ============================================================================
echo ""
echo "🛑 Останавливаем старые контейнеры..."

docker-compose down 2>/dev/null || true
docker-compose -f docker-compose-fixed.yml down 2>/dev/null || true

# Очистка Docker
echo "🧹 Очищаем Docker..."
docker system prune -f

# ============================================================================
# Копирование исправленных файлов
# ============================================================================
echo ""
echo "📝 Копирование исправленных файлов..."

# Копируем исправленную конфигурацию Traefik
cp traefik/traefik-fixed.yml traefik/traefik.yml

# ============================================================================
# Запуск с исправленной конфигурацией
# ============================================================================
echo ""
echo "🚀 Запускаем с исправленной конфигурацией..."

docker-compose -f docker-compose-fixed.yml up -d --build

# ============================================================================
# Проверка статуса
# ============================================================================
echo ""
echo "📊 Проверка статуса контейнеров..."

sleep 10
docker-compose -f docker-compose-fixed.yml ps

echo ""
echo "📋 Логи контейнеров:"
echo "docker-compose -f docker-compose-fixed.yml logs -f"

echo ""
echo "✅ Деплой завершен!"
echo "🌐 Доступные URL:"
echo "   - Основной сайт: https://gtm.baby"
echo "   - API: https://api.gtm.baby"
echo "   - Traefik Dashboard: https://traefik.gtm.baby"
echo ""
echo "🤖 Telegram Bot работает в фоне (без веб-интерфейса)" 