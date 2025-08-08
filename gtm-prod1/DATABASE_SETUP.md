# 🗄️ Настройка базы данных Supabase

## 📋 Шаги для настройки

### 1. Откройте Supabase Dashboard
Перейдите в ваш проект: https://supabase.com/dashboard/project/rxmtovqxjsvogyywyrha

### 2. Откройте SQL Editor
- В левом меню найдите "SQL Editor"
- Нажмите "New query"

### 3. Выполните SQL скрипт
Скопируйте содержимое файла `bot/fix_database.sql` и вставьте в SQL Editor.

### 4. Нажмите "Run"
Выполните скрипт. Должны создаться все таблицы и политики.

### 5. Проверьте результат
В левом меню перейдите в "Table Editor" и убедитесь, что создались таблицы:
- `users`
- `artists` 
- `subscriptions`
- `referrals`
- `artist_gallery`
- `giveaways`
- `giveaway_tickets`

## 🔧 Проверка настройки

После выполнения SQL скрипта запустите тест:

```bash
cd gtm-prod1/bot
python3 debug_supabase.py
```

Должны быть все тесты зелеными ✅

## 🚀 Запуск системы

После настройки базы данных:

```bash
# Тест бота
python3 bot_simple.py

# Полная система
./run_local_supabase.sh
```

## 📁 Файлы для настройки

- `bot/fix_database.sql` - SQL схема базы данных
- `bot/debug_supabase.py` - скрипт диагностики
- `bot/.env` - конфигурация (уже настроен)

## ⚠️ Если что-то не работает

1. Проверьте, что SQL скрипт выполнился без ошибок
2. Убедитесь, что в `.env` файле правильные ключи
3. Запустите `debug_supabase.py` для диагностики
4. Проверьте логи в Supabase Dashboard 