# 🚀 Руководство по развертыванию GTM

## 📋 Предварительные требования

### Системные требования
- Docker Engine 20.10+
- Docker Compose 2.0+
- 2GB RAM минимум
- 10GB свободного места
- Linux/Unix система

### Сетевые требования
- Домен `gtm.baby` с DNS записями:
  ```
  gtm.baby          A    YOUR_SERVER_IP
  api.gtm.baby      A    YOUR_SERVER_IP
  traefik.gtm.baby  A    YOUR_SERVER_IP
  ```
- Открытые порты: 80, 443, 8080

### SSL сертификаты
- **Автоматически**: Let's Encrypt (рекомендуется)
- **Вручную**: Скопировать в `traefik/ssl/gtm.baby-ssl-bundle/`

## 🔧 Установка и настройка

### 1. Подготовка системы

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Docker (если не установлен)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Добавление пользователя в группу docker
sudo usermod -aG docker $USER

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Клонирование и настройка

```bash
# Клонирование проекта
git clone <repository_url> @GTMALL
cd @GTMALL

# Запуск скрипта настройки
chmod +x setup.sh
./setup.sh
```

### 3. Настройка переменных окружения

```bash
# Редактирование .env файла
nano .env
```

**Обязательные переменные:**
```bash
# Supabase
SUPABASE_SERVICE_ROLE_KEY=your_actual_service_role_key

# Telegram Bot
TELEGRAM_BOT_TOKEN=your_actual_bot_token

# Traefik Dashboard
TRAEFIK_DASHBOARD_AUTH=admin:your_secure_password
```

### 4. SSL сертификаты (опционально)

Если у вас есть SSL сертификаты:

```bash
# Создание директории
mkdir -p traefik/ssl/gtm.baby-ssl-bundle

# Копирование сертификатов
cp your_certificate.crt traefik/ssl/gtm.baby-ssl-bundle/
cp your_private_key.key traefik/ssl/gtm.baby-ssl-bundle/

# Установка прав
chmod 600 traefik/ssl/gtm.baby-ssl-bundle/*
```

## 🚀 Запуск

### 1. Создание сети Docker

```bash
docker network create traefik
```

### 2. Запуск сервисов

```bash
# Запуск всех сервисов
docker-compose up -d

# Проверка статуса
docker-compose ps

# Просмотр логов
docker-compose logs -f
```

### 3. Проверка работоспособности

```bash
# Проверка API
curl -k https://api.gtm.baby/api/health

# Проверка Traefik Dashboard
curl -k https://traefik.gtm.baby

# Проверка SSL сертификатов
openssl s_client -connect api.gtm.baby:443 -servername api.gtm.baby
```

## 📊 Мониторинг

### Логи

```bash
# Логи всех сервисов
docker-compose logs -f

# Логи конкретного сервиса
docker-compose logs -f api
docker-compose logs -f bot
docker-compose logs -f traefik
```

### Статистика

```bash
# Использование ресурсов
docker stats

# Статус контейнеров
docker-compose ps

# Информация о сети
docker network inspect traefik
```

### Traefik Dashboard

- URL: `https://traefik.gtm.baby`
- Логин: `admin`
- Пароль: из переменной `TRAEFIK_DASHBOARD_AUTH`

## 🔧 Обслуживание

### Обновление

```bash
# Остановка сервисов
docker-compose down

# Обновление образов
docker-compose pull

# Перезапуск с новыми образами
docker-compose up -d
```

### Резервное копирование

```bash
# Резервное копирование volumes
docker run --rm -v gtm_traefik_acme:/data -v $(pwd):/backup alpine tar czf /backup/traefik_acme_backup.tar.gz -C /data .
docker run --rm -v gtm_redis_data:/data -v $(pwd):/backup alpine tar czf /backup/redis_data_backup.tar.gz -C /data .
```

### Восстановление

```bash
# Восстановление volumes
docker run --rm -v gtm_traefik_acme:/data -v $(pwd):/backup alpine tar xzf /backup/traefik_acme_backup.tar.gz -C /data
docker run --rm -v gtm_redis_data:/data -v $(pwd):/backup alpine tar xzf /backup/redis_data_backup.tar.gz -C /data
```

## 🚨 Устранение неполадок

### Проблемы с SSL

```bash
# Проверка сертификатов Let's Encrypt
docker-compose logs traefik | grep acme

# Принудительное обновление сертификатов
docker-compose restart traefik
```

### Проблемы с API

```bash
# Проверка логов API
docker-compose logs api

# Проверка переменных окружения
docker-compose exec api env | grep SUPABASE

# Тестирование подключения к Supabase
docker-compose exec api python -c "import requests; print(requests.get('https://api.gtm.baby/api/health').json())"
```

### Проблемы с ботом

```bash
# Проверка логов бота
docker-compose logs bot

# Проверка токена бота
docker-compose exec bot python -c "import os; print('Bot token:', os.getenv('TELEGRAM_BOT_TOKEN')[:10] + '...')"
```

### Проблемы с сетью

```bash
# Проверка сети
docker network ls
docker network inspect traefik

# Пересоздание сети
docker network rm traefik
docker network create traefik
docker-compose up -d
```

## 🔒 Безопасность

### Firewall

```bash
# Настройка UFW
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8080/tcp
sudo ufw enable
```

### Обновления безопасности

```bash
# Автоматические обновления
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

### Мониторинг безопасности

```bash
# Проверка уязвимостей
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image traefik:v2.10
```

## 📈 Масштабирование

### Горизонтальное масштабирование API

```bash
# Масштабирование API до 3 экземпляров
docker-compose up --scale api=3 -d
```

### Добавление Redis кластера

```bash
# В docker-compose.yml добавить:
redis-cluster:
  image: redis:7-alpine
  command: redis-cli --cluster create redis:6379 redis:6380 redis:6381 --cluster-replicas 1
```

### Мониторинг производительности

```bash
# Установка Prometheus и Grafana
# (отдельная конфигурация)
```

## 📝 Полезные команды

```bash
# Быстрый перезапуск
docker-compose restart

# Пересборка образов
docker-compose build --no-cache

# Очистка неиспользуемых ресурсов
docker system prune -a

# Просмотр использования диска
docker system df

# Экспорт логов
docker-compose logs > gtm_logs.txt
``` 