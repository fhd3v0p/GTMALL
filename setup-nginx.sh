#!/bin/bash

# ============================================================================
# Настройка Nginx для GTM.baby
# ============================================================================

set -e

echo "🚀 Начинаем настройку Nginx для GTM.baby..."

# Проверяем, что мы в правильной директории
if [ ! -d "web" ]; then
    echo "❌ Ошибка: директория 'web' не найдена"
    exit 1
fi

# Создаем директории для nginx
echo "📁 Создаем директории..."
sudo mkdir -p /var/www/gtm.baby
sudo mkdir -p /etc/nginx/sites-available
sudo mkdir -p /etc/nginx/sites-enabled
sudo mkdir -p /etc/nginx/ssl

# Копируем файлы сайта
echo "📋 Копируем файлы сайта..."
sudo cp -r web/* /var/www/gtm.baby/

# Устанавливаем права доступа
echo "🔐 Устанавливаем права доступа..."
sudo chown -R www-data:www-data /var/www/gtm.baby
sudo chmod -R 755 /var/www/gtm.baby

# Копируем SSL сертификаты (если они есть)
if [ -d "gtm.baby-ssl-bundle" ]; then
    echo "🔒 Копируем SSL сертификаты..."
    sudo cp -r gtm.baby-ssl-bundle/* /etc/nginx/ssl/
    sudo chown -R root:root /etc/nginx/ssl
    sudo chmod -R 600 /etc/nginx/ssl
else
    echo "⚠️  SSL сертификаты не найдены в gtm.baby-ssl-bundle"
fi

# Создаем конфигурацию nginx
echo "⚙️  Создаем конфигурацию nginx..."

cat > /tmp/gtm.baby.conf << 'EOF'
# ============================================================================
# Nginx Configuration for GTM.baby
# ============================================================================

# Основные настройки
server {
    listen 80;
    server_name gtm.baby www.gtm.baby;
    
    # Редирект на HTTPS
    return 301 https://$server_name$request_uri;
}

# HTTPS сервер
server {
    listen 443 ssl http2;
    server_name gtm.baby www.gtm.baby;
    
    # SSL сертификаты
    ssl_certificate /etc/nginx/ssl/domain.cert.pem;
    ssl_certificate_key /etc/nginx/ssl/private.key.pem;
    
    # SSL настройки
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    
    # Корневая директория
    root /var/www/gtm.baby;
    index index.html;
    
    # Gzip сжатие
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;
    
    # Обработка Flutter web routing
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # Кэширование статических файлов
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        add_header Access-Control-Allow-Origin "*";
    }
    
    # API прокси (если API запущен на том же сервере)
    location /api/ {
        proxy_pass http://localhost:5000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Port $server_port;
    }
    
    # Health check
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
    
    # Логи
    access_log /var/log/nginx/gtm.baby.access.log;
    error_log /var/log/nginx/gtm.baby.error.log;
}

# HTTP сервер для API (если нужно)
server {
    listen 80;
    server_name api.gtm.baby;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Копируем конфигурацию
sudo cp /tmp/gtm.baby.conf /etc/nginx/sites-available/gtm.baby

# Активируем сайт
echo "🔗 Активируем сайт..."
sudo ln -sf /etc/nginx/sites-available/gtm.baby /etc/nginx/sites-enabled/

# Удаляем дефолтную конфигурацию
sudo rm -f /etc/nginx/sites-enabled/default

# Проверяем конфигурацию
echo "🔍 Проверяем конфигурацию nginx..."
sudo nginx -t

if [ $? -eq 0 ]; then
    echo "✅ Конфигурация nginx корректна"
    
    # Перезапускаем nginx
    echo "🔄 Перезапускаем nginx..."
    sudo systemctl reload nginx
    
    echo "🎉 Настройка завершена успешно!"
    echo ""
    echo "📋 Что было сделано:"
    echo "   - Скопированы файлы сайта в /var/www/gtm.baby"
    echo "   - Настроена конфигурация nginx"
    echo "   - Настроены SSL сертификаты"
    echo "   - Активирован сайт"
    echo ""
    echo "🌐 Сайт должен быть доступен по адресу: https://gtm.baby"
    echo ""
    echo "📝 Для проверки статуса используйте:"
    echo "   sudo systemctl status nginx"
    echo "   sudo nginx -t"
    echo "   sudo tail -f /var/log/nginx/gtm.baby.error.log"
else
    echo "❌ Ошибка в конфигурации nginx"
    exit 1
fi 