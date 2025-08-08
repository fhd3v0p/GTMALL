-- Добавление полей для системы билетов и рефералов
-- Это поля будут отслеживать билеты за подписку, время создания пользователя и реферальные коды

-- Добавляем поле для отслеживания билета за подписки
ALTER TABLE users ADD COLUMN IF NOT EXISTS has_subscription_ticket BOOLEAN DEFAULT FALSE;

-- Добавляем поле для времени создания пользователя
ALTER TABLE users ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Добавляем поле для реферального кода
ALTER TABLE users ADD COLUMN IF NOT EXISTS referral_code VARCHAR(20) UNIQUE;

-- Обновляем существующие записи (если у пользователя есть билеты, считаем что билет за подписки уже начислен)
UPDATE users 
SET has_subscription_ticket = TRUE 
WHERE tickets_count > 0 AND has_subscription_ticket IS NULL;

-- Создаем индексы для быстрого поиска
CREATE INDEX IF NOT EXISTS idx_users_has_subscription_ticket ON users(has_subscription_ticket);
CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);
CREATE INDEX IF NOT EXISTS idx_users_referral_code ON users(referral_code);

-- Проверяем структуру таблицы
SELECT column_name, data_type, is_nullable, column_default 
FROM information_schema.columns 
WHERE table_name = 'users' 
ORDER BY ordinal_position; 