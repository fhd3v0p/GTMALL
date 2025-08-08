-- Добавление артиста "Чучундра" в систему GTM
-- Этот скрипт добавляет данные артиста в Supabase

-- Получаем ID города и категории
DO $$
DECLARE
    moscow_id BIGINT;
    spb_id BIGINT;
    tattoo_id BIGINT;
    artist_id BIGINT;
BEGIN
    -- Получаем ID Москвы
    SELECT id INTO moscow_id FROM cities WHERE name = 'Москва';
    
    -- Получаем ID Санкт-Петербурга
    SELECT id INTO spb_id FROM cities WHERE name = 'Санкт-Петербург';
    
    -- Получаем ID категории Tattoo
    SELECT id INTO tattoo_id FROM categories WHERE name = 'Tattoo';
    
    -- Проверяем что все ID найдены
    IF moscow_id IS NULL OR spb_id IS NULL OR tattoo_id IS NULL THEN
        RAISE EXCEPTION 'Не найдены необходимые города или категории';
    END IF;
    
    -- Добавляем артиста "Чучундра" для Москвы
    INSERT INTO artists (
        name, 
        username, 
        bio, 
        avatar_url, 
        city_id, 
        category_id, 
        specialties, 
        rating,
        telegram,
        instagram,
        tiktok,
        is_active
    ) VALUES (
        'Чучундра',
        'chchundra_tattoo',
        'Профессиональный тату-мастер с уникальным стилем. Специализируется на черно-белых работах и минимализме.',
        'https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets/artists/Чучундра/avatar.png',
        moscow_id,
        tattoo_id,
        ARRAY['Черно-белые тату', 'Минимализм', 'Графика', 'Дотворк'],
        4.8,
        '@chchndra_tattoo',
        '@chchundra_ink',
        '@chchundra_art',
        true
    ) RETURNING id INTO artist_id;
    
    -- Добавляем изображения галереи
    INSERT INTO artist_gallery (artist_id, image_url, title, display_order) VALUES
    (artist_id, 'https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets/artists/Чучундра/gallery1.jpg', 'Работа 1', 1),
    (artist_id, 'https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets/artists/Чучундра/gallery2.jpg', 'Работа 2', 2),
    (artist_id, 'https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets/artists/Чучундра/gallery3.jpg', 'Работа 3', 3),
    (artist_id, 'https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets/artists/Чучундра/gallery4.jpg', 'Работа 4', 4),
    (artist_id, 'https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets/artists/Чучундра/gallery5.jpg', 'Работа 5', 5),
    (artist_id, 'https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets/artists/Чучундра/gallery6.jpg', 'Работа 6', 6),
    (artist_id, 'https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets/artists/Чучундра/gallery7.jpg', 'Работа 7', 7),
    (artist_id, 'https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets/artists/Чучундра/gallery8.jpg', 'Работа 8', 8),
    (artist_id, 'https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets/artists/Чучундра/gallery9.jpg', 'Работа 9', 9),
    (artist_id, 'https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets/artists/Чучундра/gallery10.jpg', 'Работа 10', 10);
    
    -- Добавляем дубликат для Санкт-Петербурга (если артист работает в двух городах)
    INSERT INTO artists (
        name, 
        username, 
        bio, 
        avatar_url, 
        city_id, 
        category_id, 
        specialties, 
        rating,
        telegram,
        instagram,
        tiktok,
        is_active
    ) VALUES (
        'Чучундра',
        'chchundra_tattoo_spb',
        'Профессиональный тату-мастер с уникальным стилем. Специализируется на черно-белых работах и минимализме. Филиал в СПб.',
        'https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets/artists/Чучундра/avatar.png',
        spb_id,
        tattoo_id,
        ARRAY['Черно-белые тату', 'Минимализм', 'Графика', 'Дотворк'],
        4.8,
        '@chchndra_tattoo',
        '@chchundra_ink',
        '@chchundra_art',
        true
    ) RETURNING id INTO artist_id;
    
    -- Добавляем те же изображения галереи для СПб
    INSERT INTO artist_gallery (artist_id, image_url, title, display_order) VALUES
    (artist_id, 'https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets/artists/Чучундра/gallery1.jpg', 'Работа 1', 1),
    (artist_id, 'https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets/artists/Чучундра/gallery2.jpg', 'Работа 2', 2),
    (artist_id, 'https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets/artists/Чучундра/gallery3.jpg', 'Работа 3', 3),
    (artist_id, 'https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets/artists/Чучундра/gallery4.jpg', 'Работа 4', 4),
    (artist_id, 'https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets/artists/Чучундра/gallery5.jpg', 'Работа 5', 5),
    (artist_id, 'https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets/artists/Чучундра/gallery6.jpg', 'Работа 6', 6),
    (artist_id, 'https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets/artists/Чучундра/gallery7.jpg', 'Работа 7', 7),
    (artist_id, 'https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets/artists/Чучундра/gallery8.jpg', 'Работа 8', 8),
    (artist_id, 'https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets/artists/Чучундра/gallery9.jpg', 'Работа 9', 9),
    (artist_id, 'https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets/artists/Чучундра/gallery10.jpg', 'Работа 10', 10);
    
    RAISE NOTICE 'Артист "Чучундра" успешно добавлен в БД для Москвы и СПб';
    
END $$;