#!/bin/bash

# ============================================================================
# GTM Deployment Script (Server Version)
# ============================================================================

set -e

# Конфигурация
DEPLOY_PATH="/opt/gtm"

echo "🚀 GTM Deployment Script (Server Version)"
echo "=========================================="
echo "Deploy Path: $DEPLOY_PATH"
echo ""

# ============================================================================
# Проверка SSL сертификатов
# ============================================================================
echo "🔒 Проверка SSL сертификатов..."

SSL_DIR="gtm.baby-ssl-bundle"
if [ -d "$SSL_DIR" ]; then
    echo "✅ SSL сертификаты найдены в $SSL_DIR"
    
    # Проверяем наличие файлов
    if [ -f "$SSL_DIR/domain.cert.pem" ] && [ -f "$SSL_DIR/private.key.pem" ]; then
        echo "✅ Сертификат и ключ найдены"
        
        # Проверяем валидность сертификата
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
# Проверка Docker
# ============================================================================
echo ""
echo "🔍 Проверка Docker..."

# Проверяем Docker
if ! command -v docker &> /dev/null; then
    echo "🔧 Установка Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    systemctl enable docker
    systemctl start docker
else
    echo "✅ Docker уже установлен"
fi

# Проверяем Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "🔧 Установка Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
else
    echo "✅ Docker Compose уже установлен"
fi

# ============================================================================
# Подготовка директории
# ============================================================================
echo ""
echo "🔧 Подготовка директории..."

# Создаем директорию для деплоя
mkdir -p $DEPLOY_PATH
cd $DEPLOY_PATH
echo "✅ Директория создана: $DEPLOY_PATH"

# ============================================================================
# Копирование файлов
# ============================================================================
echo ""
echo "📁 Копирование файлов..."

# Если мы находимся в директории с проектом, копируем файлы
if [ -f "docker-compose.yml" ]; then
    echo "📋 Копирование файлов проекта..."
    cp -r * $DEPLOY_PATH/
    echo "✅ Файлы проекта скопированы"
else
    echo "⚠️  Файлы проекта не найдены в текущей директории"
    echo "Убедитесь, что вы находитесь в директории с проектом GTM"
    exit 1
fi

# ============================================================================
# Копирование SSL сертификатов
# ============================================================================
echo ""
echo "🔒 Копирование SSL сертификатов..."

# Копируем SSL сертификаты
if [ -d "gtm.baby-ssl-bundle" ]; then
    echo "📋 Копирование SSL сертификатов..."
    cp -r gtm.baby-ssl-bundle $DEPLOY_PATH/
    
    # Устанавливаем правильные права доступа
    chmod 600 $DEPLOY_PATH/gtm.baby-ssl-bundle/*.pem
    echo "✅ SSL сертификаты скопированы и права установлены"
else
    echo "❌ SSL сертификаты не найдены"
    exit 1
fi

# ============================================================================
# Настройка переменных окружения
# ============================================================================
echo ""
echo "🔧 Настройка переменных окружения..."

cd $DEPLOY_PATH

# Создаем .env файл
cat > .env << 'ENV_EOF'
# ============================================================================
# GTM Deployment Environment Variables
# ============================================================================

# Общие настройки
ENVIRONMENT=production
DOMAIN=gtm.baby
TZ=Europe/Moscow

# Supabase Configuration
SUPABASE_URL=https://rxmtovqxjsvogyywyrha.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1Mjg1NTAsImV4cCI6MjA3MDEwNDU1MH0.gDkJybktFoi486hbIVwppDfmVQlAR0fM4o4Sl1-AxhE
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=7533650686:AAEU4_nJZHGfzOv9XL4m_fDVt0q3dMDPQX8
TELEGRAM_FOLDER_LINK=https://t.me/addlist/qRX5VmLZF7E3M2U9
WEBAPP_URL=https://gtm.baby

# API Server Configuration
API_PORT=5000
API_HOST=0.0.0.0
FLASK_ENV=production

# Database Configuration
DATABASE_URL=postgresql://gtm_user:gtm_secure_password_2024@postgres:5432/gtm_db

# Redis Configuration
REDIS_URL=redis://redis:6379/0

# Traefik Configuration
TRAEFIK_DASHBOARD_AUTH=admin:gtm_secure_2024

# Logging
LOG_LEVEL=INFO
ENV_EOF

echo "✅ .env файл создан"
echo "⚠️  ВАЖНО: Отредактируйте SUPABASE_SERVICE_ROLE_KEY в .env файле!"

# ============================================================================
# Запуск сервисов
# ============================================================================
echo ""
echo "🚀 Запуск сервисов..."

# Создаем сеть Docker
echo "🌐 Создание Docker сети..."
docker network create traefik 2>/dev/null || echo "✅ Сеть traefik уже существует"

# Копируем файлы из исходного проекта (если есть)
echo "📋 Проверка исходных файлов..."
if [ -d "../gtm-prod1/bot" ]; then
    echo "📋 Копирование исходных файлов..."
    cp ../gtm-prod1/bot/bot_main.py bot/
    cp ../gtm-prod1/bot/supabase_client.py bot/
    cp ../gtm-prod1/bot/webapp_handler.py bot/
    cp ../gtm-prod1/bot/api_server.py api/
    echo "✅ Исходные файлы скопированы"
else
    echo "⚠️  Исходные файлы не найдены, используем шаблоны"
fi

# Запускаем сервисы
echo "🚀 Запуск Docker Compose..."
docker-compose up -d

# Проверяем статус
echo "📊 Статус сервисов:"
docker-compose ps

echo "✅ Деплой завершен!"

# ============================================================================
# Проверка работоспособности
# ============================================================================
echo ""
echo "🔍 Проверка работоспособности..."

echo "📊 Статус контейнеров:"
docker-compose ps

echo "📋 Логи Traefik:"
docker-compose logs --tail=10 traefik

echo "📋 Логи API:"
docker-compose logs --tail=10 api

echo "📋 Логи Bot:"
docker-compose logs --tail=10 bot

echo ""
echo "🌐 Доступные сервисы:"
echo "- API: https://api.gtm.baby"
echo "- Traefik Dashboard: https://traefik.gtm.baby"
echo "- Web App: https://gtm.baby (после добавления)"
echo ""
echo "🔧 Полезные команды:"
echo "- Просмотр логов: docker-compose logs -f"
echo "- Перезапуск: docker-compose restart"
echo "- Остановка: docker-compose down"
echo "- Обновление: docker-compose pull && docker-compose up -d"

echo ""
echo "✅ Деплой завершен!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Отредактируйте SUPABASE_SERVICE_ROLE_KEY в .env файле"
echo "2. Проверьте доступность сервисов"
echo "3. Настройте DNS записи для домена gtm.baby"
echo "" 