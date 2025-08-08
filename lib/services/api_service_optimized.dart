import 'dart:convert';
import 'package:http/http.dart' as http;
import '../api_config.dart';
import '../models/master_model.dart';
import '../models/product_model.dart';

class ApiServiceOptimized {
  static String get baseUrl => ApiConfig.apiBaseUrl;
  
  // Кэширование (уменьшено до 1 минуты для быстрого обновления)
  static final Map<String, dynamic> _cache = {};
  static const Duration _cacheTimeout = Duration(minutes: 1); // Было 30 минут
  static final Map<String, DateTime> _cacheTimestamps = {};
  
  // Retry настройки
  static const int _maxRetries = 3;
  static const Duration _retryDelay = Duration(seconds: 2);
  
  // HTTP клиент с таймаутом
  static final http.Client _client = http.Client();
  
  /// Проверка актуальности кэша
  static bool _isCacheValid(String key) {
    final timestamp = _cacheTimestamps[key];
    if (timestamp == null) return false;
    return DateTime.now().difference(timestamp) < _cacheTimeout;
  }
  
  /// Очистка устаревшего кэша
  static void _cleanExpiredCache() {
    final now = DateTime.now();
    _cacheTimestamps.removeWhere((key, timestamp) {
      if (now.difference(timestamp) >= _cacheTimeout) {
        _cache.remove(key);
        return true;
      }
      return false;
    });
  }
  
  /// Принудительная очистка всего кэша
  static void clearAllCache() {
    _cache.clear();
    _cacheTimestamps.clear();
    print('DEBUG: Cache cleared');
  }
  
  /// Очистка кэша для конкретного товара
  static void clearProductCache(String productId) {
    final cacheKey = 'product:$productId';
    _cache.remove(cacheKey);
    _cacheTimestamps.remove(cacheKey);
    print('DEBUG: Product cache cleared for $productId');
  }
  
  /// HTTP запрос с retry логикой
  static Future<http.Response> _makeRequest(
    String url, {
    Map<String, String>? headers,
    Object? body,
    String method = 'GET',
  }) async {
    int attempts = 0;
    
    while (attempts < _maxRetries) {
      try {
        final uri = Uri.parse(url);
        final requestHeaders = {
          'Content-Type': 'application/json',
          ...?headers,
        };
        
        http.Response response;
        
        switch (method.toUpperCase()) {
          case 'GET':
            response = await _client.get(uri, headers: requestHeaders);
            break;
          case 'POST':
            response = await _client.post(
              uri,
              headers: requestHeaders,
              body: body,
            );
            break;
          case 'PUT':
            response = await _client.put(
              uri,
              headers: requestHeaders,
              body: body,
            );
            break;
          case 'DELETE':
            response = await _client.delete(uri, headers: requestHeaders);
            break;
          default:
            throw Exception('Unsupported HTTP method: $method');
        }
        
        return response;
      } catch (e) {
        attempts++;
        if (attempts >= _maxRetries) {
          throw Exception('Request failed after $_maxRetries attempts: $e');
        }
        await Future.delayed(_retryDelay * attempts);
      }
    }
    
    throw Exception('Request failed');
  }
  
  /// Получение всех мастеров с кэшированием
  static Future<List<MasterModel>> getMasters() async {
    const cacheKey = 'masters';
    
    // Очищаем устаревший кэш
    _cleanExpiredCache();
    
    // Проверяем кэш
    if (_cache.containsKey(cacheKey) && _isCacheValid(cacheKey)) {
      print('DEBUG: Using cached masters');
      return _cache[cacheKey];
    }
    
    try {
      print('DEBUG: Loading masters from API');
      final response = await _makeRequest('$baseUrl/masters');
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final masters = (data['masters'] as List)
            .map((m) => MasterModel.fromApiData(m))
            .toList();
        
        // Кэшируем результат
        _cache[cacheKey] = masters;
        _cacheTimestamps[cacheKey] = DateTime.now();
        
        print('DEBUG: Loaded ${masters.length} masters from API');
        return masters;
      } else {
        print('DEBUG: API returned status ${response.statusCode}');
        throw Exception('Failed to load masters: ${response.statusCode}');
      }
    } catch (e) {
      print('DEBUG: Error loading masters from API: $e');
      // Fallback на локальные данные
      return await _loadMastersFromAssets();
    }
  }
  
  /// Fallback загрузка мастеров из ассетов
  static Future<List<MasterModel>> _loadMastersFromAssets() async {
    print('DEBUG: Loading masters from assets');
    
    final artistFolders = [
      'assets/artists/Lin++',
      'assets/artists/Blodivamp',
      'assets/artists/Aspergill',
      'assets/artists/EMI',
      'assets/artists/naidi',
      'assets/artists/MurderDoll',
      'assets/artists/poteryua',
      'assets/artists/alena',
      'assets/artists/msk_tattoo_EMI',
      'assets/artists/msk_tattoo_Alena',
    ];
    
    final results = await Future.wait(
      artistFolders.map((folder) => MasterModel.fromArtistFolder(folder).catchError((e) {
        print('DEBUG: Error loading from $folder: $e');
        return null;
      })),
    );
    
    final masters = results.whereType<MasterModel>().toList();
    print('DEBUG: Loaded ${masters.length} masters from assets');
    
    return masters;
  }
  
  /// Получение рейтинга мастера
  static Future<RatingData?> getMasterRating(String masterId, String userId) async {
    final cacheKey = 'rating:$masterId:$userId';
    
    // Проверяем кэш
    if (_cache.containsKey(cacheKey) && _isCacheValid(cacheKey)) {
      return _cache[cacheKey];
    }
    
    try {
      final response = await _makeRequest(
        '$baseUrl/masters/$masterId/rating?user_id=$userId',
      );
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final ratingData = RatingData.fromJson(data);
        
        // Кэшируем результат
        _cache[cacheKey] = ratingData;
        _cacheTimestamps[cacheKey] = DateTime.now();
        
        return ratingData;
      }
    } catch (e) {
      print('DEBUG: Error loading rating: $e');
    }
    
    return null;
  }
  
  /// Установка рейтинга мастера
  static Future<bool> rateMaster(String masterId, String userId, int rating) async {
    try {
      final response = await _makeRequest(
        '$baseUrl/masters/$masterId/rate',
        method: 'POST',
        body: jsonEncode({
          'user_id': userId,
          'rating': rating,
        }),
      );
      
      if (response.statusCode == 200) {
        // Инвалидируем кэш рейтинга
        _cache.remove('rating:$masterId:$userId');
        return true;
      }
    } catch (e) {
      print('DEBUG: Error rating master: $e');
    }
    
    return false;
  }
  
  /// Получение статистики пользователя
  static Future<UserStats?> getUserStats(String userId) async {
    final cacheKey = 'user_stats:$userId';
    
    // Проверяем кэш
    if (_cache.containsKey(cacheKey) && _isCacheValid(cacheKey)) {
      return _cache[cacheKey];
    }
    
    try {
      final response = await _makeRequest('$baseUrl/user/$userId/stats');
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final stats = UserStats.fromJson(data);
        
        // Кэшируем результат
        _cache[cacheKey] = stats;
        _cacheTimestamps[cacheKey] = DateTime.now();
        
        return stats;
      }
    } catch (e) {
      print('DEBUG: Error loading user stats: $e');
    }
    
    return null;
  }
  
  /// Получение реферальной информации
  static Future<ReferralInfo?> getReferralInfo(String userId) async {
    final cacheKey = 'referral:$userId';
    
    // Проверяем кэш
    if (_cache.containsKey(cacheKey) && _isCacheValid(cacheKey)) {
      return _cache[cacheKey];
    }
    
    try {
      final response = await _makeRequest('$baseUrl/referral/$userId');
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final referralInfo = ReferralInfo.fromJson(data);
        
        // Кэшируем результат
        _cache[cacheKey] = referralInfo;
        _cacheTimestamps[cacheKey] = DateTime.now();
        
        return referralInfo;
      }
    } catch (e) {
      print('DEBUG: Error loading referral info: $e');
    }
    
    return null;
  }
  
  /// Логирование реферальной статистики
  static Future<bool> logReferralStats(String userId) async {
    try {
      final response = await _makeRequest(
        '$baseUrl/log-referral-stats',
        method: 'POST',
        body: jsonEncode({'user_id': userId}),
      );
      
      return response.statusCode == 200;
    } catch (e) {
      print('DEBUG: Error logging referral stats: $e');
      return false;
    }
  }
  
  /// Получение призов гивевея
  static Future<List<GiveawayPrize>> getGiveawayPrizes() async {
    const cacheKey = 'giveaway_prizes';
    
    // Проверяем кэш
    if (_cache.containsKey(cacheKey) && _isCacheValid(cacheKey)) {
      return _cache[cacheKey];
    }
    
    try {
      final response = await _makeRequest('$baseUrl/giveaway/prizes');
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final prizes = (data['prizes'] as List)
            .map((p) => GiveawayPrize.fromJson(p))
            .toList();
        
        // Кэшируем результат
        _cache[cacheKey] = prizes;
        _cacheTimestamps[cacheKey] = DateTime.now();
        
        return prizes;
      }
    } catch (e) {
      print('DEBUG: Error loading giveaway prizes: $e');
    }
    
    return [];
  }
  
  /// Проверка статуса гивевея
  static Future<GiveawayStatus?> getGiveawayStatus() async {
    const cacheKey = 'giveaway_status';
    
    // Проверяем кэш (короткий TTL для статуса)
    if (_cache.containsKey(cacheKey)) {
      final timestamp = _cacheTimestamps[cacheKey];
      if (timestamp != null && DateTime.now().difference(timestamp) < const Duration(minutes: 5)) {
        return _cache[cacheKey];
      }
    }
    
    try {
      final response = await _makeRequest('$baseUrl/giveaway/status');
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final status = GiveawayStatus.fromJson(data);
        
        // Кэшируем результат
        _cache[cacheKey] = status;
        _cacheTimestamps[cacheKey] = DateTime.now();
        
        return status;
      }
    } catch (e) {
      print('DEBUG: Error loading giveaway status: $e');
    }
    
    return null;
  }
  
  /// Очистка кэша
  static void clearCache() {
    _cache.clear();
    _cacheTimestamps.clear();
    print('DEBUG: Cache cleared');
  }
  
  /// Очистка кэша для конкретного ключа
  static void clearCacheForKey(String key) {
    _cache.remove(key);
    _cacheTimestamps.remove(key);
    print('DEBUG: Cache cleared for key: $key');
  }

  /// Получение всех артистов
  static Future<List<MasterModel>> getArtists() async {
    const cacheKey = 'artists';
    
    // Очищаем устаревший кэш
    _cleanExpiredCache();
    
    // Проверяем кэш
    if (_cache.containsKey(cacheKey) && _isCacheValid(cacheKey)) {
      print('DEBUG: Using cached artists');
      return _cache[cacheKey];
    }
    
    try {
      print('DEBUG: Loading artists from API');
      final response = await _makeRequest('$baseUrl/artists');
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final artists = (data['artists'] as List)
            .map((a) => MasterModel.fromApiData(a))
            .toList();
        
        // Кэшируем результат
        _cache[cacheKey] = artists;
        _cacheTimestamps[cacheKey] = DateTime.now();
        
        print('DEBUG: Loaded ${artists.length} artists from API');
        return artists;
      } else {
        print('DEBUG: API returned status ${response.statusCode}');
        throw Exception('Failed to load artists: ${response.statusCode}');
      }
    } catch (e) {
      print('DEBUG: Error loading artists from API: $e');
      return [];
    }
  }

  /// Получение всех товаров
  static Future<List<ProductModel>> getProducts({String? category, String? masterId}) async {
    final cacheKey = 'products:${category ?? 'all'}:${masterId ?? 'all'}';
    
    // Очищаем устаревший кэш
    _cleanExpiredCache();
    
    // Проверяем кэш
    if (_cache.containsKey(cacheKey) && _isCacheValid(cacheKey)) {
      print('DEBUG: Using cached products');
      return _cache[cacheKey];
    }
    
    try {
      print('DEBUG: Loading products from API');
      
      final queryParams = <String, String>{};
      if (category != null) queryParams['category'] = category;
      if (masterId != null) queryParams['master_id'] = masterId;
      
      final uri = Uri.parse('$baseUrl/products').replace(queryParameters: queryParams);
      final response = await _makeRequest(uri.toString());
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final products = (data['products'] as List)
            .map((p) => ProductModel.fromJson(p))
            .toList();
        
        // Кэшируем результат
        _cache[cacheKey] = products;
        _cacheTimestamps[cacheKey] = DateTime.now();
        
        print('DEBUG: Loaded ${products.length} products from API');
        return products;
      } else {
        print('DEBUG: API returned status ${response.statusCode}');
        throw Exception('Failed to load products: ${response.statusCode}');
      }
    } catch (e) {
      print('DEBUG: Error loading products from API: $e');
      return [];
    }
  }

  /// Получение товара по ID
  static Future<ProductModel?> getProduct(String productId, {String? userId}) async {
    final cacheKey = 'product:$productId';
    
    // Очищаем устаревший кэш
    _cleanExpiredCache();
    
    // Проверяем кэш
    if (_cache.containsKey(cacheKey) && _isCacheValid(cacheKey)) {
      print('DEBUG: Using cached product');
      return _cache[cacheKey];
    }
    
    try {
      print('DEBUG: Loading product from API');
      
      final queryParams = <String, String>{};
      if (userId != null) queryParams['user_id'] = userId;
      
      final uri = Uri.parse('$baseUrl/products/$productId').replace(queryParameters: queryParams);
      final response = await _makeRequest(uri.toString());
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final product = ProductModel.fromJson(data);
        
        // Кэшируем результат
        _cache[cacheKey] = product;
        _cacheTimestamps[cacheKey] = DateTime.now();
        
        print('DEBUG: Loaded product from API');
        return product;
      } else {
        print('DEBUG: API returned status ${response.statusCode}');
        return null;
      }
    } catch (e) {
      print('DEBUG: Error loading product from API: $e');
      return null;
    }
  }

  /// Добавление нового товара
  static Future<bool> addProduct(ProductModel product) async {
    try {
      print('DEBUG: Adding product to API');
      
      final response = await _makeRequest(
        '$baseUrl/products',
        method: 'POST',
        body: jsonEncode(product.toJson()),
      );
      
      if (response.statusCode == 201) {
        // Инвалидируем кэш товаров
        _cache.removeWhere((key, value) => key.startsWith('products:'));
        print('DEBUG: Product added successfully');
        return true;
      } else {
        print('DEBUG: API returned status ${response.statusCode}');
        return false;
      }
    } catch (e) {
      print('DEBUG: Error adding product to API: $e');
      return false;
    }
  }

  /// Логирование продажи
  static Future<bool> logSale({
    required String productId,
    required String masterId,
    String? userId,
    int quantity = 1,
    double price = 0,
    double totalAmount = 0,
  }) async {
    try {
      print('DEBUG: Logging sale to API');
      
      final saleData = {
        'product_id': productId,
        'master_id': masterId,
        'user_id': userId,
        'quantity': quantity,
        'price': price,
        'total_amount': totalAmount,
        'status': 'completed',
      };
      
      final response = await _makeRequest(
        '$baseUrl/sales',
        method: 'POST',
        body: jsonEncode(saleData),
      );
      
      if (response.statusCode == 200) {
        print('DEBUG: Sale logged successfully');
        return true;
      } else {
        print('DEBUG: API returned status ${response.statusCode}');
        return false;
      }
    } catch (e) {
      print('DEBUG: Error logging sale to API: $e');
      return false;
    }
  }

  /// Получение аналитики товаров
  static Future<Map<String, dynamic>?> getProductAnalytics({String? productId, String? masterId}) async {
    try {
      print('DEBUG: Loading product analytics from API');
      
      final queryParams = <String, String>{};
      if (productId != null) queryParams['product_id'] = productId;
      if (masterId != null) queryParams['master_id'] = masterId;
      
      final uri = Uri.parse('$baseUrl/products/analytics').replace(queryParameters: queryParams);
      final response = await _makeRequest(uri.toString());
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        print('DEBUG: Loaded product analytics from API');
        return data;
      } else {
        print('DEBUG: API returned status ${response.statusCode}');
        return null;
      }
    } catch (e) {
      print('DEBUG: Error loading product analytics from API: $e');
      return null;
    }
  }
}

// Модели данных
class RatingData {
  final double averageRating;
  final int votes;
  final int? userRating;
  
  RatingData({
    required this.averageRating,
    required this.votes,
    this.userRating,
  });
  
  factory RatingData.fromJson(Map<String, dynamic> json) {
    return RatingData(
      averageRating: (json['average'] as num?)?.toDouble() ?? 0.0,
      votes: json['votes'] as int? ?? 0,
      userRating: json['user_rating'] as int?,
    );
  }
}

class UserStats {
  final int tasksCompleted;
  final bool giveawayCompleted;
  final int referralCount;
  final int totalReferralXp;
  
  UserStats({
    required this.tasksCompleted,
    required this.giveawayCompleted,
    required this.referralCount,
    required this.totalReferralXp,
  });
  
  factory UserStats.fromJson(Map<String, dynamic> json) {
    return UserStats(
      tasksCompleted: json['tasks_completed'] as int? ?? 0,
      giveawayCompleted: json['giveaway_completed'] as bool? ?? false,
      referralCount: json['referral_count'] as int? ?? 0,
      totalReferralXp: json['total_referral_xp'] as int? ?? 0,
    );
  }
}

class ReferralInfo {
  final String referralCode;
  final int referralCount;
  final int totalReferralXp;
  final List<String> invitedUsers;
  
  ReferralInfo({
    required this.referralCode,
    required this.referralCount,
    required this.totalReferralXp,
    required this.invitedUsers,
  });
  
  factory ReferralInfo.fromJson(Map<String, dynamic> json) {
    return ReferralInfo(
      referralCode: json['referral_code'] as String? ?? '',
      referralCount: json['referral_count'] as int? ?? 0,
      totalReferralXp: json['total_referral_xp'] as int? ?? 0,
      invitedUsers: (json['invited_users'] as List?)?.cast<String>() ?? [],
    );
  }
}

class GiveawayPrize {
  final String name;
  final String description;
  final int value;
  final String category;
  final String? imageUrl;
  
  GiveawayPrize({
    required this.name,
    required this.description,
    required this.value,
    required this.category,
    this.imageUrl,
  });
  
  factory GiveawayPrize.fromJson(Map<String, dynamic> json) {
    return GiveawayPrize(
      name: json['name'] as String? ?? '',
      description: json['description'] as String? ?? '',
      value: json['value'] as int? ?? 0,
      category: json['category'] as String? ?? '',
      imageUrl: json['image_url'] as String?,
    );
  }
}

class GiveawayStatus {
  final bool isActive;
  final DateTime? endDate;
  final int totalParticipants;
  final List<String> winners;
  
  GiveawayStatus({
    required this.isActive,
    this.endDate,
    required this.totalParticipants,
    required this.winners,
  });
  
  factory GiveawayStatus.fromJson(Map<String, dynamic> json) {
    return GiveawayStatus(
      isActive: json['is_active'] as bool? ?? false,
      endDate: json['end_date'] != null 
          ? DateTime.parse(json['end_date'] as String)
          : null,
      totalParticipants: json['total_participants'] as int? ?? 0,
      winners: (json['winners'] as List?)?.cast<String>() ?? [],
    );
  }
} 