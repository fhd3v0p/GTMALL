# 🔧 Настройка системы рейтингов GTM

## Шаг 1: Выполните SQL в Supabase Dashboard

1. Откройте [Supabase Dashboard](https://app.supabase.com)
2. Выберите проект `rxmtovqxjsvogyywyrha`
3. Перейдите в **SQL Editor**
4. Создайте новый запрос и вставьте следующий код:

```sql
-- Добавляем колонки для рейтинга в таблицу artists
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

-- Создаем индексы
CREATE INDEX IF NOT EXISTS idx_artist_ratings_artist_id ON artist_ratings(artist_id);
CREATE INDEX IF NOT EXISTS idx_artist_ratings_user_id ON artist_ratings(user_id);

-- Функция для добавления рейтинга
CREATE OR REPLACE FUNCTION add_artist_rating(
  artist_name_param TEXT,
  user_id_param TEXT,
  rating_param INTEGER,
  comment_param TEXT DEFAULT NULL
)
RETURNS JSON AS $$
DECLARE
  target_artist_id BIGINT;
  result JSON;
BEGIN
  -- Находим ID артиста по имени
  SELECT id INTO target_artist_id FROM artists WHERE name = artist_name_param;
  
  IF target_artist_id IS NULL THEN
    RETURN JSON_BUILD_OBJECT('success', false, 'error', 'Artist not found');
  END IF;
  
  -- Добавляем или обновляем рейтинг
  INSERT INTO artist_ratings (artist_id, user_id, rating, comment)
  VALUES (target_artist_id, user_id_param, rating_param, comment_param)
  ON CONFLICT (artist_id, user_id) 
  DO UPDATE SET 
    rating = rating_param,
    comment = comment_param,
    updated_at = now();
  
  -- Пересчитываем средний рейтинг
  UPDATE artists SET 
    average_rating = (
      SELECT COALESCE(AVG(rating), 0)::DECIMAL(3,2) 
      FROM artist_ratings 
      WHERE artist_id = target_artist_id
    ),
    total_ratings = (
      SELECT COUNT(*) 
      FROM artist_ratings 
      WHERE artist_id = target_artist_id
    )
  WHERE id = target_artist_id;
  
  RETURN JSON_BUILD_OBJECT('success', true, 'artist_id', target_artist_id);
END;
$$ LANGUAGE plpgsql;

-- Функция для получения рейтинга артиста
CREATE OR REPLACE FUNCTION get_artist_rating(artist_name_param TEXT)
RETURNS JSON AS $$
DECLARE
  result JSON;
BEGIN
  SELECT JSON_BUILD_OBJECT(
    'artist_name', name,
    'average_rating', COALESCE(average_rating, 0),
    'total_ratings', COALESCE(total_ratings, 0)
  ) INTO result
  FROM artists 
  WHERE name = artist_name_param;
  
  RETURN COALESCE(result, JSON_BUILD_OBJECT('error', 'Artist not found'));
END;
$$ LANGUAGE plpgsql;
```

5. Нажмите **Run** для выполнения SQL

## Шаг 2: Проверка установки

После выполнения SQL, запустите эту команду для проверки:

```bash
python3 -c "
import urllib.request
import json

SUPABASE_URL = 'https://rxmtovqxjsvogyywyrha.supabase.co'
SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1Mjg1NTAsImV4cCI6MjA3MDEwNDU1MH0.gDkJybktFoi486hbIVwppDfmVQlAR0fM4o4Sl1-AxhE'

req = urllib.request.Request(
    f'{SUPABASE_URL}/rest/v1/artists?select=*&limit=1',
    headers={'apikey': SUPABASE_ANON_KEY, 'Authorization': f'Bearer {SUPABASE_ANON_KEY}'}
)

with urllib.request.urlopen(req) as response:
    data = json.loads(response.read())
    if data:
        columns = list(data[0].keys())
        print('Колонки в таблице artists:', columns)
        print('✅ average_rating есть:', 'average_rating' in columns)
        print('✅ total_ratings есть:', 'total_ratings' in columns)
"
```

## Шаг 3: Тестирование функции

```bash
curl -X POST \
  -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1Mjg1NTAsImV4cCI6MjA3MDEwNDU1MH0.gDkJybktFoi486hbIVwppDfmVQlAR0fM4o4Sl1-AxhE" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1Mjg1NTAsImV4cCI6MjA3MDEwNDU1MH0.gDkJybktFoi486hbIVwppDfmVQlAR0fM4o4Sl1-AxhE" \
  -H "Content-Type: application/json" \
  -d '{
    "artist_name_param": "Lin++",
    "user_id_param": "test_user_123",
    "rating_param": 5,
    "comment_param": "Отличная работа!"
  }' \
  "https://rxmtovqxjsvogyywyrha.supabase.co/rest/v1/rpc/add_artist_rating"
```

## Что дальше?

После успешной установки мы:
1. Обновим bot_main.py с командами рейтинга
2. Исправим Flutter для чтения рейтингов (без записи)

**Выполните Шаг 1 в Supabase Dashboard, затем сообщите о результате!**