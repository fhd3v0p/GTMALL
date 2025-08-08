-- GTM Supabase Database Setup
-- Выполните этот скрипт в SQL Editor Supabase

-- Таблица пользователей
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(100),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    tickets_count INTEGER DEFAULT 0,
    has_subscription_ticket BOOLEAN DEFAULT FALSE,
    referral_code VARCHAR(20) UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Таблица подписок на каналы
CREATE TABLE IF NOT EXISTS subscriptions (
    id BIGSERIAL PRIMARY KEY,
    telegram_id BIGINT REFERENCES users(telegram_id) ON DELETE CASCADE,
    channel_id BIGINT NOT NULL,
    channel_name VARCHAR(200) NOT NULL,
    channel_username VARCHAR(100),
    subscribed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(telegram_id, channel_id)
);

-- Таблица рефералов
CREATE TABLE IF NOT EXISTS referrals (
    id BIGSERIAL PRIMARY KEY,
    telegram_id BIGINT REFERENCES users(telegram_id) ON DELETE CASCADE,
    referral_code VARCHAR(20) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Таблица артистов
CREATE TABLE IF NOT EXISTS artists (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    username VARCHAR(100),
    bio TEXT,
    avatar_url VARCHAR(500),
    city VARCHAR(100),
    specialties TEXT[],
    rating DECIMAL(3,2) DEFAULT 0.0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Таблица галереи артистов
CREATE TABLE IF NOT EXISTS artist_gallery (
    id BIGSERIAL PRIMARY KEY,
    artist_id BIGINT REFERENCES artists(id) ON DELETE CASCADE,
    image_url VARCHAR(500) NOT NULL,
    title VARCHAR(200),
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Таблица розыгрышей
CREATE TABLE IF NOT EXISTS giveaways (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    prize_amount DECIMAL(10,2),
    start_date TIMESTAMP WITH TIME ZONE,
    end_date TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Таблица билетов розыгрыша
CREATE TABLE IF NOT EXISTS giveaway_tickets (
    id BIGSERIAL PRIMARY KEY,
    giveaway_id BIGINT REFERENCES giveaways(id) ON DELETE CASCADE,
    telegram_id BIGINT REFERENCES users(telegram_id) ON DELETE CASCADE,
    ticket_number INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(giveaway_id, telegram_id)
);

-- Индексы для оптимизации
CREATE INDEX IF NOT EXISTS idx_users_telegram_id ON users(telegram_id);
CREATE INDEX IF NOT EXISTS idx_subscriptions_telegram_id ON subscriptions(telegram_id);
CREATE INDEX IF NOT EXISTS idx_subscriptions_channel_id ON subscriptions(channel_id);
CREATE INDEX IF NOT EXISTS idx_referrals_telegram_id ON referrals(telegram_id);
CREATE INDEX IF NOT EXISTS idx_referrals_code ON referrals(referral_code);
CREATE INDEX IF NOT EXISTS idx_artists_active ON artists(is_active);
CREATE INDEX IF NOT EXISTS idx_giveaway_tickets_telegram_id ON giveaway_tickets(telegram_id);

-- RLS (Row Level Security) политики
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE referrals ENABLE ROW LEVEL SECURITY;
ALTER TABLE artists ENABLE ROW LEVEL SECURITY;
ALTER TABLE artist_gallery ENABLE ROW LEVEL SECURITY;
ALTER TABLE giveaways ENABLE ROW LEVEL SECURITY;
ALTER TABLE giveaway_tickets ENABLE ROW LEVEL SECURITY;

-- Политики для чтения (публичный доступ)
CREATE POLICY "Публичное чтение артистов" ON artists FOR SELECT USING (is_active = true);
CREATE POLICY "Публичное чтение галереи" ON artist_gallery FOR SELECT USING (true);
CREATE POLICY "Публичное чтение розыгрышей" ON giveaways FOR SELECT USING (is_active = true);

-- Политики для пользователей (только свои данные)
CREATE POLICY "Пользователи видят свои данные" ON users FOR ALL USING (telegram_id = current_setting('app.telegram_id')::bigint);
CREATE POLICY "Пользователи видят свои подписки" ON subscriptions FOR ALL USING (telegram_id = current_setting('app.telegram_id')::bigint);
CREATE POLICY "Пользователи видят свои рефералы" ON referrals FOR ALL USING (telegram_id = current_setting('app.telegram_id')::bigint);
CREATE POLICY "Пользователи видят свои билеты" ON giveaway_tickets FOR ALL USING (telegram_id = current_setting('app.telegram_id')::bigint);

-- Функция для обновления updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Триггеры для автоматического обновления updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_artists_updated_at BEFORE UPDATE ON artists FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Функция для создания реферального кода
CREATE OR REPLACE FUNCTION generate_referral_code()
RETURNS VARCHAR(20) AS $$
BEGIN
    RETURN upper(substring(md5(random()::text) from 1 for 8));
END;
$$ LANGUAGE plpgsql;

-- Комментарии к таблицам
COMMENT ON TABLE users IS 'Пользователи Telegram бота';
COMMENT ON TABLE subscriptions IS 'Подписки пользователей на каналы';
COMMENT ON TABLE referrals IS 'Реферальные коды пользователей';
COMMENT ON TABLE artists IS 'Артисты/мастера';
COMMENT ON TABLE artist_gallery IS 'Галерея работ артистов';
COMMENT ON TABLE giveaways IS 'Розыгрыши призов';
COMMENT ON TABLE giveaway_tickets IS 'Билеты пользователей в розыгрышах';

-- Тестовые данные
INSERT INTO artists (name, username, bio, avatar_url, city, specialties, rating, is_active) VALUES
('Test Artist', 'test_artist', 'Тестовый артист для проверки', 'https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets/avatars/test.jpg', 'Москва', ARRAY['Тату', 'Пирсинг'], 4.5, true)
ON CONFLICT DO NOTHING; 