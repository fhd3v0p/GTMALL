-- GTM Supabase Extended Schema
-- Расширенная схема с поддержкой билетов и проверки подписок

-- Таблица городов
CREATE TABLE IF NOT EXISTS cities (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    code VARCHAR(10),
    population INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Таблица категорий
CREATE TABLE IF NOT EXISTS categories (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    type VARCHAR(50),
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Таблица связи артистов с городами
CREATE TABLE IF NOT EXISTS artist_cities (
    id BIGSERIAL PRIMARY KEY,
    artist_id BIGINT NOT NULL,
    city_id BIGINT NOT NULL REFERENCES cities(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(artist_id, city_id)
);

-- Таблица связи артистов с категориями
CREATE TABLE IF NOT EXISTS artist_categories (
    id BIGSERIAL PRIMARY KEY,
    artist_id BIGINT NOT NULL,
    category_id BIGINT NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(artist_id, category_id)
);

-- Обновляем таблицу пользователей с полями для билетов
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS subscription_tickets INTEGER DEFAULT 0 CHECK (subscription_tickets <= 1),
ADD COLUMN IF NOT EXISTS referral_tickets INTEGER DEFAULT 0 CHECK (referral_tickets <= 10),
ADD COLUMN IF NOT EXISTS total_tickets INTEGER DEFAULT 0;

-- Индексы для оптимизации
CREATE INDEX IF NOT EXISTS idx_artist_cities_artist_id ON artist_cities(artist_id);
CREATE INDEX IF NOT EXISTS idx_artist_cities_city_id ON artist_cities(city_id);
CREATE INDEX IF NOT EXISTS idx_artist_categories_artist_id ON artist_categories(artist_id);
CREATE INDEX IF NOT EXISTS idx_artist_categories_category_id ON artist_categories(category_id);
CREATE INDEX IF NOT EXISTS idx_cities_active ON cities(is_active);
CREATE INDEX IF NOT EXISTS idx_categories_active ON categories(is_active);
CREATE INDEX IF NOT EXISTS idx_users_subscription_tickets ON users(subscription_tickets);
CREATE INDEX IF NOT EXISTS idx_users_referral_tickets ON users(referral_tickets);
CREATE INDEX IF NOT EXISTS idx_users_total_tickets ON users(total_tickets);

-- RLS политики
ALTER TABLE cities ENABLE ROW LEVEL SECURITY;
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE artist_cities ENABLE ROW LEVEL SECURITY;
ALTER TABLE artist_categories ENABLE ROW LEVEL SECURITY;

-- Публичное чтение городов
CREATE POLICY "Публичное чтение городов" ON cities FOR SELECT USING (is_active = true);

-- Публичное чтение категорий
CREATE POLICY "Публичное чтение категорий" ON categories FOR SELECT USING (is_active = true);

-- Публичное чтение связей артистов
CREATE POLICY "Публичное чтение связей артистов" ON artist_cities FOR SELECT USING (true);
CREATE POLICY "Публичное чтение связей артистов" ON artist_categories FOR SELECT USING (true);

-- Полный доступ для service role
CREATE POLICY "Service role full access" ON cities FOR ALL USING (true);
CREATE POLICY "Service role full access" ON categories FOR ALL USING (true);
CREATE POLICY "Service role full access" ON artist_cities FOR ALL USING (true);
CREATE POLICY "Service role full access" ON artist_categories FOR ALL USING (true);

-- Функция для получения отфильтрованных артистов
CREATE OR REPLACE FUNCTION get_artists_filtered(
    p_city VARCHAR DEFAULT NULL,
    p_category VARCHAR DEFAULT NULL,
    p_limit INTEGER DEFAULT 50,
    p_offset INTEGER DEFAULT 0
) RETURNS TABLE (
    id BIGINT,
    name VARCHAR,
    avatar_url VARCHAR,
    city VARCHAR,
    category VARCHAR,
    bio TEXT,
    telegram VARCHAR,
    tiktok VARCHAR,
    pinterest VARCHAR,
    pinterest_url VARCHAR,
    telegram_url VARCHAR,
    tiktok_url VARCHAR,
    booking_url VARCHAR,
    location_html TEXT,
    gallery_html TEXT,
    subscription_channels TEXT[]
) AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        a.id,
        a.name,
        a.avatar_url,
        c.name as city,
        cat.name as category,
        a.bio,
        a.telegram,
        a.tiktok,
        a.pinterest,
        a.pinterest_url,
        a.telegram_url,
        a.tiktok_url,
        a.booking_url,
        a.location_html,
        a.gallery_html,
        a.subscription_channels
    FROM artists a
    LEFT JOIN artist_cities ac ON a.id = ac.artist_id
    LEFT JOIN cities c ON ac.city_id = c.id
    LEFT JOIN artist_categories acc ON a.id = acc.artist_id
    LEFT JOIN categories cat ON acc.category_id = cat.id
    WHERE a.is_active = true
    AND (p_city IS NULL OR c.name = p_city)
    AND (p_category IS NULL OR cat.name = p_category)
    ORDER BY a.name
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

-- Функция для обновления общего количества билетов пользователя
CREATE OR REPLACE FUNCTION update_user_total_tickets()
RETURNS TRIGGER AS $$
BEGIN
    NEW.total_tickets = COALESCE(NEW.subscription_tickets, 0) + COALESCE(NEW.referral_tickets, 0);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггер для автоматического обновления total_tickets
CREATE TRIGGER update_user_total_tickets_trigger
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_user_total_tickets();

-- Функция для проверки подписки и начисления билета
CREATE OR REPLACE FUNCTION check_subscription_and_award_ticket(
    p_telegram_id BIGINT,
    p_is_subscribed BOOLEAN
) RETURNS JSON AS $$
DECLARE
    user_record RECORD;
    result JSON;
BEGIN
    -- Получаем информацию о пользователе
    SELECT * INTO user_record FROM users WHERE telegram_id = p_telegram_id;
    
    IF user_record IS NULL THEN
        RETURN json_build_object(
            'success', false,
            'message', 'Пользователь не найден',
            'subscription_tickets', 0,
            'referral_tickets', 0,
            'total_tickets', 0
        );
    END IF;
    
    -- Если подписан и билет еще не начислен
    IF p_is_subscribed AND user_record.subscription_tickets = 0 THEN
        UPDATE users 
        SET subscription_tickets = 1,
            total_tickets = total_tickets + 1
        WHERE telegram_id = p_telegram_id;
        
        RETURN json_build_object(
            'success', true,
            'message', 'Билет начислен за подписку на папку',
            'subscription_tickets', 1,
            'referral_tickets', user_record.referral_tickets,
            'total_tickets', user_record.total_tickets + 1,
            'ticket_awarded', true
        );
    ELSE
        RETURN json_build_object(
            'success', true,
            'message', CASE 
                WHEN NOT p_is_subscribed THEN 'Не подписан на папку'
                ELSE 'Билет уже начислен за подписку'
            END,
            'subscription_tickets', user_record.subscription_tickets,
            'referral_tickets', user_record.referral_tickets,
            'total_tickets', user_record.total_tickets,
            'ticket_awarded', false
        );
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Функция для получения статистики билетов
CREATE OR REPLACE FUNCTION get_tickets_stats() RETURNS JSON AS $$
DECLARE
    total_subscription_tickets INTEGER;
    total_referral_tickets INTEGER;
    total_user_tickets INTEGER;
BEGIN
    SELECT 
        COALESCE(SUM(subscription_tickets), 0),
        COALESCE(SUM(referral_tickets), 0),
        COALESCE(SUM(total_tickets), 0)
    INTO total_subscription_tickets, total_referral_tickets, total_user_tickets
    FROM users;
    
    RETURN json_build_object(
        'total_subscription_tickets', total_subscription_tickets,
        'total_referral_tickets', total_referral_tickets,
        'total_user_tickets', total_user_tickets
    );
END;
$$ LANGUAGE plpgsql;

-- Вставляем базовые данные
INSERT INTO cities (name, code, population) VALUES 
    ('Москва', 'МСК', 13200000),
    ('Санкт-Петербург', 'СПБ', 5600000),
    ('Новосибирск', 'НСК', 1700000),
    ('Екатеринбург', 'ЕКБ', 1600000),
    ('Казань', 'КАЗ', 1400000)
ON CONFLICT (name) DO NOTHING;

INSERT INTO categories (name, type, description) VALUES 
    ('Татуировки', 'tattoo', 'Художественные татуировки'),
    ('Пирсинг', 'piercing', 'Пирсинг различных частей тела'),
    ('Перманентный макияж', 'pmu', 'Перманентный макияж'),
    ('Косметология', 'cosmetology', 'Косметологические услуги')
ON CONFLICT (name) DO NOTHING; 