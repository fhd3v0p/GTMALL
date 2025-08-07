#!/bin/bash

echo "🔄 Переименование папки SSL сертификатов..."
echo "============================================="

# Проверить наличие старой папки
if [ -d "/root/gtmall/gtm.baby-ssl-bundle" ]; then
    echo "📁 Найдена папка gtm.baby-ssl-bundle"
    
    # Остановить контейнеры
    echo "🛑 Останавливаем контейнеры..."
    docker-compose -f docker-compose-fixed.yml down
    
    # Переименовать папку
    echo "🔄 Переименовываем папку..."
    mv /root/gtmall/gtm.baby-ssl-bundle /root/gtmall/ssl
    
    # Проверить результат
    echo "✅ Проверяем результат:"
    ls -la /root/gtmall/ssl/
    
    # Применить новую конфигурацию
    echo "📝 Применяем новую конфигурацию..."
    cp traefik/traefik-final.yml traefik/traefik.yml
    
    # Запустить заново
    echo "🚀 Запускаем с новой конфигурацией..."
    docker-compose -f docker-compose-fixed.yml up -d
    
    # Ждать запуска
    echo "⏳ Ждем запуска..."
    sleep 10
    
    # Проверить статус
    echo "📊 Проверка статуса:"
    docker-compose -f docker-compose-fixed.yml ps
    
    echo ""
    echo "✅ Переименование завершено!"
    echo "🌐 Проверьте: https://gtm.baby"
else
    echo "❌ Папка gtm.baby-ssl-bundle не найдена!"
    echo "📁 Проверьте содержимое /root/gtmall/:"
    ls -la /root/gtmall/
fi 