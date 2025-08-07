#!/bin/bash

# ============================================================================
# Установка Nginx на сервер
# ============================================================================

set -e

echo "🚀 Начинаем установку Nginx..."

# Обновляем пакеты
echo "📦 Обновляем пакеты..."
sudo apt update

# Устанавливаем nginx
echo "📥 Устанавливаем nginx..."
sudo apt install -y nginx

# Проверяем статус nginx
echo "🔍 Проверяем статус nginx..."
sudo systemctl status nginx --no-pager

# Настраиваем автозапуск
echo "⚙️  Настраиваем автозапуск nginx..."
sudo systemctl enable nginx

# Создаем резервную копию дефолтной конфигурации
echo "💾 Создаем резервную копию дефолтной конфигурации..."
sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.backup

echo "✅ Nginx установлен успешно!"
echo ""
echo "📝 Следующие шаги:"
echo "   1. Запустите скрипт setup-nginx.sh для настройки сайта"
echo "   2. Убедитесь, что SSL сертификаты находятся в gtm.baby-ssl-bundle/"
echo "   3. Проверьте, что файлы сайта находятся в web/"
echo ""
echo "🌐 Nginx будет доступен на порту 80 и 443" 