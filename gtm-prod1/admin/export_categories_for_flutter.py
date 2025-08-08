#!/usr/bin/env python3
"""
Скрипт для экспорта категорий в JSON формат для Flutter приложения
"""

import os
import sys
import json
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gtm_admin_panel.settings')
django.setup()

from admin_panel.models import Category

def export_categories_for_flutter():
    """
    Экспортирует категории в JSON формат для Flutter
    """
    
    # Получаем все категории
    categories = Category.objects.all().order_by('type', 'name')
    
    # Группируем по типу
    products = []
    services = []
    all_categories = []
    
    for category in categories:
        cat_data = {
            'id': category.id,
            'name': category.name,
            'type': category.type,
            'type_display': category.get_type_display(),
            'created_at': category.created_at.isoformat() if category.created_at else None
        }
        
        all_categories.append(cat_data)
        
        if category.type == 'product':
            products.append(cat_data)
        else:
            services.append(cat_data)
    
    # Создаем структуру данных как в Flutter
    flutter_data = {
        'categories': [cat['name'] for cat in all_categories],
        'product_categories': [cat['name'] for cat in products],
        'service_categories': [cat['name'] for cat in services],
        'detailed_categories': {
            'products': products,
            'services': services,
            'all': all_categories
        }
    }
    
    # Сохраняем в JSON файл
    output_file = 'categories_for_flutter.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(flutter_data, f, ensure_ascii=False, indent=2)
    
    print(f"📁 Категории экспортированы в файл: {output_file}")
    print(f"📊 Статистика:")
    print(f"   • Всего категорий: {len(all_categories)}")
    print(f"   • Товары: {len(products)}")
    print(f"   • Услуги: {len(services)}")
    
    print(f"\n📋 Категории товаров:")
    for cat in products:
        print(f"   • {cat['name']}")
    
    print(f"\n📋 Категории услуг:")
    for cat in services:
        print(f"   • {cat['name']}")
    
    # Создаем Dart код для Flutter
    dart_code = generate_dart_code(flutter_data)
    dart_file = 'categories_dart.dart'
    with open(dart_file, 'w', encoding='utf-8') as f:
        f.write(dart_code)
    
    print(f"\n📁 Dart код сохранен в файл: {dart_file}")
    
    return flutter_data

def generate_dart_code(data):
    """
    Генерирует Dart код для Flutter приложения
    """
    categories_list = ',\n    '.join([f"'{cat}'" for cat in data['categories']])
    product_categories_list = ',\n    '.join([f"'{cat}'" for cat in data['product_categories']])
    service_categories_list = ',\n    '.join([f"'{cat}'" for cat in data['service_categories']])
    
    dart_code = f'''// Автоматически сгенерированный код категорий
// Обновлен: {django.utils.timezone.now().strftime('%Y-%m-%d %H:%M:%S')}

class MasterCloudCategories {{
  // Все категории
  static const List<String> categories = [
    {categories_list}
  ];

  // Категории товаров (для перехода на product screen)
  static const List<String> productCategories = [
    {product_categories_list}
  ];

  // Категории услуг (для перехода на master detail screen)
  static const List<String> serviceCategories = [
    {service_categories_list}
  ];
  
  // Проверка, является ли категория товарной
  static bool isProductCategory(String category) {{
    return productCategories.contains(category);
  }}
  
  // Проверка, является ли категория услугой
  static bool isServiceCategory(String category) {{
    return serviceCategories.contains(category);
  }}
  
  // Получение типа категории
  static String getCategoryType(String category) {{
    if (isProductCategory(category)) {{
      return 'product';
    }} else if (isServiceCategory(category)) {{
      return 'service';
    }}
    return 'unknown';
  }}
}}
'''
    
    return dart_code

if __name__ == "__main__":
    try:
        export_categories_for_flutter()
        print("\n🎉 Экспорт завершен успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка при экспорте: {e}")
        sys.exit(1) 