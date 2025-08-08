from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from django.shortcuts import render
from django.contrib import messages
from django.core.files.uploadedfile import UploadedFile
import requests
import json
from .models import (
    User, Artist, City, Giveaway, Product, SubscriptionChannel, 
    TaskCompletion, ReferralInvite, GiveawayChannel, Category,
    ArtistCategory, ArtistCity, ArtistLinks, FolderSubscriptionTicket,
    ReferralTicket, GiveawaySubscriptionChannel, GiveawaySubscriptionClick,
    GiveawayResult
)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'first_name', 'last_name', 'registered_at', 'last_activity')
    list_filter = ('registered_at', 'last_activity')
    search_fields = ('username', 'first_name', 'last_name')
    readonly_fields = ('user_id', 'registered_at')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbr', 'size', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'abbr')
    ordering = ('name',)

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'folder_name', 'get_categories', 'get_cities', 'get_https_avatar_status', 'get_https_gallery_status', 'created_at')
    list_filter = ('categories', 'cities', 'created_at')
    
    def get_queryset(self, request):
        """Добавляем аннотации для фильтрации по HTTPS статусу"""
        qs = super().get_queryset(request)
        return qs
    search_fields = ('name', 'folder_name', 'bio')
    readonly_fields = ('created_at', 'updated_at', 'folder_name')
    change_list_template = 'admin/artist_file_upload.html'
    
    actions = ['mark_as_https_ready', 'clear_https_links']
    
    def mark_as_https_ready(self, request, queryset):
        """Пометить артистов как готовых к HTTPS"""
        count = queryset.count()
        self.message_user(request, f'{count} артистов помечены как готовые к HTTPS')
    mark_as_https_ready.short_description = "Пометить как готовые к HTTPS"
    
    def clear_https_links(self, request, queryset):
        """Очистить HTTPS ссылки"""
        count = queryset.count()
        queryset.update(
            avatar_https='',
            gallery_https_1='', gallery_https_2='', gallery_https_3='', gallery_https_4='', gallery_https_5='',
            gallery_https_6='', gallery_https_7='', gallery_https_8='', gallery_https_9='', gallery_https_10=''
        )
        self.message_user(request, f'HTTPS ссылки очищены у {count} артистов')
    clear_https_links.short_description = "Очистить HTTPS ссылки"
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'bio', 'avatar_url', 'folder_name')
        }),
        ('HTTPS ссылки на изображения (временное решение)', {
            'fields': (
                'avatar_https',
                'gallery_https_1', 'gallery_https_2', 'gallery_https_3', 'gallery_https_4', 'gallery_https_5',
                'gallery_https_6', 'gallery_https_7', 'gallery_https_8', 'gallery_https_9', 'gallery_https_10'
            ),
            'description': 'Вставьте HTTPS ссылки на изображения из публичного S3 бакета. Приоритет отдается HTTPS ссылкам. Порядок: Аватар → Фото 1-10.'
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_categories(self, obj):
        return ', '.join([cat.name for cat in obj.categories.all()]) if obj.categories.exists() else '-'
    get_categories.short_description = 'Категории'
    
    def get_cities(self, obj):
        return ', '.join([city.name for city in obj.cities.all()]) if obj.cities.exists() else '-'
    get_cities.short_description = 'Города'
    
    def get_https_avatar_status(self, obj):
        """Показывает статус HTTPS аватара"""
        if obj.avatar_https:
            return '✅ HTTPS'
        elif obj.avatar_url:
            return '⚠️ Старый'
        return '❌ Нет'
    get_https_avatar_status.short_description = 'Аватар'
    
    def get_https_gallery_status(self, obj):
        """Показывает количество HTTPS фото в галерее"""
        count = obj.get_gallery_count()
        if count > 0:
            return f'✅ {count} фото'
        return '❌ Нет фото'
    get_https_gallery_status.short_description = 'Галерея'
    
    def save_model(self, request, obj, form, change):
        # Автоматически генерируем folder_name если его нет
        if not obj.folder_name:
            if obj.pk:
                obj.folder_name = f"id{obj.pk:06d}"
            else:
                # Сохраняем чтобы получить ID
                super().save_model(request, obj, form, change)
                obj.folder_name = f"id{obj.pk:06d}"
        
        super().save_model(request, obj, form, change)
        
        # Создаем папку в MinIO
        try:
            response = requests.post(
                'http://localhost:3001/api/admin/artists',
                json={'name': obj.name, 'bio': obj.bio},
                headers={'Content-Type': 'application/json'}
            )
            if response.status_code == 201:
                messages.success(request, f'Папка артиста создана в MinIO: {obj.folder_name}')
        except Exception as e:
            messages.warning(request, f'Ошибка создания папки в MinIO: {e}')
    
    def get_urls(self):
        from django.urls import URLPattern, path
        urls = super().get_urls()
        custom_urls = [
            path('upload-avatar/<int:artist_id>/', self.upload_avatar, name='upload_avatar'),
            path('upload-gallery/<int:artist_id>/', self.upload_gallery, name='upload_gallery'),
        ]
        return custom_urls + urls
    
    def upload_avatar(self, request, artist_id):
        if request.method == 'POST':
            try:
                artist = Artist.objects.get(id=artist_id)
                file = request.FILES.get('avatar')
                
                if file:
                    # Загружаем в MinIO через API
                    files = {'file': file}
                    response = requests.post(
                        f'http://localhost:3001/api/admin/artists/{artist_id}/avatar',
                        files=files
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        artist.avatar_url = data['avatar_url']
                        artist.save()
                        messages.success(request, 'Аватар успешно загружен')
                    else:
                        messages.error(request, 'Ошибка загрузки аватара')
                
            except Artist.DoesNotExist:
                messages.error(request, 'Артист не найден')
            except Exception as e:
                messages.error(request, f'Ошибка: {e}')
        
        return HttpResponseRedirect('../')
    
    def upload_gallery(self, request, artist_id):
        if request.method == 'POST':
            try:
                artist = Artist.objects.get(id=artist_id)
                files = request.FILES.getlist('gallery')
                
                for i, file in enumerate(files, 1):
                    if file:
                        # Загружаем в MinIO через API
                        files_data = {'file': file, 'image_number': i}
                        response = requests.post(
                            f'http://localhost:3001/api/admin/artists/{artist_id}/gallery',
                            files=files_data
                        )
                        
                        if response.status_code == 200:
                            messages.success(request, f'Изображение {i} успешно загружено')
                        else:
                            messages.error(request, f'Ошибка загрузки изображения {i}')
                
            except Artist.DoesNotExist:
                messages.error(request, 'Артист не найден')
            except Exception as e:
                messages.error(request, f'Ошибка: {e}')
        
        return HttpResponseRedirect('../')

@admin.register(ArtistLinks)
class ArtistLinksAdmin(admin.ModelAdmin):
    list_display = ('artist', 'telegram', 'instagram', 'tiktok', 'updated_at')
    list_filter = ('updated_at',)
    search_fields = ('artist__name', 'telegram', 'instagram', 'tiktok')
    
    fieldsets = (
        ('Артист', {
            'fields': ('artist',)
        }),
        ('Социальные сети', {
            'fields': (
                'telegram', 'telegram_url',
                'instagram', 'tiktok', 'tiktok_url',
                'pinterest', 'pinterest_url', 'booking_url'
            ),
            'description': 'Instagram - Мета запрещена в РФ'
        }),
        ('Локация и галерея', {
            'fields': ('location_html', 'gallery_html')
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ArtistCategory)
class ArtistCategoryAdmin(admin.ModelAdmin):
    list_display = ('artist', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('artist__name', 'category__name')
    ordering = ('artist__name', 'category__name')

@admin.register(ArtistCity)
class ArtistCityAdmin(admin.ModelAdmin):
    list_display = ('artist', 'city', 'created_at')
    list_filter = ('city', 'created_at')
    search_fields = ('artist__name', 'city__name')
    ordering = ('artist__name', 'city__name')

@admin.register(Giveaway)
class GiveawayAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'current_participants', 'max_participants', 'start_date', 'end_date', 'get_telegram_folder_link', 'app_button_enabled')
    list_filter = ('status', 'start_date', 'end_date', 'app_button_enabled')
    search_fields = ('name', 'prize', 'telegram_folder')
    readonly_fields = ('created_at', 'updated_at', 'current_participants')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'prize'),
            'description': 'Название розыгрыша, описание и приз'
        }),
        ('Telegram папка', {
            'fields': ('telegram_folder',),
            'description': 'Ссылка на Telegram папку с каналами для подписки. Эта ссылка будет отображаться в Flutter приложении.'
        }),
        ('Временные рамки', {
            'fields': ('start_date', 'end_date'),
            'description': 'Дата и время начала и окончания розыгрыша (UTC+3 по московскому времени)'
        }),
        ('Участники', {
            'fields': ('max_participants', 'current_participants'),
            'description': 'Максимальное количество участников и текущее количество'
        }),
        ('Статус и настройки', {
            'fields': ('status', 'auto_winner', 'app_button_enabled'),
            'description': 'Статус розыгрыша, автоматический выбор победителей и активация кнопки "Перейти в приложение"'
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_telegram_folder_link(self, obj):
        """Отображение ссылки на Telegram папку"""
        if obj.telegram_folder:
            return f'<a href="{obj.telegram_folder}" target="_blank">Открыть папку</a>'
        return 'Не указана'
    get_telegram_folder_link.short_description = 'Telegram папка'
    get_telegram_folder_link.allow_tags = True

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'subcategory', 'brand', 'price', 'get_final_price', 'get_display_size', 'get_master_name', 'get_https_avatar_status', 'get_https_gallery_status', 'is_available', 'is_new', 'created_at')
    list_filter = ('category', 'subcategory', 'brand', 'size_type', 'is_available', 'is_new', 'created_at')
    search_fields = ('name', 'description', 'brand', 'master__name')
    readonly_fields = ('created_at', 'updated_at')
    
    actions = ['mark_as_https_ready', 'clear_https_links']
    
    def mark_as_https_ready(self, request, queryset):
        """Пометить товары как готовые к HTTPS"""
        count = queryset.count()
        self.message_user(request, f'{count} товаров помечены как готовые к HTTPS')
    mark_as_https_ready.short_description = "Пометить как готовые к HTTPS"
    
    def clear_https_links(self, request, queryset):
        """Очистить HTTPS ссылки товаров"""
        count = queryset.count()
        queryset.update(
            avatar_https='',
            gallery_https_1='', gallery_https_2='', gallery_https_3='', gallery_https_4='', 
            gallery_https_5='', gallery_https_6='', gallery_https_7=''
        )
        self.message_user(request, f'HTTPS ссылки очищены у {count} товаров')
    clear_https_links.short_description = "Очистить HTTPS ссылки"
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'category', 'subcategory', 'brand', 'description', 'summary'),
            'description': 'ID генерируется автоматически. Краткое описание для корзины - короткое описание товара для отображения в корзине.'
        }),
        ('Цены и скидки', {
            'fields': ('price', 'old_price', 'discount_percent'),
            'description': 'Цены указываются в рублях (₽)'
        }),
        ('Размеры', {
            'fields': ('size_type', 'size_clothing', 'size_pants', 'size_shoes_eu', 'size', 'color'),
            'description': 'Выберите тип размера и заполните соответствующие поля'
        }),
        ('Мастер', {
            'fields': ('master', 'master_telegram'),
            'description': 'Выберите мастера из списка. При выборе мастера его аватар будет отображаться в Master Cloud Screen.'
        }),
        ('Медиа', {
            'fields': ('avatar', 'gallery'),
            'description': 'Галерея: укажите список URL изображений в формате JSON ["url1", "url2"]. Можно загрузить до 7 изображений.'
        }),
        ('HTTPS ссылки на изображения товара (временное решение)', {
            'fields': (
                'avatar_https',
                'gallery_https_1', 'gallery_https_2', 'gallery_https_3', 'gallery_https_4', 
                'gallery_https_5', 'gallery_https_6', 'gallery_https_7'
            ),
            'description': 'Вставьте HTTPS ссылки на изображения товара из публичного S3 бакета. Приоритет отдается HTTPS ссылкам. Порядок: Аватар товара → Фото товара 1-7.'
        }),
        ('Статус', {
            'fields': ('is_new', 'is_available')
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_final_price(self, obj):
        """Отображение финальной цены со скидкой"""
        if obj.discount_percent > 0:
            final_price = obj.price * (1 - obj.discount_percent / 100)
            return f"{final_price:.2f}₽ (-{obj.discount_percent}%)"
        return f"{obj.price}₽"
    get_final_price.short_description = 'Финальная цена'
    
    def get_display_size(self, obj):
        """Отображение размера"""
        return obj.get_display_size()
    get_display_size.short_description = 'Размер'
    
    def get_master_name(self, obj):
        """Отображение имени мастера"""
        return obj.get_master_name()
    get_master_name.short_description = 'Мастер'
    
    def get_https_avatar_status(self, obj):
        """Показывает статус HTTPS аватара товара"""
        if obj.avatar_https:
            return '✅ HTTPS'
        elif obj.avatar:
            return '⚠️ Старый'
        return '❌ Нет'
    get_https_avatar_status.short_description = 'Аватар товара'
    
    def get_https_gallery_status(self, obj):
        """Показывает количество HTTPS фото в галерее товара"""
        count = obj.get_gallery_count()
        if count > 0:
            return f'✅ {count} фото'
        return '❌ Нет фото'
    get_https_gallery_status.short_description = 'Галерея товара'

@admin.register(SubscriptionChannel)
class SubscriptionChannelAdmin(admin.ModelAdmin):
    list_display = ('channel_name', 'channel_username', 'is_active', 'required_for_giveaway', 'created_at')
    list_filter = ('is_active', 'required_for_giveaway', 'created_at')
    search_fields = ('channel_name', 'channel_username')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('channel_name', 'channel_username', 'channel_description'),
            'description': 'Название канала, username и описание'
        }),
        ('Настройки', {
            'fields': ('is_active', 'required_for_giveaway'),
            'description': 'Активен ли канал и требуется ли для участия в розыгрыше'
        }),
        ('Системная информация', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at',)

@admin.register(TaskCompletion)
class TaskCompletionAdmin(admin.ModelAdmin):
    list_display = ('user', 'task_name', 'task_number', 'completed_at')
    list_filter = ('task_name', 'completed_at')
    search_fields = ('user__username', 'task_name')

@admin.register(ReferralInvite)
class ReferralInviteAdmin(admin.ModelAdmin):
    list_display = ('inviter', 'invitee_username', 'status', 'invited_at')
    list_filter = ('status', 'invited_at')
    search_fields = ('inviter__username', 'invitee_username')

@admin.register(GiveawayChannel)
class GiveawayChannelAdmin(admin.ModelAdmin):
    list_display = ('channel_name', 'channel_id', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('channel_name',)

@admin.register(GiveawaySubscriptionChannel)
class GiveawaySubscriptionChannelAdmin(admin.ModelAdmin):
    list_display = ('channel_name', 'channel_username', 'channel_id', 'is_active', 'order_index', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('channel_name', 'channel_username')
    ordering = ('order_index',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('channel_name', 'channel_username', 'channel_id'),
            'description': 'Название канала, username и ID канала'
        }),
        ('Настройки', {
            'fields': ('is_active', 'order_index'),
            'description': 'Активен ли канал и порядок сортировки'
        }),
        ('Системная информация', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at',)

@admin.register(FolderSubscriptionTicket)
class FolderSubscriptionTicketAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'is_subscribed', 'created_at', 'updated_at')
    list_filter = ('is_subscribed', 'created_at', 'updated_at')
    search_fields = ('user_id',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ReferralTicket)
class ReferralTicketAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'referred_user_id', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user_id', 'referred_user_id')
    readonly_fields = ('created_at',)

@admin.register(GiveawaySubscriptionClick)
class GiveawaySubscriptionClickAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'clicked_at', 'is_verified', 'verified_at')
    list_filter = ('is_verified', 'clicked_at', 'verified_at')
    search_fields = ('user_id',)
    readonly_fields = ('clicked_at', 'verified_at')

@admin.register(GiveawayResult)
class GiveawayResultAdmin(admin.ModelAdmin):
    list_display = ('giveaway_id', 'place_number', 'prize_name', 'prize_value', 'winner_username', 'is_manual_winner', 'created_at')
    list_filter = ('giveaway_id', 'place_number', 'is_manual_winner', 'created_at')
    search_fields = ('prize_name', 'winner_username', 'winner_first_name')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('giveaway_id', 'place_number', 'prize_name', 'prize_value'),
            'description': 'ID розыгрыша, место, название и стоимость приза'
        }),
        ('Победитель', {
            'fields': ('winner_user_id', 'winner_username', 'winner_first_name', 'is_manual_winner'),
            'description': 'Информация о победителе. Для 1 места можно указать победителя вручную.'
        }),
        ('Системная информация', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
