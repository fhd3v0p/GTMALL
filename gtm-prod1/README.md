# GTM Production Environment (gtm-prod1)

Полная производственная среда для GTM проекта с Docker, PostgreSQL, Redis и Flutter веб-приложением.

## Структура проекта

```
gtm-prod1/
├── api/                    # Flask API сервер
├── admin/                  # Django админ панель
├── bot/                    # Telegram бот
├── webapp/                 # Flutter веб-приложение (собирается автоматически)
├── docker-compose.yml      # Docker Compose конфигурация
├── nginx.conf             # Nginx конфигурация
├── deploy_with_ssl.sh     # Скрипт деплоя с SSL
├── deploy_to_server.sh    # Скрипт деплоя на сервер
└── build_flutter.sh       # Скрипт сборки Flutter приложения
```

## Быстрый старт

### 1. Локальная сборка Flutter приложения

```bash
# Сделать скрипт исполняемым
chmod +x build_flutter.sh

# Собрать Flutter приложение
./build_flutter.sh
```

### 2. Локальный запуск

```bash
# Запустить все сервисы
docker-compose up -d

# Проверить статус
docker-compose ps
```

### 3. Деплой на сервер

```bash
# Сделать скрипт исполняемым
chmod +x deploy_to_server.sh

# Деплой на сервер 31.56.39.165
./deploy_to_server.sh
```

### 4. Деплой с SSL

```bash
# Сделать скрипт исполняемым
chmod +x deploy_with_ssl.sh

# Деплой с SSL сертификатами
./deploy_with_ssl.sh
```

## Доступные URL

### Локально
- Веб-приложение: http://localhost
- API: http://localhost:3001
- Админка: http://localhost:8000
- API Health: http://localhost:3001/health

### На сервере
- Веб-приложение: http://31.56.39.165
- API: http://31.56.39.165:3001
- Админка: http://31.56.39.165:8000
- API Health: http://31.56.39.165:3001/health

### С SSL
- Веб-приложение: https://gtm.baby
- API: https://api.gtm.baby
- Админка: https://admin.gtm.baby

## Сервисы

### API (Flask)
- Порт: 3001
- База данных: PostgreSQL
- Кэш: Redis
- Файлы: /app/uploads

### Админка (Django)
- Порт: 8000
- База данных: PostgreSQL
- Статические файлы: /app/static
- Медиа файлы: /app/media

### Бот (Telegram)
- Подключение к API
- База данных: PostgreSQL
- Кэш: Redis

### Nginx
- Порт: 80, 443
- Проксирование запросов
- Статические файлы Flutter приложения

## База данных

### PostgreSQL
- База: gtm_db
- Пользователь: gtm_user
- Пароль: gtm_secure_password_2024
- Порт: 5432

### Redis
- Порт: 6379
- База: 0

## Переменные окружения

### API
```bash
DATABASE_URL=postgresql://gtm_user:gtm_secure_password_2024@postgres:5432/gtm_db
REDIS_URL=redis://redis:6379/0
DB_HOST=postgres
REDIS_HOST=redis
API_HOST=0.0.0.0
API_PORT=3001
DEBUG=False
ENVIRONMENT=production
```

### Бот
```bash
DATABASE_URL=postgresql://gtm_user:gtm_secure_password_2024@postgres:5432/gtm_db
REDIS_URL=redis://redis:6379/0
TELEGRAM_BOT_TOKEN=7533650686:AAEU4_nJZHGfzOv9XL4m_fDVt0q3dMDPQX8
```

### Админка
```bash
DATABASE_URL=postgresql://gtm_user:gtm_secure_password_2024@postgres:5432/gtm_db
DB_HOST=postgres
REDIS_HOST=redis
DEBUG=False
```

## Flutter приложение

### Отображение артистов
Приложение загружает артистов из папки `assets/artists/` и отображает их в:
- `master_cloud_screen.dart` - облако мастеров
- `master_detail_screen.dart` - детальная информация о мастере

### Структура папки артиста
```
assets/artists/[artist_name]/
├── avatar.png          # Аватар артиста
├── bio.txt            # Биография
├── links.json         # Социальные сети и ссылки
├── gallery1.jpg       # Галерея работ
├── gallery2.jpg
└── ...
```

### API подключение
Приложение подключается к API через `api_config.dart`:
- Тестовый сервер: http://31.56.39.165:3001/api
- Продакшн: https://api.gtm.baby/api

## Мониторинг

### Логи
```bash
# Просмотр логов API
docker-compose logs api

# Просмотр логов админки
docker-compose logs admin

# Просмотр логов бота
docker-compose logs bot

# Просмотр всех логов
docker-compose logs -f
```

### Здоровье сервисов
```bash
# Проверка API
curl http://localhost:3001/health

# Проверка админки
curl http://localhost:8000

# Проверка веб-приложения
curl http://localhost
```

## Устранение неполадок

### Проблемы с базой данных
```bash
# Проверка подключения к PostgreSQL
docker-compose exec postgres psql -U gtm_user -d gtm_db

# Проверка подключения к Redis
docker-compose exec redis redis-cli ping
```

### Проблемы с Flutter приложением
```bash
# Пересборка Flutter приложения
./build_flutter.sh

# Проверка файлов в webapp
ls -la webapp/
```

### Проблемы с SSL
```bash
# Проверка SSL сертификатов
openssl s_client -connect gtm.baby:443

# Проверка Traefik
docker-compose logs traefik
```

## Разработка

### Добавление нового артиста
1. Создать папку в `assets/artists/[artist_name]/`
2. Добавить файлы: `avatar.png`, `bio.txt`, `links.json`
3. Добавить галерею: `gallery1.jpg`, `gallery2.jpg`, ...
4. Обновить список артистов в `master_cloud_screen.dart`
5. Пересобрать Flutter приложение: `./build_flutter.sh`

### Обновление API
1. Внести изменения в `api/`
2. Пересобрать контейнер: `docker-compose build api`
3. Перезапустить: `docker-compose up -d api`

### Обновление админки
1. Внести изменения в `admin/`
2. Пересобрать контейнер: `docker-compose build admin`
3. Перезапустить: `docker-compose up -d admin`
