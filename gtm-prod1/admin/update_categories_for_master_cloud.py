#!/usr/bin/env python3
"""
Скрипт для обновления категорий в Django админ панели
Оставляет только 8 основных категорий для Master Cloud Screen
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gtm_admin_panel.settings')
django.setup()

from admin_panel.models import Category, Artist, Product, City
from django.utils import timezone

def update_categories_for_master_cloud():
    """Обновление категорий для Master Cloud Screen"""
    print("🔄 Обновление категорий для Master Cloud Screen...")
    
    # 8 основных категорий для Master Cloud Screen
    master_cloud_categories = [
        # Продуктовые категории (4 штуки)
        {'name': 'GTM BRAND', 'type': 'product'},
        {'name': 'Jewelry', 'type': 'product'},
        {'name': 'Custom', 'type': 'product'},
        {'name': 'Second', 'type': 'product'},
        
        # Сервисные категории (4 штуки)
        {'name': 'Tattoo', 'type': 'service'},
        {'name': 'Hair', 'type': 'service'},
        {'name': 'Nails', 'type': 'service'},
        {'name': 'Piercing', 'type': 'service'},
    ]
    
    print(f"📋 Основных категорий: {len(master_cloud_categories)}")
    
    # Получаем все существующие категории
    all_categories = Category.objects.all()
    print(f"📊 Всего категорий в БД: {all_categories.count()}")
    
    # Активируем нужные категории
    for cat_data in master_cloud_categories:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'type': cat_data['type'],
                'is_active': True,
                'created_at': timezone.now()
            }
        )
        
        if created:
            print(f"✅ Создана категория: {category.name} ({category.get_type_display()})")
        else:
            # Обновляем существующую категорию
            category.type = cat_data['type']
            category.is_active = True
            category.save()
            print(f"ℹ️  Категория уже существует: {category.name} ({category.get_type_display()})")
    
    # Деактивируем остальные категории
    categories_to_deactivate = Category.objects.exclude(
        name__in=[cat['name'] for cat in master_cloud_categories]
    )
    
    print(f"📋 Деактивируем остальные категории:")
    deactivated_count = 0
    for category in categories_to_deactivate:
        category.is_active = False
        category.save()
        print(f"   • {category.name} ({category.get_type_display()}) - ДЕАКТИВИРОВАНА")
        deactivated_count += 1
    
    print(f"✅ Деактивировано категорий: {deactivated_count}")
    
    # Выводим результаты
    active_categories = Category.objects.filter(is_active=True)
    inactive_categories = Category.objects.filter(is_active=False)
    
    print(f"📊 Результаты обновления:")
    print(f"   ✅ Активных категорий: {active_categories.count()}")
    print(f"   📋 Деактивированных: {inactive_categories.count()}")
    
    print(f"📋 Активные категории для Master Cloud Screen:")
    for category in active_categories.order_by('type', 'name'):
        print(f"   • {category.name} ({category.get_type_display()})")
    
    return active_categories

def create_sample_artists():
    """Создание примеров артистов с категориями"""
    print("🔄 Создание примеров артистов с категориями...")
    
    # Получаем активные категории
    active_categories = Category.objects.filter(is_active=True)
    
    # Примеры артистов
    sample_artists = [
        {
            'name': 'EMI',
            'bio': 'Профессиональный тату-мастер с 5-летним опытом. Специализируется на реалистичных татуировках и минимализме.',
            'categories': ['Tattoo', 'Second'],
            'cities': ['Москва']
        },
        {
            'name': 'Alena',
            'bio': 'Мастер по маникюру и педикюру. Создаю уникальные дизайны ногтей для любого случая.',
            'categories': ['Nails', 'Custom'],
            'cities': ['Москва']
        },
        {
            'name': 'Lin++',
            'bio': 'Стилист-парикмахер. Создаю индивидуальные образы и укладки для любого типа волос.',
            'categories': ['Hair', 'GTM BRAND'],
            'cities': ['Москва']
        }
    ]
    
    for artist_data in sample_artists:
        try:
            # Проверяем, существует ли артист
            artist = Artist.objects.filter(name=artist_data['name']).first()
            
            if artist:
                # Обновляем существующего артиста
                artist.bio = artist_data['bio']
                artist.save()
                print(f"ℹ️  Обновлен артист: {artist.name}")
            else:
                # Создаем нового артиста
                artist = Artist.objects.create(
                    name=artist_data['name'],
                    bio=artist_data['bio'],
                    avatar_url=f'https://gtm.baby/avatars/{artist_data["name"].lower()}.jpg',
                    created_at=timezone.now()
                )
                print(f"✅ Создан артист: {artist.name}")
            
            # Очищаем существующие категории и добавляем новые
            artist.categories.clear()
            for cat_name in artist_data['categories']:
                try:
                    category = Category.objects.get(name=cat_name, is_active=True)
                    artist.categories.add(category)
                    print(f"   📋 Добавлена категория: {category.name}")
                except Category.DoesNotExist:
                    print(f"   ❌ Категория не найдена: {cat_name}")
            
            # Очищаем существующие города и добавляем новые
            artist.cities.clear()
            for city_name in artist_data['cities']:
                try:
                    city = City.objects.get(name=city_name)
                    artist.cities.add(city)
                    print(f"   🏙️  Добавлен город: {city.name}")
                except City.DoesNotExist:
                    print(f"   ❌ Город не найден: {city_name}")
                    
        except Exception as e:
            print(f"❌ Ошибка при обновлении: {e}")

if __name__ == '__main__':
    try:
        # Обновляем категории
        active_categories = update_categories_for_master_cloud()
        
        # Создаем примеры артистов
        create_sample_artists()
        
        print("\n✅ Обновление завершено успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        sys.exit(1) 