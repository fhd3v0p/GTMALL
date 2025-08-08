-- Создание упрощенной системы рейтингов для GTM

-- Создание таблицы оценок
CREATE TABLE IF NOT EXISTS artist_ratings (
  id BIGSERIAL PRIMARY KEY,
  artist_id BIGINT REFERENCES artists(id) ON DELETE CASCADE,
  user_id TEXT NOT NULL,
  rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
  comment TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  UNIQUE(artist_id, user_id)
);

-- Создание индексов
CREATE INDEX IF NOT EXISTS idx_artist_ratings_artist_id ON artist_ratings(artist_id);
CREATE INDEX IF NOT EXISTS idx_artist_ratings_user_id ON artist_ratings(user_id);

-- Добавление колонок для рейтинга в таблицу artists
ALTER TABLE artists ADD COLUMN IF NOT EXISTS average_rating DECIMAL(3,2) DEFAULT 0.0;
ALTER TABLE artists ADD COLUMN IF NOT EXISTS total_ratings INTEGER DEFAULT 0;