import 'dart:convert';
import 'package:http/http.dart' as http;
import '../api_config.dart';

class TicketsApiService {
  static String get _baseUrl => '${ApiConfig.ratingApiBaseUrl}/api'; // API endpoint from .env
  
  /// Проверка подписки и получение билетов
  static Future<Map<String, dynamic>> checkSubscription(int telegramId) async {
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/check_subscription'),
        headers: ApiConfig.ratingApiHeaders,
        body: jsonEncode({
          'telegram_id': telegramId,
        }),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Ошибка проверки подписки: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Ошибка сети: $e');
    }
  }

  /// Получение статистики билетов пользователя
  static Future<Map<String, dynamic>> getUserTickets(int telegramId) async {
    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/user_tickets/$telegramId'),
        headers: ApiConfig.ratingApiHeaders,
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Ошибка получения билетов: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Ошибка сети: $e');
    }
  }

  /// Получение общей статистики билетов
  static Future<Map<String, dynamic>> getTotalTicketsStats() async {
    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/total_tickets_stats'),
        headers: ApiConfig.ratingApiHeaders,
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Ошибка получения статистики: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Ошибка сети: $e');
    }
  }

  /// Прямой вызов Supabase RPC функции для проверки подписки
  static Future<Map<String, dynamic>> callTelegramBotCheck(int telegramId) async {
    try {
      final response = await http.post(
        Uri.parse('${ApiConfig.supabaseUrl}/rest/v1/rpc/check_subscription_and_award_ticket'),
        headers: {
          'apikey': ApiConfig.supabaseAnonKey,
          'Authorization': 'Bearer ${ApiConfig.supabaseAnonKey}',
          'Content-Type': 'application/json',
        },
        body: jsonEncode({
          'p_telegram_id': telegramId,
          'p_is_subscribed': true, // Временно true для тестирования
        }),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Ошибка вызова Supabase: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Ошибка сети: $e');
    }
  }
}

/// Модель данных билетов
class TicketStats {
  final int subscriptionTickets;
  final int referralTickets;
  final int totalTickets;
  final String referralCode;
  final bool ticketAwarded;
  final String message;

  TicketStats({
    required this.subscriptionTickets,
    required this.referralTickets,
    required this.totalTickets,
    required this.referralCode,
    required this.ticketAwarded,
    required this.message,
  });

  factory TicketStats.fromJson(Map<String, dynamic> json) {
    return TicketStats(
      subscriptionTickets: json['subscription_tickets'] ?? 0,
      referralTickets: json['referral_tickets'] ?? 0,
      totalTickets: json['total_tickets'] ?? 0,
      referralCode: json['referral_code'] ?? '',
      ticketAwarded: json['ticket_awarded'] ?? false,
      message: json['message'] ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'subscription_tickets': subscriptionTickets,
      'referral_tickets': referralTickets,
      'total_tickets': totalTickets,
      'referral_code': referralCode,
      'ticket_awarded': ticketAwarded,
      'message': message,
    };
  }
}

/// Модель общей статистики билетов
class TotalTicketsStats {
  final int totalSubscriptionTickets;
  final int totalReferralTickets;
  final int totalUserTickets;

  TotalTicketsStats({
    required this.totalSubscriptionTickets,
    required this.totalReferralTickets,
    required this.totalUserTickets,
  });

  factory TotalTicketsStats.fromJson(Map<String, dynamic> json) {
    return TotalTicketsStats(
      totalSubscriptionTickets: json['total_subscription_tickets'] ?? 0,
      totalReferralTickets: json['total_referral_tickets'] ?? 0,
      totalUserTickets: json['total_user_tickets'] ?? 0,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'total_subscription_tickets': totalSubscriptionTickets,
      'total_referral_tickets': totalReferralTickets,
      'total_user_tickets': totalUserTickets,
    };
  }
} 