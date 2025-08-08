from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('telegram-links/', views.telegram_links, name='telegram_links'),
    path('artists/', views.artists, name='artists'),
    path('cities/', views.cities, name='cities'),
    path('giveaway/', views.giveaway, name='giveaway'),
    path('file-manager/', views.file_manager, name='file_manager'),
    path('system-status/', views.system_status, name='system_status'),
    
    # API endpoints
    path('api/system-status/', views.api_system_status, name='api_system_status'),
    path('api/telegram-links/', views.api_telegram_links, name='api_telegram_links'),
    path('api/artists/', views.api_artists, name='api_artists'),
    path('api/artists-with-images/', views.api_artists_with_images, name='api_artists_with_images'),
    path('api/cities/', views.api_cities, name='api_cities'),
    path('api/categories/', views.api_categories, name='api_categories'),
    path('api/giveaway-telegram/', views.api_giveaway_telegram, name='api_giveaway_telegram'),
    path('api/admin/analytics/', views.api_admin_analytics, name='api_admin_analytics'),
    path('api/users/', views.api_users, name='api_users'),
    path('api/products/', views.api_products, name='api_products'),
    path('api/products/master/<int:master_id>/category/<str:category>/', views.api_products_by_master_and_category, name='api_products_by_master_and_category'),
    
    # CRUD операции для артистов
    path('api/artists/create/', views.api_create_artist, name='api_create_artist'),
    path('api/artists/<int:artist_id>/update/', views.api_update_artist, name='api_update_artist'),
    path('api/artists/<int:artist_id>/delete/', views.api_delete_artist, name='api_delete_artist'),
] 