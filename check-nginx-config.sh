#!/bin/bash

# ============================================================================
# GTM Nginx Config Check Script
# ============================================================================

set -e

echo "🔍 GTM Nginx Config Check Script"
echo "================================="

# ============================================================================
# Проверка nginx.conf
# ============================================================================
echo "📋 Проверка nginx.conf..."

if [ -f "nginx.conf" ]; then
    echo "✅ nginx.conf найден"
    
    # Проверка синтаксиса (если nginx установлен)
    if command -v nginx &> /dev/null; then
        echo "🔍 Проверка синтаксиса nginx..."
        if nginx -t -c "$(pwd)/nginx.conf" 2>/dev/null; then
            echo "✅ Конфигурация nginx корректна"
        else
            echo "❌ Ошибка в конфигурации nginx"
            exit 1
        fi
    else
        echo "⚠️  nginx не установлен локально, пропускаем проверку синтаксиса"
    fi
    
    # Проверка структуры конфигурации
    echo "🔍 Проверка структуры конфигурации..."
    
    # Проверка наличия SSL блоков
    if grep -q "ssl_certificate" nginx.conf; then
        echo "✅ SSL конфигурация найдена"
    else
        echo "❌ SSL конфигурация не найдена"
    fi
    
    # Проверка server блоков
    if grep -q "server_name gtm.baby" nginx.conf; then
        echo "✅ Конфигурация для gtm.baby найдена"
    else
        echo "❌ Конфигурация для gtm.baby не найдена"
    fi
    
    # Проверка API прокси
    if grep -q "proxy_pass" nginx.conf; then
        echo "✅ API прокси настроен"
    else
        echo "❌ API прокси не настроен"
    fi
    
else
    echo "❌ nginx.conf не найден"
    exit 1
fi

# ============================================================================
# Проверка SSL сертификатов
# ============================================================================
echo ""
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
        fi
    else
        echo "❌ Не найдены необходимые файлы сертификатов"
    fi
else
    echo "❌ Директория SSL сертификатов не найдена: $SSL_DIR"
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
    fi
    
    if [ -f "web/admin_new.html" ]; then
        echo "✅ admin_new.html найден"
    else
        echo "❌ admin_new.html не найден в web директории"
    fi
    
    # Проверка основных файлов Flutter
    if [ -f "web/main.dart.js" ]; then
        echo "✅ main.dart.js найден"
    else
        echo "❌ main.dart.js не найден"
    fi
    
    if [ -d "web/assets" ]; then
        echo "✅ assets директория найдена"
    else
        echo "❌ assets директория не найдена"
    fi
    
else
    echo "❌ Web директория не найдена"
fi

# ============================================================================
# Проверка Docker Compose
# ============================================================================
echo ""
echo "🐳 Проверка Docker Compose..."

if [ -f "docker-compose-simple.yml" ]; then
    echo "✅ docker-compose-simple.yml найден"
    
    # Проверка структуры
    if grep -q "nginx:" docker-compose-simple.yml; then
        echo "✅ nginx сервис настроен"
    else
        echo "❌ nginx сервис не настроен"
    fi
    
    if grep -q "api:" docker-compose-simple.yml; then
        echo "✅ api сервис настроен"
    else
        echo "❌ api сервис не настроен"
    fi
    
else
    echo "❌ docker-compose-simple.yml не найден"
fi

echo ""
echo "✅ Проверка завершена!"
echo "🚀 Для деплоя на сервере выполните: ./deploy-nginx.sh" 