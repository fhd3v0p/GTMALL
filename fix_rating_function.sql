-- Исправленная RPC функция без updated_at
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
    comment = comment_param;
  
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