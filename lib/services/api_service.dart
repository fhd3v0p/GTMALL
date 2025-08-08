import 'dart:convert';
import 'package:http/http.dart' as http;
import '../api_config.dart';

class ApiService {
  // Используем Supabase API вместо legacy
  static String get baseUrl => ApiConfig.apiBaseUrl;
  static String get supabaseUrl => ApiConfig.supabaseUrl;
  static String get supabaseAnonKey => ApiConfig.supabaseAnonKey;

  // Headers для Supabase API
  static Map<String, String> get headers => ApiConfig.headers;

  // === REFERRAL CODE via Rating API ===
  static Future<String?> getOrCreateReferralCode(String telegramId) async {
    try {
      final resp = await http.post(
        Uri.parse('${ApiConfig.ratingApiBaseUrl}/api/referral-code'),
        headers: ApiConfig.ratingApiHeaders,
        body: jsonEncode({'telegram_id': int.tryParse(telegramId) ?? telegramId}),
      );
      if (resp.statusCode == 200 && resp.body.isNotEmpty) {
        final body = jsonDecode(resp.body);
        final code = body['referral_code'] as String?;
        return code;
      }
    } catch (_) {}
    return null;
  }

  // === ARTISTS ===
  static Future<List<Map<String, dynamic>>> getArtists() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/${ApiConfig.artistsTable}'),
        headers: headers,
      );

      if (response.statusCode == 200) {
        return List<Map<String, dynamic>>.from(json.decode(response.body));
      } else {
        throw Exception('Failed to load artists: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error fetching artists: $e');
    }
  }

  static Future<Map<String, dynamic>?> getArtist(int artistId) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/${ApiConfig.artistsTable}?id=eq.$artistId'),
        headers: headers,
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data.isNotEmpty ? Map<String, dynamic>.from(data.first) : null;
      } else {
        throw Exception('Failed to load artist: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error fetching artist: $e');
    }
  }

  // === USERS ===
  static Future<Map<String, dynamic>?> getUser(int telegramId) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/${ApiConfig.usersTable}?telegram_id=eq.$telegramId'),
        headers: headers,
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data.isNotEmpty ? Map<String, dynamic>.from(data.first) : null;
      } else {
        throw Exception('Failed to load user: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error fetching user: $e');
    }
  }

  static Future<Map<String, dynamic>> createUser(Map<String, dynamic> userData) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/${ApiConfig.usersTable}'),
        headers: headers,
        body: json.encode(userData),
      );

      if (response.statusCode == 201) {
        return Map<String, dynamic>.from(json.decode(response.body));
      } else {
        throw Exception('Failed to create user: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error creating user: $e');
    }
  }

  static Future<Map<String, dynamic>> updateUser(int telegramId, Map<String, dynamic> userData) async {
    try {
      final response = await http.patch(
        Uri.parse('$baseUrl/${ApiConfig.usersTable}?telegram_id=eq.$telegramId'),
        headers: headers,
        body: json.encode(userData),
      );

      if (response.statusCode == 200) {
        return Map<String, dynamic>.from(json.decode(response.body));
      } else {
        throw Exception('Failed to update user: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error updating user: $e');
    }
  }

  // === SUBSCRIPTIONS ===
  static Future<List<Map<String, dynamic>>> getUserSubscriptions(int telegramId) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/${ApiConfig.subscriptionsTable}?telegram_id=eq.$telegramId'),
        headers: headers,
      );

      if (response.statusCode == 200) {
        return List<Map<String, dynamic>>.from(json.decode(response.body));
      } else {
        throw Exception('Failed to load subscriptions: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error fetching subscriptions: $e');
    }
  }

  static Future<Map<String, dynamic>> addSubscription(Map<String, dynamic> subscriptionData) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/${ApiConfig.subscriptionsTable}'),
        headers: headers,
        body: json.encode(subscriptionData),
      );

      if (response.statusCode == 201) {
        return Map<String, dynamic>.from(json.decode(response.body));
      } else {
        throw Exception('Failed to add subscription: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error adding subscription: $e');
    }
  }

  // === REFERRALS ===
  static Future<Map<String, dynamic>?> getReferralByCode(String referralCode) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/${ApiConfig.referralsTable}?referral_code=eq.$referralCode'),
        headers: headers,
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data.isNotEmpty ? Map<String, dynamic>.from(data.first) : null;
      } else {
        throw Exception('Failed to load referral: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error fetching referral: $e');
    }
  }

  static Future<Map<String, dynamic>> createReferral(Map<String, dynamic> referralData) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/${ApiConfig.referralsTable}'),
        headers: headers,
        body: json.encode(referralData),
      );

      if (response.statusCode == 201) {
        return Map<String, dynamic>.from(json.decode(response.body));
      } else {
        throw Exception('Failed to create referral: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error creating referral: $e');
    }
  }

  // === GIVEAWAYS ===
  static Future<List<Map<String, dynamic>>> getActiveGiveaways() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/${ApiConfig.giveawaysTable}?is_active=eq.true'),
        headers: headers,
      );

      if (response.statusCode == 200) {
        return List<Map<String, dynamic>>.from(json.decode(response.body));
      } else {
        throw Exception('Failed to load giveaways: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error fetching giveaways: $e');
    }
  }

  // === STATISTICS ===
  static Future<int> getTotalTickets() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/${ApiConfig.usersTable}?select=tickets_count'),
        headers: headers,
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data.fold<int>(0, (sum, user) => sum + ((user['tickets_count'] as int?) ?? 0));
      } else {
        throw Exception('Failed to load total tickets: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error fetching total tickets: $e');
    }
  }

  static Future<Map<String, dynamic>> getUserStats(int telegramId) async {
    try {
      final user = await getUser(telegramId);
      final subscriptions = await getUserSubscriptions(telegramId);
      
      return {
        'user': user,
        'subscriptions': subscriptions,
        'tickets_count': user?['tickets_count'] ?? 0,
        'has_subscription_ticket': user?['has_subscription_ticket'] ?? false,
      };
    } catch (e) {
      throw Exception('Error fetching user stats: $e');
    }
  }

  // === MASTERS ===
  static Future<List<Map<String, dynamic>>> getMasters() async {
    try {
      // Используем таблицу artists как masters
      final response = await http.get(
        Uri.parse('$baseUrl/${ApiConfig.artistsTable}'),
        headers: headers,
      );

      if (response.statusCode == 200) {
        return List<Map<String, dynamic>>.from(json.decode(response.body));
      } else {
        throw Exception('Failed to load masters: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error fetching masters: $e');
    }
  }

  // === PRODUCTS ===
  static Future<List<Map<String, dynamic>>> getProductsByMasterAndCategory(int masterId, int categoryId) async {
    try {
      print('🚨 DEBUG: Запрашиваем продукты для мастера ID: $masterId');
      print('🚨 DEBUG: URL запроса: $baseUrl/${ApiConfig.productsTable}?master_id=eq.$masterId');
      print('🚨 DEBUG: Headers: $headers');
      
      // Используем таблицу products
      final response = await http.get(
        Uri.parse('$baseUrl/${ApiConfig.productsTable}?master_id=eq.$masterId'),
        headers: headers,
      );

      print('🚨 DEBUG: Ответ API - статус: ${response.statusCode}');
      print('🚨 DEBUG: Ответ API - тело: ${response.body}');

      if (response.statusCode == 200) {
        final List<Map<String, dynamic>> products = List<Map<String, dynamic>>.from(json.decode(response.body));
        print('🚨 DEBUG: Загружено продуктов: ${products.length}');
        for (var product in products) {
          print('🚨 DEBUG: Продукт: ${product['name']} (категория: ${product['category']})');
        }
        return products;
      } else {
        print('🚨 DEBUG: Ошибка загрузки продуктов: ${response.statusCode}');
        print('🚨 DEBUG: Тело ошибки: ${response.body}');
        throw Exception('Failed to load products: ${response.statusCode}');
      }
    } catch (e) {
      print('🚨 DEBUG: Исключение при загрузке продуктов: $e');
      throw Exception('Error fetching products: $e');
    }
  }

  // === HEALTH CHECK ===
  static Future<bool> healthCheck() async {
    try {
      final response = await http.get(
        Uri.parse('$supabaseUrl/rest/v1/'),
        headers: headers,
      );
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }
} 