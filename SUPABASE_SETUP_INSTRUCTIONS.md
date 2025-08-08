# 🚀 Инструкция по настройке Supabase для артиста GTM

## ✅ Что уже сделано

1. **Артист GTM добавлен в Supabase** ✅
   - ID: 14
   - Имя: GTM
   - Категория: GTM BRAND
   - Telegram: @G_T_MODEL
   - Booking URL: https://t.me/GTM_ADM

## 📋 Что нужно сделать

### 1. Создать таблицу products в Supabase Dashboard

1. Откройте [Supabase Dashboard](https://supabase.com/dashboard/project/rxmtovqxjsvogyywyrha)
2. Перейдите в **SQL Editor**
3. Скопируйте и выполните SQL из файла `create_products_table.sql`

### 2. Загрузить изображения в Storage

1. В Supabase Dashboard перейдите в **Storage**
2. Выберите bucket `gtm-assets-public`
3. Создайте папки:
   - `artists/GTM/`
   - `products/GTM_Tshirt/`
4. Загрузите файлы:
   - `assets/artists/GTM/avatar.png` → `artists/GTM/avatar.png`
   - `assets/artists/GTM/gallery1.jpg` → `artists/GTM/gallery1.jpg`
   - `assets/artists/GTM/gallery2.jpg` → `artists/GTM/gallery2.jpg`
   - `assets/artists/GTM/gallery3.jpg` → `artists/GTM/gallery3.jpg`
   - `assets/products/GTM_Tshirt/avatar.jpg` → `products/GTM_Tshirt/avatar.jpg`
   - `assets/products/GTM_Tshirt/gallery1.jpg` → `products/GTM_Tshirt/gallery1.jpg`
   - `assets/products/GTM_Tshirt/gallery2.jpg` → `products/GTM_Tshirt/gallery2.jpg`
   - `assets/products/GTM_Tshirt/gallery3.jpg` → `products/GTM_Tshirt/gallery3.jpg`

### 3. Добавить продукт

После создания таблицы products и загрузки изображений, запустите скрипт:

```bash
source venv_supabase/bin/activate
python add_gtm_artist_and_product.py
```

## 📱 Структура данных

### Артист GTM
```json
{
  "id": 14,
  "name": "GTM",
  "username": "gtm_brand",
  "bio": "GOTHAM'S TOP MODEL - неформальный маркетплейс внутри Telegram...",
  "avatar_url": "https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets-public/artists/GTM/avatar.png",
  "city": "Санкт-Петербург, Москва, Екатеринбург, Новосибирск, Казань",
  "specialties": ["GTM BRAND"],
  "telegram": "@G_T_MODEL",
  "telegram_url": "https://t.me/G_T_MODEL",
  "booking_url": "https://t.me/GTM_ADM",
  "location_html": "Base:Saint-P, MSC"
}
```

### Продукт GOTHAM'S TOP MODEL CROP FIT T-SHIRT
```json
{
  "name": "GOTHAM'S TOP MODEL CROP FIT T-SHIRT",
  "category": "GTM BRAND",
  "subcategory": "tshirt",
  "brand": "GTM",
  "description": "Укороченная футболка GTM...",
  "price": 3799.00,
  "size": "XS S M L XL XXL",
  "color": "Черный",
  "master_id": 14,
  "master_telegram": "@G_T_MODEL",
  "avatar": "https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets-public/products/GTM_Tshirt/avatar.jpg",
  "gallery": [
    "https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets-public/products/GTM_Tshirt/gallery1.jpg",
    "https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets-public/products/GTM_Tshirt/gallery2.jpg",
    "https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets-public/products/GTM_Tshirt/gallery3.jpg"
  ],
  "is_new": true,
  "is_available": true
}
```

## 🎯 Результат

После выполнения всех шагов:

1. **В Master Cloud Screen** в категории "GTM BRAND" появится артист GTM
2. **При нажатии на аватар GTM** откроется Master Products Screen
3. **В Master Products Screen** будет отображаться продукт GOTHAM'S TOP MODEL CROP FIT T-SHIRT
4. **При нажатии на продукт** откроется Master Product Screen с:
   - Галереей продукта
   - Информацией о мастере
   - Кнопкой "Купить" (работает как booking URL с текстом о скидке)

## 🔧 Flutter интеграция

Flutter приложение уже настроено для работы с Supabase:
- `lib/api_config.dart` - конфигурация Supabase
- `lib/services/api_service.dart` - API для работы с данными
- `lib/screens/master_products_screen.dart` - экран продуктов мастера
- `lib/screens/master_product_screen.dart` - экран деталей продукта

Все данные будут автоматически загружаться из Supabase! 