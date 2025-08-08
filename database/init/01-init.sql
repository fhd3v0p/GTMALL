-- ============================================================================
-- GTM Database Initialization Script
-- ============================================================================

-- Создание расширений
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Создание таблицы пользователей
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    telegram_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    phone_number VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Создание таблицы художников
CREATE TABLE IF NOT EXISTS artists (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    username VARCHAR(255) UNIQUE,
    bio TEXT,
    avatar_url TEXT,
    gallery_urls TEXT[],
    rating DECIMAL(3,2) DEFAULT 0.0,
    rating_count INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Создание таблицы отзывов
CREATE TABLE IF NOT EXISTS reviews (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    artist_id UUID REFERENCES artists(id) ON DELETE CASCADE,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, artist_id)
);

-- Создание таблицы сессий
CREATE TABLE IF NOT EXISTS sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    session_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE
);

-- Создание индексов для производительности
CREATE INDEX IF NOT EXISTS idx_users_telegram_id ON users(telegram_id);
CREATE INDEX IF NOT EXISTS idx_artists_username ON artists(username);
CREATE INDEX IF NOT EXISTS idx_artists_rating ON artists(rating DESC);
CREATE INDEX IF NOT EXISTS idx_reviews_artist_id ON reviews(artist_id);
CREATE INDEX IF NOT EXISTS idx_reviews_user_id ON reviews(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_expires_at ON sessions(expires_at);

-- Создание триггера для обновления updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Применение триггеров
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_artists_updated_at BEFORE UPDATE ON artists
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_reviews_updated_at BEFORE UPDATE ON reviews
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Функция для обновления рейтинга художника
CREATE OR REPLACE FUNCTION update_artist_rating()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN
        UPDATE artists 
        SET 
            rating = (
                SELECT COALESCE(AVG(rating), 0.0) 
                FROM reviews 
                WHERE artist_id = NEW.artist_id
            ),
            rating_count = (
                SELECT COUNT(*) 
                FROM reviews 
                WHERE artist_id = NEW.artist_id
            )
        WHERE id = NEW.artist_id;
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE artists 
        SET 
            rating = (
                SELECT COALESCE(AVG(rating), 0.0) 
                FROM reviews 
                WHERE artist_id = OLD.artist_id
            ),
            rating_count = (
                SELECT COUNT(*) 
                FROM reviews 
                WHERE artist_id = OLD.artist_id
            )
        WHERE id = OLD.artist_id;
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ language 'plpgsql';

-- Применение триггера для обновления рейтинга
CREATE TRIGGER update_artist_rating_trigger
    AFTER INSERT OR UPDATE OR DELETE ON reviews
    FOR EACH ROW EXECUTE FUNCTION update_artist_rating();

-- Вставка начальных данных художников
INSERT INTO artists (name, username, bio, rating, rating_count) VALUES
    ('GTM', 'gtm_tattoo', 'Основатель студии GTM', 4.8, 15),
    ('EMI', 'emi_tattoo', 'Мастер татуировки', 4.9, 23),
    ('Alena', 'alena_tattoo', 'Художник-татуировщик', 4.7, 18),
    ('Aspergill', 'aspergill_tattoo', 'Мастер художественной татуировки', 4.6, 12),
    ('Blodivamp', 'blodivamp_tattoo', 'Специалист по цветным тату', 4.5, 9),
    ('Chuchundra', 'chuchundra_tattoo', 'Мастер минималистичных тату', 4.4, 7),
    ('Klubnika', 'klubnika_tattoo', 'Художник-татуировщик', 4.3, 11),
    ('Lin++', 'lin_tattoo', 'Мастер современной татуировки', 4.2, 8),
    ('MurderDoll', 'murderdoll_tattoo', 'Специалист по черно-белым тату', 4.1, 6),
    ('Naidi', 'naidi_tattoo', 'Мастер художественной татуировки', 4.0, 5)
ON CONFLICT (username) DO NOTHING; 