-- Миграция таблицы artists для связи с cities и categories
-- Выполните этот скрипт в SQL Editor Supabase

-- Сначала добавим новые столбцы
ALTER TABLE artists 
ADD COLUMN IF NOT EXISTS city_id BIGINT REFERENCES cities(id),
ADD COLUMN IF NOT EXISTS category_id BIGINT REFERENCES categories(id),
ADD COLUMN IF NOT EXISTS instagram VARCHAR(100),
ADD COLUMN IF NOT EXISTS display_order INTEGER DEFAULT 0;

-- Заполним city_id на основе текстового поля city
UPDATE artists 
SET city_id = cities.id 
FROM cities 
WHERE artists.city = cities.name OR artists.city ILIKE cities.name;

-- Заполним category_id на основе specialties или создадим категорию Tattoo по умолчанию
UPDATE artists 
SET category_id = categories.id 
FROM categories 
WHERE categories.name = 'Tattoo' AND artists.category_id IS NULL;

-- Создадим индексы
CREATE INDEX IF NOT EXISTS idx_artists_city_id ON artists(city_id);
CREATE INDEX IF NOT EXISTS idx_artists_category_id ON artists(category_id);

-- Обновим функцию get_artists_filtered с правильными типами
CREATE OR REPLACE FUNCTION get_artists_filtered(
    p_city TEXT DEFAULT '',
    p_category TEXT DEFAULT '',
    p_limit INTEGER DEFAULT 50,
    p_offset INTEGER DEFAULT 0
)
RETURNS TABLE (
    id BIGINT,
    name TEXT,
    username TEXT,
    bio TEXT,
    avatar_url TEXT,
    city_name TEXT,
    category_name TEXT,
    category_type TEXT,
    specialties TEXT[],
    rating DECIMAL,
    telegram TEXT,
    instagram TEXT,
    tiktok TEXT,
    is_active BOOLEAN,
    gallery_urls TEXT[]
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        a.id,
        a.name::TEXT,
        a.username::TEXT,
        a.bio::TEXT,
        a.avatar_url::TEXT,
        COALESCE(c.name, a.city)::TEXT as city_name,
        COALESCE(cat.name, 'Unknown')::TEXT as category_name,
        COALESCE(cat.type, 'service')::TEXT as category_type,
        a.specialties,
        a.rating,
        a.telegram::TEXT,
        a.instagram::TEXT,
        a.tiktok::TEXT,
        a.is_active,
        COALESCE(
            ARRAY(
                SELECT ag.image_url::TEXT
                FROM artist_gallery ag 
                WHERE ag.artist_id = a.id 
                ORDER BY ag.display_order, ag.id
            ),
            ARRAY[]::TEXT[]
        ) as gallery_urls
    FROM artists a
    LEFT JOIN cities c ON a.city_id = c.id
    LEFT JOIN categories cat ON a.category_id = cat.id
    WHERE 
        a.is_active = true
        AND (p_city = '' OR c.name ILIKE '%' || p_city || '%' OR a.city ILIKE '%' || p_city || '%')
        AND (p_category = '' OR cat.name ILIKE '%' || p_category || '%')
    ORDER BY a.rating DESC, a.created_at DESC
    LIMIT p_limit
    OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

-- Комментарий к обновлению
COMMENT ON FUNCTION get_artists_filtered IS 'Получение артистов с фильтрацией по городам и категориям (обновленная версия)';