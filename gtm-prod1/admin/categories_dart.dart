// Автоматически сгенерированный код категорий
// Обновлен: 2025-08-05 12:13:20

class MasterCloudCategories {
  // Все категории
  static const List<String> categories = [
    'Accessories',
    'Clothing',
    'Cosmetics',
    'Custom',
    'GTM BRAND',
    'Jewelry',
    'Second',
    'Shoes',
    'Beauty',
    'Fashion',
    'Fitness',
    'Hair',
    'Makeup',
    'Massage',
    'Nails',
    'Photography',
    'Piercing',
    'Tattoo',
    'Косметология',
    'Маникюр',
    'Пирсинг',
    'Татуировки'
  ];

  // Категории товаров (для перехода на product screen)
  static const List<String> productCategories = [
    'Accessories',
    'Clothing',
    'Cosmetics',
    'Custom',
    'GTM BRAND',
    'Jewelry',
    'Second',
    'Shoes'
  ];

  // Категории услуг (для перехода на master detail screen)
  static const List<String> serviceCategories = [
    'Beauty',
    'Fashion',
    'Fitness',
    'Hair',
    'Makeup',
    'Massage',
    'Nails',
    'Photography',
    'Piercing',
    'Tattoo',
    'Косметология',
    'Маникюр',
    'Пирсинг',
    'Татуировки'
  ];
  
  // Проверка, является ли категория товарной
  static bool isProductCategory(String category) {
    return productCategories.contains(category);
  }
  
  // Проверка, является ли категория услугой
  static bool isServiceCategory(String category) {
    return serviceCategories.contains(category);
  }
  
  // Получение типа категории
  static String getCategoryType(String category) {
    if (isProductCategory(category)) {
      return 'product';
    } else if (isServiceCategory(category)) {
      return 'service';
    }
    return 'unknown';
  }
}
