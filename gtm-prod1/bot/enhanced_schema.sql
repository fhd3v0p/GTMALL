-- GTM Enhanced Supabase Database Schema
-- Расширенная схема базы данных для системы GTM

-- Таблица городов
CREATE TABLE IF NOT EXISTS cities (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    code VARCHAR(10) UNIQUE NOT NULL,
    population INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    display_order INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Таблица категорий
CREATE TABLE IF NOT EXISTS categories (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    type VARCHAR(20) NOT NULL DEFAULT 'service', -- 'service' или 'product'
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    display_order INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Обновленная таблица артистов с внешними ключами
DROP TABLE IF EXISTS artists CASCADE;
CREATE TABLE artists (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    username VARCHAR(100),
    bio TEXT,
    avatar_url VARCHAR(500),
    city_id BIGINT REFERENCES cities(id),
    category_id BIGINT REFERENCES categories(id),
    specialties TEXT[],
    rating DECIMAL(3,2) DEFAULT 0.0,
    telegram VARCHAR(100),
    instagram VARCHAR(100),
    tiktok VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Обновленная таблица галереи артистов
DROP TABLE IF EXISTS artist_gallery CASCADE;
CREATE TABLE artist_gallery (
    id BIGSERIAL PRIMARY KEY,
    artist_id BIGINT REFERENCES artists(id) ON DELETE CASCADE,
    image_url VARCHAR(500) NOT NULL,
    title VARCHAR(200),
    description TEXT,
    display_order INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Индексы для оптимизации
CREATE INDEX IF NOT EXISTS idx_cities_active ON cities(is_active);
CREATE INDEX IF NOT EXISTS idx_cities_name ON cities(name);
CREATE INDEX IF NOT EXISTS idx_categories_active ON categories(is_active);
CREATE INDEX IF NOT EXISTS idx_categories_type ON categories(type);
CREATE INDEX IF NOT EXISTS idx_artists_city ON artists(city_id);
CREATE INDEX IF NOT EXISTS idx_artists_category ON artists(category_id);
CREATE INDEX IF NOT EXISTS idx_artists_active ON artists(is_active);
CREATE INDEX IF NOT EXISTS idx_artist_gallery_artist ON artist_gallery(artist_id);

-- RLS (Row Level Security) политики
ALTER TABLE cities ENABLE ROW LEVEL SECURITY;
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE artists ENABLE ROW LEVEL SECURITY;
ALTER TABLE artist_gallery ENABLE ROW LEVEL SECURITY;

-- Политики для публичного чтения
CREATE POLICY "Публичное чтение городов" ON cities FOR SELECT USING (is_active = true);
CREATE POLICY "Публичное чтение категорий" ON categories FOR SELECT USING (is_active = true);
CREATE POLICY "Публичное чтение артистов" ON artists FOR SELECT USING (is_active = true);
CREATE POLICY "Публичное чтение галереи" ON artist_gallery FOR SELECT USING (true);

-- Триггеры для автоматического обновления updated_at
CREATE TRIGGER update_cities_updated_at BEFORE UPDATE ON cities FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_categories_updated_at BEFORE UPDATE ON categories FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_artists_updated_at BEFORE UPDATE ON artists FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Функция для получения артистов с фильтрацией
CREATE OR REPLACE FUNCTION get_artists_filtered(
    p_city VARCHAR DEFAULT '',
    p_category VARCHAR DEFAULT '',
    p_limit INTEGER DEFAULT 50,
    p_offset INTEGER DEFAULT 0
)
RETURNS TABLE (
    id BIGINT,
    name VARCHAR,
    username VARCHAR,
    bio TEXT,
    avatar_url VARCHAR,
    city_name VARCHAR,
    category_name VARCHAR,
    category_type VARCHAR,
    specialties TEXT[],
    rating DECIMAL,
    telegram VARCHAR,
    instagram VARCHAR,
    tiktok VARCHAR,
    is_active BOOLEAN,
    gallery_urls TEXT[]
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        a.id,
        a.name,
        a.username,
        a.bio,
        a.avatar_url,
        c.name as city_name,
        cat.name as category_name,
        cat.type as category_type,
        a.specialties,
        a.rating,
        a.telegram,
        a.instagram,
        a.tiktok,
        a.is_active,
        ARRAY(
            SELECT ag.image_url 
            FROM artist_gallery ag 
            WHERE ag.artist_id = a.id 
            ORDER BY ag.display_order, ag.id
        ) as gallery_urls
    FROM artists a
    LEFT JOIN cities c ON a.city_id = c.id
    LEFT JOIN categories cat ON a.category_id = cat.id
    WHERE 
        a.is_active = true
        AND (p_city = '' OR c.name ILIKE '%' || p_city || '%')
        AND (p_category = '' OR cat.name ILIKE '%' || p_category || '%')
    ORDER BY a.rating DESC, a.created_at DESC
    LIMIT p_limit
    OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

-- Вставка начальных данных: города
INSERT INTO cities (name, code, population, display_order) VALUES
('Москва', 'MSC', 13200000, 1),
('Санкт-Петербург', 'SPB', 5600000, 2),
('Новосибирск', 'NSK', 1700000, 3),
('Екатеринбург', 'EKB', 1600000, 4),
('Казань', 'KAZ', 1400000, 5)
ON CONFLICT (name) DO UPDATE SET
    code = EXCLUDED.code,
    population = EXCLUDED.population,
    display_order = EXCLUDED.display_order;

-- Вставка начальных данных: категории
INSERT INTO categories (name, code, type, description, display_order) VALUES
('Tattoo', 'tattoo', 'service', 'Татуировки', 1),
('Hair', 'hair', 'service', 'Парикмахерские услуги', 2),
('Nails', 'nails', 'service', 'Маникюр и педикюр', 3),
('Piercing', 'piercing', 'service', 'Пирсинг', 4),
('GTM BRAND', 'gtm_brand', 'product', 'Брендовые товары GTM', 5),
('Jewelry', 'jewelry', 'product', 'Украшения', 6),
('Custom', 'custom', 'product', 'Индивидуальные заказы', 7),
('Second', 'second', 'product', 'Вторые руки', 8)
ON CONFLICT (name) DO UPDATE SET
    code = EXCLUDED.code,
    type = EXCLUDED.type,
    description = EXCLUDED.description,
    display_order = EXCLUDED.display_order;

-- Комментарии к таблицам
COMMENT ON TABLE cities IS 'Города где работают артисты';
COMMENT ON TABLE categories IS 'Категории услуг и товаров';
COMMENT ON TABLE artists IS 'Артисты/мастера с привязкой к городам и категориям';
COMMENT ON TABLE artist_gallery IS 'Галерея работ артистов';