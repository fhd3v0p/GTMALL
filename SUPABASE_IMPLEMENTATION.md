# Реализация загрузки артистов из Supabase API и CDN

## Обзор

Данная реализация позволяет загружать артистов по городам и категориям из Supabase API и CDN бакета, что значительно ускоряет загрузку по сравнению с локальными ассетами.

## Архитектура

### 1. База данных Supabase

#### Таблицы:
- `artists` - основная таблица артистов
- `cities` - города работы артистов
- `categories` - категории услуг/товаров
- `artist_cities` - связь артистов с городами (many-to-many)
- `artist_categories` - связь артистов с категориями (many-to-many)

#### Функция фильтрации:
```sql
CREATE OR REPLACE FUNCTION get_artists_filtered(
    p_city VARCHAR DEFAULT NULL,
    p_category VARCHAR DEFAULT NULL,
    p_limit INTEGER DEFAULT 50,
    p_offset INTEGER DEFAULT 0
)
```

### 2. Сервисы

#### SupabaseArtistsService
- `getCities()` - получение всех городов
- `getCategories()` - получение всех категорий
- `getArtistsFiltered()` - получение артистов с фильтрацией
- `getArtistsByCity()` - получение артистов по городу
- `getArtistsByCategory()` - получение артистов по категории
- `getArtistsByCityAndCategory()` - получение артистов по городу и категории

#### CdnImageService
- `getImageUrl()` - формирование URL изображения
- `getArtistAvatarUrl()` - URL аватара артиста
- `getArtistGalleryUrls()` - URL галереи артиста

### 3. Виджеты

#### CdnImage
Универсальный виджет для отображения изображений с CDN:
```dart
CdnImage(
  imageUrl: 'artists/123/avatar.png',
  width: 100,
  height: 100,
  borderRadius: BorderRadius.circular(50),
)
```

#### ArtistAvatar
Специализированный виджет для аватаров артистов:
```dart
ArtistAvatar(
  artistId: '123',
  size: 100,
)
```

#### ArtistGallery
Виджет для отображения галереи артиста:
```dart
ArtistGallery(
  artistId: '123',
  maxImages: 10,
)
```

## Использование

### 1. Загрузка городов

```dart
// В CitySelectionScreen
Future<void> _loadCities() async {
  final citiesData = await SupabaseArtistsService.getCities();
  // Преобразование данных в _CityPoint
}
```

### 2. Загрузка артистов по городу

```dart
// В MasterCloudScreen
Future<void> _loadMasters() async {
  final supabaseMasters = await SupabaseArtistsService.getArtistsByCity(widget.city);
  // Обработка результатов
}
```

### 3. Отображение изображений

```dart
// Вместо Image.asset используем CdnImage
CdnImage(
  imageUrl: master.avatar,
  width: avatarSize,
  height: avatarSize,
  borderRadius: BorderRadius.circular(avatarSize / 2),
)
```

## Преимущества

### 1. Производительность
- **Быстрая загрузка**: CDN обеспечивает быструю доставку изображений
- **Кэширование**: Встроенное кэширование на 5 минут
- **Фильтрация на уровне БД**: Эффективная фильтрация по городам и категориям

### 2. Масштабируемость
- **Динамическое добавление**: Новые артисты добавляются без обновления приложения
- **Гибкая структура**: Поддержка множественных городов и категорий
- **CDN**: Глобальное распространение контента

### 3. Надежность
- **Fallback система**: Автоматический переход на локальные ассеты при ошибках
- **Обработка ошибок**: Graceful degradation при проблемах с сетью
- **Валидация данных**: Проверка корректности данных

## Настройка

### 1. Supabase Configuration

Убедитесь, что в `lib/api_config.dart` правильно настроены параметры:

```dart
static const String supabaseUrl = 'https://your-project.supabase.co';
static const String supabaseAnonKey = 'your-anon-key';
static const String storageBucket = 'gtm-assets';
```

### 2. База данных

Выполните SQL скрипт `gtm-prod1/bot/supabase_schema_extended.sql` для создания необходимых таблиц и функций.

### 3. Storage Bucket

Создайте bucket `gtm-assets` в Supabase Storage со следующей структурой:
```
gtm-assets/
├── artists/
│   ├── 1/
│   │   ├── avatar.png
│   │   ├── gallery1.jpg
│   │   ├── gallery2.jpg
│   │   └── ...
│   └── ...
├── banners/
├── products/
└── avatars/
```

## Мониторинг

### Логирование

Все операции логируются с префиксом `DEBUG:`:
```
DEBUG: Загружаем города из Supabase
DEBUG: Загружено 5 городов из Supabase
DEBUG: Загружаем мастеров из Supabase для города: Москва
DEBUG: Загружено из Supabase: 12 мастеров
```

### Метрики

Отслеживайте следующие метрики:
- Время загрузки артистов
- Количество загруженных артистов
- Процент успешных загрузок
- Использование кэша

## Troubleshooting

### Проблемы с загрузкой

1. **Проверьте конфигурацию Supabase**
2. **Убедитесь в правильности RLS политик**
3. **Проверьте доступность Storage bucket**

### Проблемы с изображениями

1. **Проверьте права доступа к Storage**
2. **Убедитесь в правильности путей к файлам**
3. **Проверьте формат изображений**

### Fallback система

При проблемах с Supabase система автоматически переключается на:
1. Старый API сервис
2. Локальные ассеты
3. Sample данные

## Будущие улучшения

### 1. Оптимизация изображений
- Автоматическое изменение размера
- WebP формат
- Lazy loading

### 2. Расширенное кэширование
- Persistent кэш
- Предзагрузка изображений
- Умная инвалидация кэша

### 3. Аналитика
- Отслеживание популярных артистов
- Метрики производительности
- A/B тестирование

### 4. Офлайн режим
- Синхронизация данных
- Офлайн просмотр
- Queue для обновлений 