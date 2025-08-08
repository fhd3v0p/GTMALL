import 'dart:convert';
import 'package:http/http.dart' as http;
import '../api_config.dart';

class SupabaseService {
  static final SupabaseService _instance = SupabaseService._internal();
  factory SupabaseService() => _instance;
  SupabaseService._internal();

  // === ARTISTS ===
  Future<List<Map<String, dynamic>>> getArtists() async {
    try {
      final response = await http.get(
        Uri.parse(ApiConfig.getTableUrl(ApiConfig.artistsTable)),
        headers: ApiConfig.headers,
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

  Future<Map<String, dynamic>?> getArtist(int artistId) async {
    try {
      final response = await http.get(
        Uri.parse('${ApiConfig.getTableUrl(ApiConfig.artistsTable)}?id=eq.$artistId'),
        headers: ApiConfig.headers,
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

  Future<List<Map<String, dynamic>>> getArtistGallery(int artistId) async {
    try {
      final response = await http.get(
        Uri.parse('${ApiConfig.getTableUrl(ApiConfig.artistGalleryTable)}?artist_id=eq.$artistId'),
        headers: ApiConfig.headers,
      );

      if (response.statusCode == 200) {
        return List<Map<String, dynamic>>.from(json.decode(response.body));
      } else {
        throw Exception('Failed to load gallery: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error fetching gallery: $e');
    }
  }

  // === USERS ===
  Future<Map<String, dynamic>?> getUser(int telegramId) async {
    try {
      final response = await http.get(
        Uri.parse('${ApiConfig.getTableUrl(ApiConfig.usersTable)}?telegram_id=eq.$telegramId'),
        headers: ApiConfig.headers,
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

  Future<Map<String, dynamic>> createUser(Map<String, dynamic> userData) async {
    try {
      final response = await http.post(
        Uri.parse(ApiConfig.getTableUrl(ApiConfig.usersTable)),
        headers: ApiConfig.headers,
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

  Future<Map<String, dynamic>> updateUser(int telegramId, Map<String, dynamic> userData) async {
    try {
      final response = await http.patch(
        Uri.parse('${ApiConfig.getTableUrl(ApiConfig.usersTable)}?telegram_id=eq.$telegramId'),
        headers: ApiConfig.headers,
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
  Future<List<Map<String, dynamic>>> getUserSubscriptions(int telegramId) async {
    try {
      final response = await http.get(
        Uri.parse('${ApiConfig.getTableUrl(ApiConfig.subscriptionsTable)}?telegram_id=eq.$telegramId'),
        headers: ApiConfig.headers,
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

  Future<Map<String, dynamic>> addSubscription(Map<String, dynamic> subscriptionData) async {
    try {
      final response = await http.post(
        Uri.parse(ApiConfig.getTableUrl(ApiConfig.subscriptionsTable)),
        headers: ApiConfig.headers,
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
  Future<Map<String, dynamic>?> getReferralByCode(String referralCode) async {
    try {
      final response = await http.get(
        Uri.parse('${ApiConfig.getTableUrl(ApiConfig.referralsTable)}?referral_code=eq.$referralCode'),
        headers: ApiConfig.headers,
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

  Future<Map<String, dynamic>> createReferral(Map<String, dynamic> referralData) async {
    try {
      final response = await http.post(
        Uri.parse(ApiConfig.getTableUrl(ApiConfig.referralsTable)),
        headers: ApiConfig.headers,
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
  Future<List<Map<String, dynamic>>> getActiveGiveaways() async {
    try {
      final response = await http.get(
        Uri.parse('${ApiConfig.getTableUrl(ApiConfig.giveawaysTable)}?is_active=eq.true'),
        headers: ApiConfig.headers,
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
  Future<int> getTotalTickets() async {
    try {
      final response = await http.get(
        Uri.parse('${ApiConfig.getTableUrl(ApiConfig.usersTable)}?select=tickets_count'),
        headers: ApiConfig.headers,
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

  Future<Map<String, dynamic>> getUserStats(int telegramId) async {
    try {
      final user = await getUser(telegramId);
      if (user == null) return {};

      final subscriptions = await getUserSubscriptions(telegramId);
      
      return {
        'total_tickets': user['tickets_count'] ?? 0,
        'subscription_tickets': subscriptions.length >= 9 ? 1 : 0,
        'referral_tickets': (user['tickets_count'] ?? 0) - (subscriptions.length >= 9 ? 1 : 0),
        'referral_code': user['referral_code'] ?? '',
        'subscriptions_count': subscriptions.length,
      };
    } catch (e) {
      throw Exception('Error fetching user stats: $e');
    }
  }

  // === STORAGE ===
  String getFileUrl(String path, String fileName) {
    return ApiConfig.getStorageUrl(path, fileName);
  }

  // === UTILITY ===
  bool get isConfigured => ApiConfig.isConfigured;
} 