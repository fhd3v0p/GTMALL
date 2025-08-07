# 🚀 GTM Nginx Setup Guide

## 📋 Обзор

Этот гайд поможет настроить nginx на сервере для сайта gtm.baby с SSL сертификатами.

## 🏗️ Структура проекта

```
@GTMALL/
├── web/                    # Flutter web файлы
│   ├── index.html         # Главная страница
│   ├── admin_new.html     # Админ панель
│   ├── assets/            # Статические файлы
│   └── ...
├── nginx.conf             # Конфигурация nginx
├── docker-compose-simple.yml  # Docker Compose для nginx
├── gtm.baby-ssl-bundle/   # SSL сертификаты
│   ├── domain.cert.pem    # Сертификат
│   └── private.key.pem    # Приватный ключ
├── setup-ssl.sh           # Скрипт настройки SSL
└── deploy-nginx.sh        # Скрипт деплоя
```

## 🔧 Настройка

### 1. Подготовка файлов

Убедитесь что у вас есть:
- ✅ Flutter web файлы в директории `web/`
- ✅ SSL сертификаты в `gtm.baby-ssl-bundle/`

### 2. Настройка SSL

```bash
# Создание SSL сертификатов
chmod +x setup-ssl.sh
./setup-ssl.sh
```

### 3. Деплой nginx

```bash
# Запуск nginx с SSL
chmod +x deploy-nginx.sh
./deploy-nginx.sh
```

## 🌐 Доступные URL

После настройки будут доступны:

- **Основной сайт**: https://gtm.baby
- **API**: https://api.gtm.baby
- **Админ панель**: https://gtm.baby/admin/
- **Health check**: https://gtm.baby/health

## 🔒 SSL Сертификаты

### Варианты получения SSL:

1. **Let's Encrypt (бесплатно)**:
   ```bash
   sudo apt install certbot
   sudo certbot certonly --standalone -d gtm.baby -d www.gtm.baby
   ```

2. **Cloudflare SSL**:
   - Настройте DNS в Cloudflare
   - Включите SSL/TLS в режиме "Full"

3. **Самоподписанный (для тестирования)**:
   ```bash
   ./setup-ssl.sh
   ```

### Размещение сертификатов:

```
gtm.baby-ssl-bundle/
├── domain.cert.pem    # Сертификат
└── private.key.pem    # Приватный ключ
```

## 🐳 Docker контейнеры

### Запуск:
```bash
docker-compose -f docker-compose-simple.yml up -d
```

### Остановка:
```bash
docker-compose -f docker-compose-simple.yml down
```

### Логи:
```bash
# Nginx логи
docker-compose -f docker-compose-simple.yml logs nginx

# API логи
docker-compose -f docker-compose-simple.yml logs api
```

## 🔍 Проверка

### Проверка SSL:
```bash
openssl s_client -connect gtm.baby:443 -servername gtm.baby
```

### Проверка доступности:
```bash
curl -I https://gtm.baby
curl -I https://api.gtm.baby/health
```

### Проверка редиректа:
```bash
curl -I http://gtm.baby
# Должен вернуть 301 редирект на HTTPS
```

## 🛠️ Устранение проблем

### Проблема: SSL сертификат недействителен
```bash
./setup-ssl.sh
```

### Проблема: nginx не запускается
```bash
# Проверка конфигурации
docker run --rm -v "$(pwd)/nginx.conf:/etc/nginx/nginx.conf:ro" nginx:alpine nginx -t

# Проверка логов
docker-compose -f docker-compose-simple.yml logs nginx
```

### Проблема: файлы не загружаются
```bash
# Проверка прав доступа
ls -la web/
ls -la gtm.baby-ssl-bundle/

# Перезапуск контейнеров
docker-compose -f docker-compose-simple.yml restart
```

## 📊 Мониторинг

### Проверка статуса контейнеров:
```bash
docker-compose -f docker-compose-simple.yml ps
```

### Мониторинг ресурсов:
```bash
docker stats
```

## 🔄 Обновление

### Обновление web файлов:
1. Скопируйте новые файлы в `web/`
2. Перезапустите nginx:
   ```bash
   docker-compose -f docker-compose-simple.yml restart nginx
   ```

### Обновление SSL:
1. Замените файлы в `gtm.baby-ssl-bundle/`
2. Перезапустите nginx:
   ```bash
   docker-compose -f docker-compose-simple.yml restart nginx
   ```

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи: `docker-compose -f docker-compose-simple.yml logs`
2. Проверьте конфигурацию: `nginx -t`
3. Проверьте SSL: `openssl x509 -in gtm.baby-ssl-bundle/domain.cert.pem -text -noout` 