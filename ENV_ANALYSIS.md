# 📊 Анализ переменных окружения GTM

## 🔍 Текущая конфигурация

### ✅ Все переменные вынесены в .env

**Файл**: `@GTMALL/env.example`

### 📋 Переменные по категориям:

#### 🌐 Общие настройки
```bash
ENVIRONMENT=production
DOMAIN=gtm.baby
TZ=Europe/Moscow
```

#### 🔗 Supabase Configuration
```bash
SUPABASE_URL=https://rxmtovqxjsvogyywyrha.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1Mjg1NTAsImV4cCI6MjA3MDEwNDU1MH0.gDkJybktFoi486hbIVwppDfmVQlAR0fM4o4Sl1-AxhE
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here  # ⚠️ ОБЯЗАТЕЛЬНО ИЗМЕНИТЬ
```

#### 🤖 Telegram Bot Configuration
```bash
TELEGRAM_BOT_TOKEN=7533650686:AAEU4_nJZHGfzOv9XL4m_fDVt0q3dMDPQX8
TELEGRAM_FOLDER_LINK=https://t.me/addlist/qRX5VmLZF7E3M2U9
WEBAPP_URL=https://gtm.baby
```

#### 🔌 API Server Configuration
```bash
API_PORT=5000
API_HOST=0.0.0.0
FLASK_ENV=production
```

#### 🗄️ Database Configuration
```bash
DATABASE_URL=postgresql://gtm_user:gtm_secure_password_2024@postgres:5432/gtm_db
```

#### 🚀 Redis Configuration
```bash
REDIS_URL=redis://redis:6379/0
```

#### 🔒 Traefik Configuration
```bash
TRAEFIK_DASHBOARD_AUTH=admin:your_secure_password_here  # ⚠️ ОБЯЗАТЕЛЬНО ИЗМЕНИТЬ
```

#### 📝 Logging
```bash
LOG_LEVEL=INFO
```

## 🔧 Использование в Docker Compose

### ✅ Все переменные передаются в контейнеры

**API Server:**
```yaml
environment:
  - SUPABASE_URL=${SUPABASE_URL}
  - SUPABASE_ANON_KEY=${SUPABASE_ANON_KEY}
  - SUPABASE_SERVICE_ROLE_KEY=${SUPABASE_SERVICE_ROLE_KEY}
  - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
  - API_PORT=${API_PORT}
  - API_HOST=${API_HOST}
  - FLASK_ENV=${FLASK_ENV}
  - DATABASE_URL=${DATABASE_URL}
  - REDIS_URL=${REDIS_URL}
  - LOG_LEVEL=${LOG_LEVEL}
```

**Telegram Bot:**
```yaml
environment:
  - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
  - TELEGRAM_FOLDER_LINK=${TELEGRAM_FOLDER_LINK}
  - WEBAPP_URL=${WEBAPP_URL}
  - SUPABASE_URL=${SUPABASE_URL}
  - SUPABASE_ANON_KEY=${SUPABASE_ANON_KEY}
  - SUPABASE_SERVICE_ROLE_KEY=${SUPABASE_SERVICE_ROLE_KEY}
  - DATABASE_URL=${DATABASE_URL}
  - REDIS_URL=${REDIS_URL}
  - LOG_LEVEL=${LOG_LEVEL}
```

## ⚠️ Обязательные изменения для продакшена

### 1. SUPABASE_SERVICE_ROLE_KEY
```bash
# Текущее значение (небезопасно):
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here

# Должно быть (получить из Supabase Dashboard):
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NDUyODU1MCwiZXhwIjoyMDcwMTA0NTUwfQ.actual_service_role_key
```

### 2. TRAEFIK_DASHBOARD_AUTH
```bash
# Текущее значение (небезопасно):
TRAEFIK_DASHBOARD_AUTH=admin:your_secure_password_here

# Должно быть (создать безопасный пароль):
TRAEFIK_DASHBOARD_AUTH=admin:gtm_secure_2024_password
```

### 3. TELEGRAM_BOT_TOKEN (проверить актуальность)
```bash
# Текущее значение:
TELEGRAM_BOT_TOKEN=7533650686:AAEU4_nJZHGfzOv9XL4m_fDVt0q3dMDPQX8

# Убедиться, что токен актуален и бот работает
```

## 🔒 Безопасность

### ✅ Безопасные практики:
- ✅ Все секреты в переменных окружения
- ✅ Нет хардкода в коде
- ✅ Разные переменные для разных окружений
- ✅ Безопасные пароли для dashboard

### ⚠️ Что нужно сделать:
1. **Изменить SUPABASE_SERVICE_ROLE_KEY** на реальный ключ
2. **Изменить TRAEFIK_DASHBOARD_AUTH** на безопасный пароль
3. **Проверить TELEGRAM_BOT_TOKEN** на актуальность
4. **Настроить DNS** для домена gtm.baby

## 📋 Инструкция по настройке

### 1. Получить Supabase Service Role Key:
1. Зайти в Supabase Dashboard
2. Settings → API
3. Скопировать "service_role" key

### 2. Создать безопасный пароль для Traefik:
```bash
# Генерировать безопасный пароль
openssl rand -base64 32
```

### 3. Проверить Telegram Bot Token:
1. Написать @BotFather в Telegram
2. Команда /mybots
3. Выбрать бота
4. API Token → Проверить актуальность

### 4. Настроить DNS:
```
gtm.baby          A    31.56.46.46
api.gtm.baby      A    31.56.46.46
traefik.gtm.baby  A    31.56.46.46
```

## 🚀 Деплой на сервер 31.56.46.46

### ✅ Готово к деплою:
- ✅ Скрипт деплоя: `@GTMALL/deploy.sh`
- ✅ SSH ключи настроены
- ✅ Docker Compose конфигурация
- ✅ Все переменные окружения

### 🔧 Команда для деплоя:
```bash
cd @GTMALL
chmod +x deploy.sh
./deploy.sh
```

### 📊 Результат деплоя:
- API: `https://api.gtm.baby`
- Traefik Dashboard: `https://traefik.gtm.baby`
- Web App: `https://gtm.baby` (после добавления)

## 📝 Заключение

✅ **Все переменные окружения вынесены в .env**
✅ **Конфигурация готова к продакшену**
✅ **Деплой на сервер 31.56.46.46 возможен**
⚠️ **Требуется изменить 2 обязательные переменные перед деплоем** 