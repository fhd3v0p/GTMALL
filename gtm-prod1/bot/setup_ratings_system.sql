-- Создание системы рейтингов для артистов
-- Этот скрипт должен быть выполнен в Supabase SQL Editor

-- Создание таблицы оценок
CREATE TABLE IF NOT EXISTS artist_ratings (
  id BIGSERIAL PRIMARY KEY,
  artist_id BIGINT REFERENCES artists(id) ON DELETE CASCADE,
  user_id TEXT NOT NULL, -- Telegram user ID
  rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
  comment TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  UNIQUE(artist_id, user_id) -- Один пользователь может оставить только одну оценку артисту
);

-- Создание индексов для быстрого поиска
CREATE INDEX IF NOT EXISTS idx_artist_ratings_artist_id ON artist_ratings(artist_id);
CREATE INDEX IF NOT EXISTS idx_artist_ratings_user_id ON artist_ratings(user_id);
CREATE INDEX IF NOT EXISTS idx_artist_ratings_created_at ON artist_ratings(created_at);

-- Добавление колонки для среднего рейтинга в таблицу artists
ALTER TABLE artists ADD COLUMN IF NOT EXISTS average_rating DECIMAL(3,2) DEFAULT 0.0;
ALTER TABLE artists ADD COLUMN IF NOT EXISTS total_ratings INTEGER DEFAULT 0;

-- Функция для пересчета среднего рейтинга
CREATE OR REPLACE FUNCTION update_artist_average_rating(artist_id_param BIGINT)
RETURNS VOID AS $$
DECLARE
  avg_rating DECIMAL(3,2);
  total_count INTEGER;
BEGIN
  -- Вычисляем средний рейтинг и количество оценок
  SELECT 
    COALESCE(AVG(rating), 0)::DECIMAL(3,2),
    COALESCE(COUNT(*), 0)
  INTO avg_rating, total_count
  FROM artist_ratings 
  WHERE artist_id = artist_id_param;
  
  -- Обновляем данные в таблице artists
  UPDATE artists 
  SET 
    average_rating = avg_rating,
    total_ratings = total_count,
    updated_at = now()
  WHERE id = artist_id_param;
  
  RAISE NOTICE 'Updated artist % rating: % (% total)', artist_id_param, avg_rating, total_count;
END;
$$ LANGUAGE plpgsql;

-- Триггер для автоматического пересчета рейтинга при добавлении/изменении/удалении оценки
CREATE OR REPLACE FUNCTION trigger_update_artist_rating()
RETURNS TRIGGER AS $$
BEGIN
  IF TG_OP = 'DELETE' THEN
    PERFORM update_artist_average_rating(OLD.artist_id);
    RETURN OLD;
  ELSE
    PERFORM update_artist_average_rating(NEW.artist_id);
    RETURN NEW;
  END IF;
END;
$$ LANGUAGE plpgsql;

-- Создание триггеров
DROP TRIGGER IF EXISTS tr_artist_ratings_update ON artist_ratings;
CREATE TRIGGER tr_artist_ratings_update
  AFTER INSERT OR UPDATE OR DELETE ON artist_ratings
  FOR EACH ROW EXECUTE FUNCTION trigger_update_artist_rating();

-- RPC функция для добавления/обновления оценки
CREATE OR REPLACE FUNCTION add_or_update_rating(
  artist_id_param BIGINT,
  user_id_param TEXT,
  rating_param INTEGER,
  comment_param TEXT DEFAULT NULL
)
RETURNS JSON AS $$
DECLARE
  result JSON;
  existing_rating RECORD;
BEGIN
  -- Проверяем валидность рейтинга
  IF rating_param < 1 OR rating_param > 5 THEN
    RETURN JSON_BUILD_OBJECT(
      'success', false,
      'error', 'Rating must be between 1 and 5'
    );
  END IF;
  
  -- Проверяем существование артиста
  IF NOT EXISTS (SELECT 1 FROM artists WHERE id = artist_id_param) THEN
    RETURN JSON_BUILD_OBJECT(
      'success', false,
      'error', 'Artist not found'
    );
  END IF;
  
  -- Проверяем существующую оценку
  SELECT * INTO existing_rating
  FROM artist_ratings 
  WHERE artist_id = artist_id_param AND user_id = user_id_param;
  
  IF existing_rating.id IS NOT NULL THEN
    -- Обновляем существующую оценку
    UPDATE artist_ratings 
    SET 
      rating = rating_param,
      comment = comment_param,
      updated_at = now()
    WHERE id = existing_rating.id;
    
    result := JSON_BUILD_OBJECT(
      'success', true,
      'action', 'updated',
      'rating_id', existing_rating.id,
      'previous_rating', existing_rating.rating,
      'new_rating', rating_param
    );
  ELSE
    -- Создаем новую оценку
    INSERT INTO artist_ratings (artist_id, user_id, rating, comment)
    VALUES (artist_id_param, user_id_param, rating_param, comment_param)
    RETURNING id INTO existing_rating;
    
    result := JSON_BUILD_OBJECT(
      'success', true,
      'action', 'created',
      'rating_id', existing_rating.id,
      'rating', rating_param
    );
  END IF;
  
  RETURN result;
END;
$$ LANGUAGE plpgsql;

-- RPC функция для получения рейтингов артиста
CREATE OR REPLACE FUNCTION get_artist_ratings(artist_id_param BIGINT)
RETURNS JSON AS $$
DECLARE
  result JSON;
  avg_rating DECIMAL(3,2);
  total_count INTEGER;
  ratings_data JSON;
BEGIN
  -- Получаем средний рейтинг и количество
  SELECT average_rating, total_ratings 
  INTO avg_rating, total_count
  FROM artists 
  WHERE id = artist_id_param;
  
  -- Получаем последние 10 оценок с комментариями
  SELECT JSON_AGG(
    JSON_BUILD_OBJECT(
      'rating', rating,
      'comment', comment,
      'created_at', created_at
    ) ORDER BY created_at DESC
  ) INTO ratings_data
  FROM (
    SELECT rating, comment, created_at
    FROM artist_ratings
    WHERE artist_id = artist_id_param
    ORDER BY created_at DESC
    LIMIT 10
  ) latest_ratings;
  
  result := JSON_BUILD_OBJECT(
    'artist_id', artist_id_param,
    'average_rating', COALESCE(avg_rating, 0),
    'total_ratings', COALESCE(total_count, 0),
    'recent_ratings', COALESCE(ratings_data, '[]'::JSON)
  );
  
  RETURN result;
END;
$$ LANGUAGE plpgsql;

-- Настройка RLS (Row Level Security)
ALTER TABLE artist_ratings ENABLE ROW LEVEL SECURITY;

-- Политика для чтения (все могут читать)
CREATE POLICY "Allow read access to artist_ratings" ON artist_ratings
  FOR SELECT USING (true);

-- Политика для записи (все могут добавлять/обновлять свои оценки)
CREATE POLICY "Allow insert/update own ratings" ON artist_ratings
  FOR ALL USING (true);

-- Первоначальный пересчет рейтингов для всех существующих артистов
DO $$
DECLARE
  artist_record RECORD;
BEGIN
  FOR artist_record IN SELECT id FROM artists LOOP
    PERFORM update_artist_average_rating(artist_record.id);
  END LOOP;
END $$;