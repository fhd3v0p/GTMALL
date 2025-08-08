# ✅ Система рейтингов GTM - Готова к внедрению

## 🏗️ Архитектура системы

```
Пользователь → Telegram Bot → Supabase → Flutter (читает)
              ↓
         /rate Lin++ 5
         /rating Lin++
         /artists
```

## 📋 Что уже сделано:

### ✅ 1. Flutter обновлен
- **Файл**: `lib/screens/master_detail_screen.dart`
- **Изменения**:
  - Flutter теперь **только читает** рейтинги из Supabase
  - При попытке поставить оценку показывается инструкция для бота
  - Отображение обновлено для новых полей: `average_rating`, `total_ratings`
  - Добавлена кнопка "Оценить" с объяснением

### ✅ 2. Подготовлены команды для бота
- **Файл**: `gtm-prod1/bot/ratings_bot_extension.py`
- **Команды**:
  - `/rate <артист> <1-5> [комментарий]` - оценить артиста
  - `/rating <артист>` - посмотреть рейтинг
  - `/artists` - список всех артистов

### ✅ 3. SQL схема готова
- **Файл**: `add_rating_columns.sql`
- **Создает**:
  - Таблицу `artist_ratings` для хранения оценок
  - Колонки `average_rating`, `total_ratings` в таблице `artists`
  - RPC функции `add_artist_rating` и `get_artist_rating`

## 🚀 Следующие шаги:

### Шаг 1: Выполните SQL в Supabase
1. Откройте [Supabase Dashboard](https://app.supabase.com) → Проект `rxmtovqxjsvogyywyrha` → SQL Editor
2. Скопируйте и выполните код из файла `add_rating_columns.sql`

### Шаг 2: Проверьте установку
```bash
python3 -c "
import urllib.request, json
req = urllib.request.Request(
    'https://rxmtovqxjsvogyywyrha.supabase.co/rest/v1/artists?select=*&limit=1',
    headers={'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1Mjg1NTAsImV4cCI6MjA3MDEwNDU1MH0.gDkJybktFoi486hbIVwppDfmVQlAR0fM4o4Sl1-AxhE'}
)
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read())
    columns = list(data[0].keys())
    print('✅ average_rating есть:', 'average_rating' in columns)
    print('✅ total_ratings есть:', 'total_ratings' in columns)
"
```

### Шаг 3: Тестируйте API функции
```bash
curl -X POST \
  -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1Mjg1NTAsImV4cCI6MjA3MDEwNDU1MH0.gDkJybktFoi486hbIVwppDfmVQlAR0fM4o4Sl1-AxhE" \
  -H "Content-Type: application/json" \
  -d '{"artist_name_param": "Lin++", "user_id_param": "test_123", "rating_param": 5}' \
  "https://rxmtovqxjsvogyywyrha.supabase.co/rest/v1/rpc/add_artist_rating"
```

### Шаг 4: Интегрируйте команды в bot_main.py
Добавьте в метод `setup_handlers()`:
```python
self.application.add_handler(CommandHandler("rate", self.rate_command))
self.application.add_handler(CommandHandler("rating", self.rating_command))  
self.application.add_handler(CommandHandler("artists", self.artists_command))
```

И методы в класс `GTMBot` (код готов в `ratings_bot_extension.py`)

## 🎯 Преимущества новой системы:

1. **Безопасность** - рейтинги только через Telegram бота
2. **Честность** - один пользователь = одна оценка на артиста
3. **Централизованность** - вся логика в одном месте
4. **Масштабируемость** - простое добавление новых функций
5. **Прозрачность** - все оценки логируются

## 📱 Пользовательский опыт:

1. **В Flutter**: Пользователь видит рейтинг, жмет "Оценить"
2. **Показывается**: Инструкция с командой для бота
3. **В боте**: Пользователь использует `/rate Lin++ 5 отличная работа!`
4. **В Flutter**: Рейтинг обновляется автоматически при следующем просмотре

**Готово к внедрению! Выполните SQL в Supabase и сообщите о результате.**