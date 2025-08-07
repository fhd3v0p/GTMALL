#!/bin/bash

# ============================================================================
# Управление Nginx для GTM.baby
# ============================================================================

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для вывода с цветом
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Проверяем, что nginx установлен
check_nginx() {
    if ! command -v nginx &> /dev/null; then
        print_error "Nginx не установлен. Запустите install-nginx.sh сначала."
        exit 1
    fi
    print_status "Nginx установлен"
}

# Показываем статус nginx
show_status() {
    print_info "Статус Nginx:"
    sudo systemctl status nginx --no-pager
}

# Проверяем конфигурацию
test_config() {
    print_info "Проверка конфигурации nginx:"
    if sudo nginx -t; then
        print_status "Конфигурация корректна"
    else
        print_error "Ошибка в конфигурации"
        exit 1
    fi
}

# Перезапускаем nginx
reload_nginx() {
    print_info "Перезапуск nginx:"
    sudo systemctl reload nginx
    print_status "Nginx перезапущен"
}

# Показываем логи
show_logs() {
    print_info "Последние логи ошибок:"
    sudo tail -n 20 /var/log/nginx/error.log
    
    if [ -f "/var/log/nginx/gtm.baby.error.log" ]; then
        print_info "Логи GTM.baby:"
        sudo tail -n 20 /var/log/nginx/gtm.baby.error.log
    fi
}

# Показываем доступные сайты
show_sites() {
    print_info "Активные сайты:"
    ls -la /etc/nginx/sites-enabled/
}

# Проверяем SSL сертификаты
check_ssl() {
    print_info "Проверка SSL сертификатов:"
    if [ -f "/etc/nginx/ssl/domain.cert.pem" ]; then
        print_status "SSL сертификат найден"
        openssl x509 -in /etc/nginx/ssl/domain.cert.pem -text -noout | grep -E "(Subject:|Not Before:|Not After:)"
    else
        print_warning "SSL сертификат не найден"
    fi
}

# Проверяем файлы сайта
check_site_files() {
    print_info "Проверка файлов сайта:"
    if [ -d "/var/www/gtm.baby" ]; then
        print_status "Директория сайта найдена"
        ls -la /var/www/gtm.baby/ | head -10
    else
        print_warning "Директория сайта не найдена"
    fi
}

# Полная диагностика
full_diagnostic() {
    print_info "=== ПОЛНАЯ ДИАГНОСТИКА ==="
    check_nginx
    test_config
    show_status
    check_ssl
    check_site_files
    show_sites
    print_info "=== КОНЕЦ ДИАГНОСТИКИ ==="
}

# Показываем помощь
show_help() {
    echo "Использование: $0 [команда]"
    echo ""
    echo "Команды:"
    echo "  status     - Показать статус nginx"
    echo "  test       - Проверить конфигурацию"
    echo "  reload     - Перезапустить nginx"
    echo "  logs       - Показать логи"
    echo "  sites      - Показать активные сайты"
    echo "  ssl        - Проверить SSL сертификаты"
    echo "  files      - Проверить файлы сайта"
    echo "  diagnostic - Полная диагностика"
    echo "  help       - Показать эту справку"
    echo ""
}

# Основная логика
case "${1:-help}" in
    "status")
        check_nginx
        show_status
        ;;
    "test")
        check_nginx
        test_config
        ;;
    "reload")
        check_nginx
        test_config
        reload_nginx
        ;;
    "logs")
        check_nginx
        show_logs
        ;;
    "sites")
        show_sites
        ;;
    "ssl")
        check_ssl
        ;;
    "files")
        check_site_files
        ;;
    "diagnostic")
        full_diagnostic
        ;;
    "help"|*)
        show_help
        ;;
esac 