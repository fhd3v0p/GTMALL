#!/usr/bin/env python3
"""
Скрипт для синхронизации категорий из Flutter приложения с Django админ панелью
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gtm_admin_panel.settings')
django.setup()

from admin_panel.models import Category

def sync_categories_from_flutter():
    """
    Синхронизирует категории из Flutter приложения с Django
    """
    
    # Категории из Flutter приложения (master_cloud_screen.dart)
    flutter_categories = [
        # Товары
        {'name': 'GTM BRAND', 'type': 'product'},
        {'name': 'Jewelry', 'type': 'product'},
        {'name': 'Custom', 'type': 'product'},
        {'name': 'Second', 'type': 'product'},
        
        # Услуги
        {'name': 'Tattoo', 'type': 'service'},
        {'name': 'Hair', 'type': 'service'},
        {'name': 'Nails', 'type': 'service'},
        {'name': 'Piercing', 'type': 'service'},
    ]
    
    print("🔄 Синхронизация категорий из Flutter приложения...")
    print(f"📋 Найдено категорий в Flutter: {len(flutter_categories)}")
    
    created_count = 0
    updated_count = 0
    existing_count = 0
    
    for cat_data in flutter_categories:
        name = cat_data['name']
        cat_type = cat_data['type']
        
        # Проверяем, существует ли категория
        category, created = Category.objects.get_or_create(
            name=name,
            defaults={
                'type': cat_type,
            }
        )
        
        if created:
            print(f"✅ Создана новая категория: {name} ({cat_type})")
            created_count += 1
        else:
            # Проверяем, нужно ли обновить тип
            if category.type != cat_type:
                category.type = cat_type
                category.save()
                print(f"🔄 Обновлена категория: {name} ({cat_type})")
                updated_count += 1
            else:
                print(f"ℹ️  Категория уже существует: {name} ({cat_type})")
                existing_count += 1
    
    print("\n📊 Результаты синхронизации:")
    print(f"   ✅ Создано новых: {created_count}")
    print(f"   🔄 Обновлено: {updated_count}")
    print(f"   ℹ️  Уже существовало: {existing_count}")
    print(f"   📈 Всего категорий: {Category.objects.count()}")
    
    # Показываем все категории
    print("\n📋 Все категории в системе:")
    for cat in Category.objects.all().order_by('type', 'name'):
        print(f"   • {cat.name} ({cat.get_type_display()})")
    
    return True

def create_additional_categories():
    """
    Создает дополнительные категории, которые могут понадобиться
    """
    additional_categories = [
        # Дополнительные товары
        {'name': 'Accessories', 'type': 'product'},
        {'name': 'Clothing', 'type': 'product'},
        {'name': 'Shoes', 'type': 'product'},
        
        # Дополнительные услуги
        {'name': 'Makeup', 'type': 'service'},
        {'name': 'Massage', 'type': 'service'},
        {'name': 'Fitness', 'type': 'service'},
        {'name': 'Beauty', 'type': 'service'},
    ]
    
    print("\n🔄 Создание дополнительных категорий...")
    
    for cat_data in additional_categories:
        name = cat_data['name']
        cat_type = cat_data['type']
        
        category, created = Category.objects.get_or_create(
            name=name,
            defaults={'type': cat_type}
        )
        
        if created:
            print(f"✅ Создана дополнительная категория: {name} ({cat_type})")
        else:
            print(f"ℹ️  Дополнительная категория уже существует: {name}")

if __name__ == "__main__":
    try:
        # Основная синхронизация
        sync_categories_from_flutter()
        
        # Создание дополнительных категорий (опционально)
        create_additional_categories()
        
        print("\n🎉 Синхронизация завершена успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка при синхронизации: {e}")
        sys.exit(1) 