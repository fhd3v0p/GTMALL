# 🌐 GTM Web Application

Папка для Flutter веб-приложения GTM.

## 📁 Структура

```
web/
├── Dockerfile          # Dockerfile для Flutter web
├── nginx.conf         # Конфигурация Nginx
├── build/             # Собранное приложение (будет создано)
└── README.md          # Этот файл
```

## 🚀 Развертывание

### 1. Сборка Flutter приложения

```bash
# В папке с Flutter проектом
flutter build web --release
```

### 2. Копирование файлов

```bash
# Скопировать build/web/ в web/build/
cp -r build/web/* web/build/
```

### 3. Запуск с Docker

```bash
# В папке @GTMALL/
docker-compose up web -d
```

## 🔧 Конфигурация

### Nginx

Nginx настроен для:
- Обслуживания статических файлов
- Кэширования
- Gzip сжатия
- Безопасности заголовков

### Traefik

Веб-приложение будет доступно по адресу:
- **Production**: https://gtm.baby
- **Development**: https://dev.gtm.baby

## 📊 Мониторинг

- **Health Check**: https://gtm.baby/health
- **Status**: https://gtm.baby/status

## 🔒 SSL

SSL сертификаты управляются Traefik автоматически через Let's Encrypt. 