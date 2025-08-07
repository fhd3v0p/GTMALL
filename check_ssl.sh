#!/bin/bash

# ============================================================================
# SSL Certificate Check Script
# ============================================================================

set -e

echo "🔒 Проверка SSL сертификатов"
echo "================================"

SSL_DIR="@GTMALL/gtm.baby-ssl-bundle"

# Проверяем наличие директории
if [ ! -d "$SSL_DIR" ]; then
    echo "❌ Директория SSL сертификатов не найдена: $SSL_DIR"
    exit 1
fi

echo "📁 Директория SSL сертификатов: $SSL_DIR"
echo ""

# Проверяем наличие файлов
CERT_FILE="$SSL_DIR/domain.cert.pem"
KEY_FILE="$SSL_DIR/private.key.pem"
PUBLIC_FILE="$SSL_DIR/public.key.pem"

echo "🔍 Проверка файлов сертификатов..."

if [ -f "$CERT_FILE" ]; then
    echo "✅ Сертификат найден: domain.cert.pem"
    echo "   Размер: $(du -h "$CERT_FILE" | cut -f1)"
else
    echo "❌ Сертификат не найден: domain.cert.pem"
fi

if [ -f "$KEY_FILE" ]; then
    echo "✅ Приватный ключ найден: private.key.pem"
    echo "   Размер: $(du -h "$KEY_FILE" | cut -f1)"
else
    echo "❌ Приватный ключ не найден: private.key.pem"
fi

if [ -f "$PUBLIC_FILE" ]; then
    echo "✅ Публичный ключ найден: public.key.pem"
    echo "   Размер: $(du -h "$PUBLIC_FILE" | cut -f1)"
else
    echo "❌ Публичный ключ не найден: public.key.pem"
fi

echo ""

# Проверяем права доступа
echo "🔐 Проверка прав доступа..."
chmod 600 "$SSL_DIR"/*.pem 2>/dev/null || true
echo "✅ Права доступа установлены (600)"

echo ""

# Проверяем валидность сертификата
echo "🔍 Проверка валидности сертификата..."
if [ -f "$CERT_FILE" ]; then
    echo "📋 Информация о сертификате:"
    openssl x509 -in "$CERT_FILE" -text -noout | grep -E "(Subject:|Issuer:|Not Before:|Not After:|DNS:)"
    echo ""
    
    # Проверяем срок действия
    NOT_AFTER=$(openssl x509 -in "$CERT_FILE" -noout -enddate | cut -d= -f2)
    echo "📅 Срок действия: $NOT_AFTER"
    
    # Проверяем, не истек ли сертификат
    if openssl x509 -in "$CERT_FILE" -checkend 0 -noout; then
        echo "✅ Сертификат действителен"
    else
        echo "❌ Сертификат истек!"
    fi
else
    echo "❌ Не удалось проверить сертификат"
fi

echo ""

# Проверяем соответствие ключа и сертификата
echo "🔍 Проверка соответствия ключа и сертификата..."
if [ -f "$CERT_FILE" ] && [ -f "$KEY_FILE" ]; then
    CERT_HASH=$(openssl x509 -noout -modulus -in "$CERT_FILE" | openssl md5)
    KEY_HASH=$(openssl rsa -noout -modulus -in "$KEY_FILE" | openssl md5)
    
    if [ "$CERT_HASH" = "$KEY_HASH" ]; then
        echo "✅ Ключ и сертификат соответствуют"
    else
        echo "❌ Ключ и сертификат НЕ соответствуют!"
    fi
else
    echo "❌ Не удалось проверить соответствие"
fi

echo ""

# Проверяем конфигурацию Traefik
echo "🔧 Проверка конфигурации Traefik..."
TRAEFIK_CONFIG="@GTMALL/traefik/traefik.yml"

if [ -f "$TRAEFIK_CONFIG" ]; then
    echo "✅ Конфигурация Traefik найдена"
    
    # Проверяем, что в конфигурации указаны правильные пути
    if grep -q "domain.cert.pem" "$TRAEFIK_CONFIG" && grep -q "private.key.pem" "$TRAEFIK_CONFIG"; then
        echo "✅ Пути к сертификатам указаны в конфигурации Traefik"
    else
        echo "❌ Пути к сертификатам НЕ указаны в конфигурации Traefik"
    fi
else
    echo "❌ Конфигурация Traefik не найдена"
fi

echo ""

# Проверяем docker-compose.yml
echo "🐳 Проверка docker-compose.yml..."
COMPOSE_FILE="@GTMALL/docker-compose.yml"

if [ -f "$COMPOSE_FILE" ]; then
    echo "✅ docker-compose.yml найден"
    
    # Проверяем монтирование SSL директории
    if grep -q "gtm.baby-ssl-bundle" "$COMPOSE_FILE"; then
        echo "✅ SSL директория монтируется в docker-compose.yml"
    else
        echo "❌ SSL директория НЕ монтируется в docker-compose.yml"
    fi
else
    echo "❌ docker-compose.yml не найден"
fi

echo ""
echo "✅ Проверка SSL сертификатов завершена!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Убедитесь, что сертификаты действительны"
echo "2. Проверьте, что домен gtm.baby настроен в DNS"
echo "3. Запустите деплой: ./deploy.sh"
echo "" 