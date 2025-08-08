from django.db import models
from django.utils import timezone

class User(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    referred_by = models.CharField(max_length=50, null=True, blank=True)
    registered_at = models.DateTimeField(default=timezone.now)
    last_activity = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.username or self.first_name} ({self.user_id})"

class TaskCompletion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_completions')
    task_name = models.CharField(max_length=100)
    task_number = models.IntegerField()
    completed_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'task_completions'

    def __str__(self):
        return f"{self.user.username} - {self.task_name} #{self.task_number}"

class ReferralInvite(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('joined', 'Присоединился'),
        ('expired', 'Истек'),
    ]
    
    inviter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invites')
    invitee_id = models.BigIntegerField()
    invitee_username = models.CharField(max_length=100, null=True, blank=True)
    invitee_first_name = models.CharField(max_length=100, null=True, blank=True)
    invited_at = models.DateTimeField(default=timezone.now)
    joined_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        db_table = 'referral_invites'

    def __str__(self):
        return f"{self.inviter.username} -> {self.invitee_username} ({self.status})"

class GiveawayChannel(models.Model):
    channel_id = models.BigIntegerField(unique=True)
    channel_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'giveaway_channels'

    def __str__(self):
        return f"{self.channel_name} ({self.channel_id})"

# Новые модели для артистов
class Category(models.Model):
    TYPE_CHOICES = [
        ('service', 'Услуга'),
        ('product', 'Товар'),
    ]
    
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='service', verbose_name="Тип")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'categories'
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

class City(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название города")
    abbr = models.CharField(max_length=10, blank=True, verbose_name="Аббревиатура")
    dx = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True, verbose_name="Координата X")
    dy = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True, verbose_name="Координата Y")
    size = models.IntegerField(default=50, verbose_name="Размер")
    telegram_link = models.URLField(blank=True, verbose_name="Telegram ссылка")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'cities'
        verbose_name = "Город"
        verbose_name_plural = "Города"

    def __str__(self):
        return self.name

class Artist(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя артиста")
    bio = models.TextField(blank=True, verbose_name="Биография")
    avatar_url = models.URLField(blank=True, verbose_name="URL аватара")
    
    # Временные поля для HTTPS ссылок (пока MinIO не настроен)
    avatar_https = models.URLField(blank=True, verbose_name="HTTPS ссылка на аватар")
    gallery_https_1 = models.URLField(blank=True, verbose_name="HTTPS ссылка на фото 1")
    gallery_https_2 = models.URLField(blank=True, verbose_name="HTTPS ссылка на фото 2")
    gallery_https_3 = models.URLField(blank=True, verbose_name="HTTPS ссылка на фото 3")
    gallery_https_4 = models.URLField(blank=True, verbose_name="HTTPS ссылка на фото 4")
    gallery_https_5 = models.URLField(blank=True, verbose_name="HTTPS ссылка на фото 5")
    gallery_https_6 = models.URLField(blank=True, verbose_name="HTTPS ссылка на фото 6")
    gallery_https_7 = models.URLField(blank=True, verbose_name="HTTPS ссылка на фото 7")
    gallery_https_8 = models.URLField(blank=True, verbose_name="HTTPS ссылка на фото 8")
    gallery_https_9 = models.URLField(blank=True, verbose_name="HTTPS ссылка на фото 9")
    gallery_https_10 = models.URLField(blank=True, verbose_name="HTTPS ссылка на фото 10")
    
    folder_name = models.CharField(max_length=255, blank=True, verbose_name="Название папки")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Связи с категориями и городами
    categories = models.ManyToManyField(Category, through='ArtistCategory', verbose_name="Категории")
    cities = models.ManyToManyField(City, through='ArtistCity', verbose_name="Города")

    class Meta:
        db_table = 'artists'
        verbose_name = "Артист"
        verbose_name_plural = "Артисты"

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Генерируем folder_name на основе ID если его нет
        if not self.folder_name:
            if self.pk:
                self.folder_name = f"id{self.pk:06d}"
            else:
                # Временно сохраняем чтобы получить ID
                super().save(*args, **kwargs)
                self.folder_name = f"id{self.pk:06d}"
        
        super().save(*args, **kwargs)
    
    def get_avatar_url(self):
        """Получить URL аватара (приоритет HTTPS ссылке)"""
        return self.avatar_https if self.avatar_https else self.avatar_url
    
    def get_gallery_urls(self):
        """Получить список URL галереи из HTTPS полей"""
        urls = []
        for i in range(1, 11):
            field_name = f'gallery_https_{i}'
            url = getattr(self, field_name, '')
            if url:
                urls.append(url)
        return urls
    
    def get_gallery_count(self):
        """Получить количество фото в галерее"""
        return len(self.get_gallery_urls())

class ArtistCategory(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, verbose_name="Артист")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'artist_categories'
        unique_together = ('artist', 'category')
        verbose_name = "Категория артиста"
        verbose_name_plural = "Категории артистов"

    def __str__(self):
        return f"{self.artist.name} - {self.category.name}"

class ArtistCity(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, verbose_name="Артист")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Город")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'artist_cities'
        unique_together = ('artist', 'city')
        verbose_name = "Город артиста"
        verbose_name_plural = "Города артистов"

    def __str__(self):
        return f"{self.artist.name} - {self.city.name}"

class ArtistLinks(models.Model):
    artist = models.OneToOneField(Artist, on_delete=models.CASCADE, verbose_name="Артист")
    telegram = models.CharField(max_length=255, blank=True, verbose_name="Telegram")
    telegram_url = models.URLField(blank=True, verbose_name="Telegram URL")
    instagram = models.CharField(max_length=255, blank=True, verbose_name="Instagram")
    tiktok = models.CharField(max_length=255, blank=True, verbose_name="TikTok")
    tiktok_url = models.URLField(blank=True, verbose_name="TikTok URL")
    pinterest = models.CharField(max_length=255, blank=True, verbose_name="Pinterest")
    pinterest_url = models.URLField(blank=True, verbose_name="Pinterest URL")
    booking_url = models.URLField(blank=True, verbose_name="Booking URL")
    location_html = models.TextField(blank=True, verbose_name="Location HTML")
    gallery_html = models.TextField(blank=True, verbose_name="Gallery HTML")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'artist_links'
        verbose_name = "Ссылки артиста"
        verbose_name_plural = "Ссылки артистов"

    def __str__(self):
        return f"Ссылки {self.artist.name}"

class Product(models.Model):
    SIZE_TYPE_CHOICES = [
        ('clothing', 'Одежда'),
        ('shoes', 'Обувь'),
        ('one_size', 'Один размер'),
    ]
    
    SUBCATEGORY_CHOICES = [
        ('pants', 'Штаны'),
        ('outerwear', 'Верхняя одежда'),
        ('shoes', 'Обувь'),
        ('tshirt', 'Футболка'),
        ('skirt', 'Юбка'),
        ('dress', 'Платье'),
        ('accessory', 'Аксессуар'),
    ]
    
    # Автоматически генерируемый ID
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Название товара")
    category = models.CharField(max_length=255, verbose_name="Категория")
    subcategory = models.CharField(max_length=50, choices=SUBCATEGORY_CHOICES, blank=True, verbose_name="Подкатегория")
    brand = models.CharField(max_length=255, blank=True, verbose_name="Бренд")
    description = models.TextField(blank=True, verbose_name="Описание")
    summary = models.TextField(blank=True, verbose_name="Краткое описание для корзины")
    
    # Цены
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена (₽)")
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Старая цена (₽)")
    discount_percent = models.IntegerField(default=0, verbose_name="Скидка (%)")
    
    # Размеры
    size = models.CharField(max_length=50, verbose_name="Общий размер")
    size_type = models.CharField(max_length=20, choices=SIZE_TYPE_CHOICES, default='clothing', verbose_name="Тип размера")
    size_clothing = models.CharField(max_length=10, blank=True, verbose_name="Размер одежды (S, M, L, XL)")
    size_pants = models.CharField(max_length=10, blank=True, verbose_name="Размер штанов")
    size_shoes_eu = models.IntegerField(null=True, blank=True, verbose_name="EU размер обуви")
    color = models.CharField(max_length=255, blank=True, verbose_name="Цвет")
    
    # Мастер
    master = models.ForeignKey('Artist', on_delete=models.CASCADE, verbose_name="Мастер")
    master_telegram = models.CharField(max_length=255, blank=True, verbose_name="Telegram мастера")
    
    # Медиа
    avatar = models.TextField(blank=True, verbose_name="Главная фото товара")
    gallery = models.JSONField(default=list, verbose_name="Галерея товара")
    
    # Временные поля для HTTPS ссылок (пока MinIO не настроен)
    avatar_https = models.URLField(blank=True, verbose_name="HTTPS ссылка на аватар товара")
    gallery_https_1 = models.URLField(blank=True, verbose_name="HTTPS ссылка на фото товара 1")
    gallery_https_2 = models.URLField(blank=True, verbose_name="HTTPS ссылка на фото товара 2")
    gallery_https_3 = models.URLField(blank=True, verbose_name="HTTPS ссылка на фото товара 3")
    gallery_https_4 = models.URLField(blank=True, verbose_name="HTTPS ссылка на фото товара 4")
    gallery_https_5 = models.URLField(blank=True, verbose_name="HTTPS ссылка на фото товара 5")
    gallery_https_6 = models.URLField(blank=True, verbose_name="HTTPS ссылка на фото товара 6")
    gallery_https_7 = models.URLField(blank=True, verbose_name="HTTPS ссылка на фото товара 7")
    
    # Статус
    is_new = models.BooleanField(default=False, verbose_name="Новинка")
    is_available = models.BooleanField(default=True, verbose_name="Доступен")
    
    # Системная информация
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.name} - {self.price}₽"
    
    def get_display_size(self):
        """Получение отображаемого размера"""
        if self.size_type == 'clothing' and self.size_clothing:
            return self.size_clothing
        elif self.size_type == 'shoes' and self.size_shoes_eu:
            return f"EU {self.size_shoes_eu}"
        elif self.size_type == 'one_size':
            return "One Size"
        return self.size or "Не указан"
    
    def get_final_price(self):
        """Получение финальной цены со скидкой"""
        if self.discount_percent > 0:
            return self.price * (1 - self.discount_percent / 100)
        return self.price
    
    def get_gallery_urls(self):
        """Получение URL галереи из связанной таблицы"""
        try:
            # Если есть данные в JSON поле, используем их
            if self.gallery and isinstance(self.gallery, list):
                return self.gallery
            
            # Иначе пытаемся получить из связанной таблицы
            # (если она существует в базе данных)
            return []
        except:
            return []
    
    def update_gallery_from_db(self):
        """Обновление галереи из связанной таблицы product_gallery"""
        try:
            # Здесь можно добавить логику для получения галереи из product_gallery
            # Пока возвращаем пустой список
            return []
        except:
            return []
    
    def get_master_name(self):
        """Получение имени мастера"""
        return self.master.name if self.master else ""
    
    def get_master_id(self):
        """Получение ID мастера"""
        return str(self.master.id) if self.master else ""
    
    def get_formatted_price(self):
        """Получение форматированной цены"""
        return f"{self.get_final_price():.0f} ₽"
    
    def get_formatted_old_price(self):
        """Получение форматированной старой цены"""
        if self.old_price:
            return f"{self.old_price:.0f} ₽"
        return ""
    
    def get_avatar_url(self):
        """Получить URL аватара товара (приоритет HTTPS ссылке)"""
        return self.avatar_https if self.avatar_https else self.avatar
    
    def get_gallery_urls(self):
        """Получить список URL галереи товара из HTTPS полей"""
        urls = []
        for i in range(1, 8):
            field_name = f'gallery_https_{i}'
            url = getattr(self, field_name, '')
            if url:
                urls.append(url)
        return urls
    
    def get_gallery_count(self):
        """Получить количество фото в галерее товара"""
        return len(self.get_gallery_urls())

class SubscriptionChannel(models.Model):
    channel_username = models.CharField(max_length=200, unique=True)
    channel_name = models.CharField(max_length=200)
    channel_description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    required_for_giveaway = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'subscription_channels'

    def __str__(self):
        return self.channel_name

class Giveaway(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активен'),
        ('paused', 'Остановлен'),
        ('finished', 'Завершен'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    prize = models.CharField(max_length=200)
    telegram_folder = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    max_participants = models.IntegerField(default=1000)
    current_participants = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    auto_winner = models.BooleanField(default=True)
    # Новое поле для активации кнопки "Перейти в приложение"
    app_button_enabled = models.BooleanField(default=True, verbose_name="Кнопка 'Перейти в приложение' активна")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'giveaways'

    def __str__(self):
        return self.name

# Новые модели для системы билетов
class FolderSubscriptionTicket(models.Model):
    user_id = models.BigIntegerField(verbose_name="ID пользователя")
    is_subscribed = models.BooleanField(default=False, verbose_name="Подписан на папку")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        db_table = 'folder_subscription_tickets'
        verbose_name = "Билет за подписку на папку"
        verbose_name_plural = "Билеты за подписку на папку"
        unique_together = ('user_id',)

    def __str__(self):
        return f"Пользователь {self.user_id} - {'Подписан' if self.is_subscribed else 'Не подписан'}"

class ReferralTicket(models.Model):
    user_id = models.BigIntegerField(verbose_name="ID пользователя")
    referred_user_id = models.BigIntegerField(verbose_name="ID приглашенного пользователя")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")

    class Meta:
        db_table = 'referral_tickets'
        verbose_name = "Билет за реферала"
        verbose_name_plural = "Билеты за рефералов"
        unique_together = ('user_id', 'referred_user_id')

    def __str__(self):
        return f"Пользователь {self.user_id} пригласил {self.referred_user_id}"

class GiveawaySubscriptionChannel(models.Model):
    channel_id = models.BigIntegerField(unique=True, verbose_name="ID канала")
    channel_username = models.CharField(max_length=200, verbose_name="Username канала")
    channel_name = models.CharField(max_length=200, verbose_name="Название канала")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    order_index = models.IntegerField(default=0, verbose_name="Порядок сортировки")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")

    class Meta:
        db_table = 'giveaway_subscription_channels'
        verbose_name = "Канал подписки для розыгрыша"
        verbose_name_plural = "Каналы подписки для розыгрыша"
        ordering = ('order_index',)

    def __str__(self):
        return f"{self.channel_name} (@{self.channel_username})"

class GiveawaySubscriptionClick(models.Model):
    user_id = models.BigIntegerField(verbose_name="ID пользователя")
    clicked_at = models.DateTimeField(default=timezone.now, verbose_name="Дата клика")
    is_verified = models.BooleanField(default=False, verbose_name="Проверена подписка")
    verified_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата проверки")

    class Meta:
        db_table = 'giveaway_subscription_clicks'
        verbose_name = "Клик по подписке на розыгрыш"
        verbose_name_plural = "Клики по подписке на розыгрыш"

    def __str__(self):
        return f"Пользователь {self.user_id} - {'Проверен' if self.is_verified else 'Не проверен'}"

class GiveawayResult(models.Model):
    giveaway_id = models.IntegerField(verbose_name="ID розыгрыша")
    place_number = models.IntegerField(verbose_name="Место")
    prize_name = models.CharField(max_length=200, verbose_name="Название приза")
    prize_value = models.CharField(max_length=200, verbose_name="Стоимость приза")
    winner_user_id = models.BigIntegerField(null=True, blank=True, verbose_name="ID победителя")
    winner_username = models.CharField(max_length=100, null=True, blank=True, verbose_name="Username победителя")
    winner_first_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Имя победителя")
    is_manual_winner = models.BooleanField(default=False, verbose_name="Ручной выбор победителя")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")

    class Meta:
        db_table = 'giveaway_results'
        verbose_name = "Результат розыгрыша"
        verbose_name_plural = "Результаты розыгрыша"
        unique_together = ('giveaway_id', 'place_number')

    def __str__(self):
        return f"Розыгрыш {self.giveaway_id} - {self.place_number} место: {self.prize_name}"
