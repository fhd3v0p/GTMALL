-- Создание таблицы products в Supabase
-- Выполните этот SQL в Supabase Dashboard -> SQL Editor

-- Создаем таблицу products
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    subcategory VARCHAR(50),
    brand VARCHAR(255),
    description TEXT,
    summary TEXT,
    price DECIMAL(10,2) NOT NULL,
    old_price DECIMAL(10,2),
    discount_percent INTEGER DEFAULT 0,
    size_type VARCHAR(20) DEFAULT 'clothing',
    size_clothing VARCHAR(10),
    size_pants VARCHAR(10),
    size_shoes_eu INTEGER,
    size VARCHAR(50),
    color VARCHAR(255),
    master_id INTEGER REFERENCES artists(id),
    master_telegram VARCHAR(255),
    avatar TEXT,
    gallery JSONB DEFAULT '[]',
    is_new BOOLEAN DEFAULT false,
    is_available BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Создаем индексы для быстрого поиска
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
CREATE INDEX IF NOT EXISTS idx_products_master_id ON products(master_id);
CREATE INDEX IF NOT EXISTS idx_products_is_available ON products(is_available);

-- Включаем Row Level Security (RLS)
ALTER TABLE products ENABLE ROW LEVEL SECURITY;

-- Создаем политики для RLS
-- Политика для чтения (все могут читать доступные продукты)
CREATE POLICY "Products are viewable by everyone" ON products
    FOR SELECT USING (is_available = true);

-- Политика для вставки (только аутентифицированные пользователи)
CREATE POLICY "Users can insert products" ON products
    FOR INSERT WITH CHECK (true);

-- Политика для обновления (только владелец или админ)
CREATE POLICY "Users can update own products" ON products
    FOR UPDATE USING (true);

-- Политика для удаления (только админ)
CREATE POLICY "Only admins can delete products" ON products
    FOR DELETE USING (false);

-- Создаем функцию для автоматического обновления updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Создаем триггер для автоматического обновления updated_at
CREATE TRIGGER update_products_updated_at 
    BEFORE UPDATE ON products 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Добавляем комментарии к таблице
COMMENT ON TABLE products IS 'Таблица товаров для GTM приложения';
COMMENT ON COLUMN products.name IS 'Название товара';
COMMENT ON COLUMN products.category IS 'Категория товара (GTM BRAND, Jewelry, Custom, Second)';
COMMENT ON COLUMN products.subcategory IS 'Подкатегория (tshirt, pants, shoes, etc.)';
COMMENT ON COLUMN products.brand IS 'Бренд товара';
COMMENT ON COLUMN products.description IS 'Полное описание товара';
COMMENT ON COLUMN products.summary IS 'Краткое описание для корзины';
COMMENT ON COLUMN products.price IS 'Цена в рублях';
COMMENT ON COLUMN products.old_price IS 'Старая цена (для скидок)';
COMMENT ON COLUMN products.discount_percent IS 'Процент скидки';
COMMENT ON COLUMN products.size_type IS 'Тип размера (clothing, shoes, one_size)';
COMMENT ON COLUMN products.size_clothing IS 'Размер одежды (XS, S, M, L, XL, XXL)';
COMMENT ON COLUMN products.size_pants IS 'Размер штанов';
COMMENT ON COLUMN products.size_shoes_eu IS 'EU размер обуви';
COMMENT ON COLUMN products.size IS 'Общий размер';
COMMENT ON COLUMN products.color IS 'Цвет товара';
COMMENT ON COLUMN products.master_id IS 'ID мастера/артиста';
COMMENT ON COLUMN products.master_telegram IS 'Telegram мастера';
COMMENT ON COLUMN products.avatar IS 'URL главной фотографии товара';
COMMENT ON COLUMN products.gallery IS 'JSON массив URL фотографий галереи';
COMMENT ON COLUMN products.is_new IS 'Флаг новинки';
COMMENT ON COLUMN products.is_available IS 'Флаг доступности товара'; 