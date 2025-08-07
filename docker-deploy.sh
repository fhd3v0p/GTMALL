#!/bin/bash

# ============================================================================
# GTM Docker Deployment Script
# ============================================================================

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функции для вывода
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Проверка наличия Docker
check_docker() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker не установлен. Установите Docker и попробуйте снова."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose не установлен. Установите Docker Compose и попробуйте снова."
        exit 1
    fi
    
    log_success "Docker и Docker Compose найдены"
}

# Проверка переменных окружения
check_env() {
    if [ ! -f "env.production" ]; then
        log_error "Файл env.production не найден. Создайте его на основе env.example"
        exit 1
    fi
    
    log_success "Переменные окружения найдены"
}

# Создание необходимых директорий
create_directories() {
    log_info "Создание необходимых директорий..."
    
    mkdir -p logs
    mkdir -p database/init
    mkdir -p gtm.baby-ssl-bundle
    
    log_success "Директории созданы"
}

# Проверка SSL сертификатов
check_ssl() {
    log_info "Проверка SSL сертификатов..."
    
    if [ ! -f "gtm.baby-ssl-bundle/domain.cert.pem" ] || [ ! -f "gtm.baby-ssl-bundle/private.key.pem" ]; then
        log_warning "SSL сертификаты не найдены. Traefik будет использовать Let's Encrypt"
    else
        log_success "SSL сертификаты найдены"
    fi
}

# Остановка существующих контейнеров
stop_containers() {
    log_info "Остановка существующих контейнеров..."
    
    docker-compose down --remove-orphans || true
    
    log_success "Контейнеры остановлены"
}

# Сборка образов
build_images() {
    log_info "Сборка Docker образов..."
    
    docker-compose build --no-cache
    
    log_success "Образы собраны"
}

# Запуск сервисов
start_services() {
    log_info "Запуск сервисов..."
    
    # Запуск базы данных и Redis
    docker-compose up -d postgres redis
    
    log_info "Ожидание готовности базы данных..."
    sleep 30
    
    # Запуск остальных сервисов
    docker-compose up -d
    
    log_success "Сервисы запущены"
}

# Проверка статуса сервисов
check_services() {
    log_info "Проверка статуса сервисов..."
    
    sleep 10
    
    docker-compose ps
    
    log_success "Проверка завершена"
}

# Показ логов
show_logs() {
    log_info "Показ логов сервисов..."
    
    echo "=== Логи Traefik ==="
    docker-compose logs traefik --tail=20
    
    echo "=== Логи API ==="
    docker-compose logs api --tail=20
    
    echo "=== Логи Bot ==="
    docker-compose logs bot --tail=20
    
    echo "=== Логи Web ==="
    docker-compose logs web --tail=20
}

# Основная функция
main() {
    log_info "Начинаем развертывание GTM проекта..."
    
    check_docker
    check_env
    create_directories
    check_ssl
    stop_containers
    build_images
    start_services
    check_services
    
    log_success "Развертывание завершено!"
    log_info "Доступные URL:"
    echo "  🌐 Основной сайт: https://gtm.baby"
    echo "  🔧 API: https://api.gtm.baby"
    echo "  📊 Traefik Dashboard: https://traefik.gtm.baby"
    echo "  👨‍💼 Admin Panel: https://admin.gtm.baby"
    
    log_info "Для просмотра логов выполните: ./docker-deploy.sh logs"
}

# Обработка аргументов
case "${1:-}" in
    "logs")
        show_logs
        ;;
    "stop")
        log_info "Остановка сервисов..."
        docker-compose down
        log_success "Сервисы остановлены"
        ;;
    "restart")
        log_info "Перезапуск сервисов..."
        docker-compose restart
        log_success "Сервисы перезапущены"
        ;;
    "status")
        docker-compose ps
        ;;
    "clean")
        log_warning "Удаление всех контейнеров и образов..."
        docker-compose down --volumes --remove-orphans
        docker system prune -f
        log_success "Очистка завершена"
        ;;
    *)
        main
        ;;
esac 