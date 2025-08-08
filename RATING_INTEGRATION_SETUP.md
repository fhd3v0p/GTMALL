# 🔥 Интеграция рейтингов: Flutter → Bot API → Supabase

## ✅ Что готово:

### 📱 **Flutter:**
- ⭐ Интерактивные звездочки для оценки
- 📡 Отправка рейтингов через HTTP API
- 🔄 Автоматическое обновление статистики
- 💫 Красивая анимация загрузки

### 🤖 **Bot API:**
- 🚀 Flask API сервер (`rating_api.py`)
- 📝 Эндпоинт `/api/rate-artist` для приема рейтингов
- 📊 Интеграция с Supabase RPC функциями
- 🔒 Валидация данных

## 🚀 Запуск системы:

### Шаг 1: Настройте Supabase
Выполните SQL из файла `add_rating_columns.sql` в Supabase Dashboard:

```sql
-- Добавляем колонки для рейтинга
ALTER TABLE artists ADD COLUMN IF NOT EXISTS average_rating DECIMAL(3,2) DEFAULT 0.0;
ALTER TABLE artists ADD COLUMN IF NOT EXISTS total_ratings INTEGER DEFAULT 0;

-- Создаем таблицу рейтингов
CREATE TABLE IF NOT EXISTS artist_ratings (
  id BIGSERIAL PRIMARY KEY,
  artist_id BIGINT REFERENCES artists(id) ON DELETE CASCADE,
  user_id TEXT NOT NULL,
  rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
  comment TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  UNIQUE(artist_id, user_id)
);

-- ... (остальной код из файла)
```

### Шаг 2: Запустите Rating API
```bash
cd gtm-prod1/bot

# Установите зависимости (в виртуальном окружении)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements_rating_api.txt

# Запустите API сервер
python3 rating_api.py
```

### Шаг 3: Запустите Flutter приложение
```bash
# В корне проекта
flutter run -d chrome --web-port=8080
```

## 🔄 Архитектура работы:

```
👤 Пользователь нажимает звездочку в Flutter
    ↓
📱 Flutter: POST /api/rate-artist
    ↓  
🤖 Rating API: получает запрос
    ↓
📝 API: вызывает RPC add_artist_rating в Supabase
    ↓
💾 Supabase: сохраняет рейтинг и пересчитывает средний
    ↓
📊 API: возвращает обновленную статистику
    ↓
📱 Flutter: обновляет UI с новым рейтингом
```

## 🔧 Конфигурация:

### Для разработки:
- Rating API: `http://localhost:5000`
- Flutter: `http://localhost:8080`

### Для продакшена:
Обновите `lib/config/api_config.dart`:
```dart
static const String ratingApiBaseUrl = 'https://your-api-domain.com';
```

## 🧪 Тестирование:

### 1. Проверьте API:
```bash
curl -X GET http://localhost:5000/api/health
```

### 2. Тестовый рейтинг:
```bash
curl -X POST http://localhost:5000/api/rate-artist \
  -H "Content-Type: application/json" \
  -d '{
    "artist_name": "EMI",
    "user_id": "test_user_123",
    "rating": 5,
    "comment": "Отличная работа!"
  }'
```

### 3. Проверьте в Flutter:
1. Откройте приложение
2. Перейдите к любому артисту  
3. Нажмите на звездочку
4. Должно появиться "✅ Спасибо за вашу оценку!"

## 🎯 Преимущества новой системы:

1. **🎨 Красивый UX** - пользователь оценивает прямо в приложении
2. **🔒 Безопасность** - все проверки на стороне API
3. **⚡ Быстрота** - мгновенная обратная связь
4. **📊 Точность** - один пользователь = одна оценка
5. **🔄 Синхронизация** - данные всегда актуальны

**Система готова к работе! Запустите и протестируйте.**