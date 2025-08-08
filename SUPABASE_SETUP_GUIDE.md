# Руководство по настройке Supabase для работы с артистами

## 1. Настройка базы данных

### Выполните SQL скрипт
```sql
-- Выполните скрипт supabase_schema_extended.sql в SQL Editor Supabase
-- Это создаст все необходимые таблицы и функции
```

### Проверьте созданные таблицы:
- `cities` - города
- `categories` - категории
- `artists` - артисты
- `artist_cities` - связь артистов с городами
- `artist_categories` - связь артистов с категориями

## 2. Добавление данных в базу

### Добавьте города:
```sql
INSERT INTO cities (name, code) VALUES 
    ('Москва', 'MSC'),
    ('Санкт-Петербург', 'SPB'),
    ('Новосибирск', 'NSK'),
    ('Казань', 'KAZ'),
    ('Екатеринбург', 'EKB')
ON CONFLICT (name) DO NOTHING;
```

### Добавьте категории:
```sql
INSERT INTO categories (name, type, description) VALUES 
    ('Tattoo', 'service', 'Татуировки'),
    ('Piercing', 'service', 'Пирсинг'),
    ('Haircut', 'service', 'Стрижки'),
    ('Makeup', 'service', 'Макияж'),
    ('Nails', 'service', 'Маникюр'),
    ('Clothing', 'product', 'Одежда'),
    ('Shoes', 'product', 'Обувь'),
    ('Accessories', 'product', 'Аксессуары'),
    ('Jewelry', 'product', 'Украшения')
ON CONFLICT (name) DO NOTHING;
```

### Добавьте артистов:
```sql
INSERT INTO artists (name, bio, avatar_url, telegram, tiktok, is_active) VALUES 
    ('Lin++', 'Профессиональный тату-мастер', 'artists/Lin++/avatar.png', '@lin_plus_plus', '@lin_plus_plus', true),
    ('EMI', 'Мастер пирсинга и татуировок', 'artists/EMI/avatar.png', '@emi_tattoo', '@emi_tattoo', true),
    ('Blodivamp', 'Специалист по татуировкам', 'artists/Blodivamp/avatar.png', '@blodivamp', '@blodivamp', true),
    ('msk_tattoo_EMI', 'Московский тату-мастер', 'artists/msk_tattoo_EMI/avatar.png', '@msk_emi', '@msk_emi', true)
ON CONFLICT (name) DO NOTHING;
```

### Свяжите артистов с городами:
```sql
-- Получите ID артистов и городов
INSERT INTO artist_cities (artist_id, city_id)
SELECT a.id, c.id
FROM artists a, cities c
WHERE a.name = 'Lin++' AND c.name = 'Москва'
ON CONFLICT (artist_id, city_id) DO NOTHING;

INSERT INTO artist_cities (artist_id, city_id)
SELECT a.id, c.id
FROM artists a, cities c
WHERE a.name = 'EMI' AND c.name = 'Санкт-Петербург'
ON CONFLICT (artist_id, city_id) DO NOTHING;

INSERT INTO artist_cities (artist_id, city_id)
SELECT a.id, c.id
FROM artists a, cities c
WHERE a.name = 'Blodivamp' AND c.name = 'Москва'
ON CONFLICT (artist_id, city_id) DO NOTHING;

INSERT INTO artist_cities (artist_id, city_id)
SELECT a.id, c.id
FROM artists a, cities c
WHERE a.name = 'msk_tattoo_EMI' AND c.name = 'Москва'
ON CONFLICT (artist_id, city_id) DO NOTHING;
```

### Свяжите артистов с категориями:
```sql
-- Получите ID артистов и категорий
INSERT INTO artist_categories (artist_id, category_id)
SELECT a.id, c.id
FROM artists a, categories c
WHERE a.name = 'Lin++' AND c.name = 'Tattoo'
ON CONFLICT (artist_id, category_id) DO NOTHING;

INSERT INTO artist_categories (artist_id, category_id)
SELECT a.id, c.id
FROM artists a, categories c
WHERE a.name = 'EMI' AND c.name = 'Tattoo'
ON CONFLICT (artist_id, category_id) DO NOTHING;

INSERT INTO artist_categories (artist_id, category_id)
SELECT a.id, c.id
FROM artists a, categories c
WHERE a.name = 'EMI' AND c.name = 'Piercing'
ON CONFLICT (artist_id, category_id) DO NOTHING;

INSERT INTO artist_categories (artist_id, category_id)
SELECT a.id, c.id
FROM artists a, categories c
WHERE a.name = 'Blodivamp' AND c.name = 'Tattoo'
ON CONFLICT (artist_id, category_id) DO NOTHING;

INSERT INTO artist_categories (artist_id, category_id)
SELECT a.id, c.id
FROM artists a, categories c
WHERE a.name = 'msk_tattoo_EMI' AND c.name = 'Tattoo'
ON CONFLICT (artist_id, category_id) DO NOTHING;
```

## 3. Настройка Storage

### Создайте bucket `gtm-assets-public`:
1. Перейдите в Storage в Supabase Dashboard
2. Нажмите "New bucket"
3. Назовите bucket `gtm-assets-public`
4. Отметьте "Public bucket" для публичного доступа

### Структура папок:
```
gtm-assets-public/
├── artists/
│   ├── Lin++/
│   │   ├── avatar.png
│   │   ├── gallery1.jpg
│   │   ├── gallery2.jpg
│   │   └── ...
│   ├── EMI/
│   │   ├── avatar.png
│   │   ├── gallery1.jpg
│   │   └── ...
│   ├── Blodivamp/
│   │   ├── avatar.png
│   │   └── ...
│   └── msk_tattoo_EMI/
│       ├── avatar.png
│       └── ...
├── banners/
│   ├── giveaway_banner.png
│   ├── city_selection_banner.png
│   └── master_cloud_banner.png
└── avatars/
    ├── avatar1.png
    ├── avatar2.png
    └── ...
```

### Загрузите изображения:
1. Создайте папку `artists` в bucket
2. Для каждого артиста создайте папку с его именем
3. Загрузите `avatar.png` в папку артиста
4. Загрузите изображения галереи как `gallery1.jpg`, `gallery2.jpg` и т.д.

## 4. Проверка работы

### Тестирование API:
1. Откройте SQL Editor в Supabase
2. Выполните запрос для проверки функции:

```sql
-- Проверка получения артистов
SELECT * FROM get_artists_filtered();

-- Проверка фильтрации по городу
SELECT * FROM get_artists_filtered(p_city := 'Москва');

-- Проверка фильтрации по категории
SELECT * FROM get_artists_filtered(p_category := 'Tattoo');

-- Проверка фильтрации по городу и категории
SELECT * FROM get_artists_filtered(p_city := 'Москва', p_category := 'Tattoo');
```

### Тестирование Storage:
1. Проверьте доступность изображений по URL:
   ```
   https://your-project.supabase.co/storage/v1/object/public/gtm-assets-public/artists/Lin++/avatar.png
   ```

## 5. Настройка RLS (Row Level Security)

### Убедитесь, что RLS включен:
```sql
-- Проверьте, что RLS включен для всех таблиц
SELECT schemaname, tablename, rowsecurity 
FROM pg_tables 
WHERE tablename IN ('cities', 'categories', 'artists', 'artist_cities', 'artist_categories');
```

### Проверьте политики:
```sql
-- Проверьте существующие политики
SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual 
FROM pg_policies 
WHERE tablename IN ('cities', 'categories', 'artists', 'artist_cities', 'artist_categories');
```

## 6. Мониторинг и отладка

### Логи в Supabase:
1. Перейдите в Logs в Supabase Dashboard
2. Фильтруйте по API calls для отслеживания запросов

### Проверка кэша:
```sql
-- Проверьте размер кэша (если используется)
SELECT schemaname, tablename, attname, n_distinct, correlation 
FROM pg_stats 
WHERE tablename IN ('cities', 'categories', 'artists');
```

## 7. Оптимизация

### Индексы:
```sql
-- Создайте дополнительные индексы для оптимизации
CREATE INDEX IF NOT EXISTS idx_artists_name ON artists(name);
CREATE INDEX IF NOT EXISTS idx_artists_active ON artists(is_active);
CREATE INDEX IF NOT EXISTS idx_cities_name ON cities(name);
CREATE INDEX IF NOT EXISTS idx_categories_name ON categories(name);
```

### Мониторинг производительности:
```sql
-- Проверьте медленные запросы
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
WHERE query LIKE '%get_artists_filtered%'
ORDER BY mean_time DESC;
```

## 8. Troubleshooting

### Проблемы с API:
1. **Ошибка 401**: Проверьте API ключи в конфигурации
2. **Ошибка 403**: Проверьте RLS политики
3. **Ошибка 404**: Проверьте существование таблиц и функций

### Проблемы с Storage:
1. **Ошибка 404**: Проверьте существование файлов и правильность путей
2. **Ошибка 403**: Проверьте права доступа к bucket
3. **Медленная загрузка**: Проверьте размер файлов и CDN настройки

### Проблемы с данными:
1. **Пустые результаты**: Проверьте связи между таблицами
2. **Дубликаты**: Проверьте UNIQUE ограничения
3. **Неправильная фильтрация**: Проверьте функцию `get_artists_filtered`

## 9. Дополнительные настройки

### Настройка CDN:
1. В Supabase Dashboard перейдите в Settings > API
2. Проверьте настройки CDN для Storage
3. Убедитесь, что bucket публичный

### Настройка мониторинга:
1. Настройте алерты для ошибок API
2. Мониторьте использование Storage
3. Отслеживайте производительность запросов

---

После выполнения всех шагов ваша система будет готова к работе с артистами через Supabase API и Storage! 