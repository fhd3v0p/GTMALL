import 'package:flutter_dotenv/flutter_dotenv.dart';

class ApiConfig {
  static final String supabaseUrl = dotenv.env['SUPABASE_URL'] ?? '';
  static final String supabaseAnonKey = dotenv.env['SUPABASE_ANON_KEY'] ?? '';
  static const String storageBucket = 'gtm-assets-public';

  static const String avatarsPath = 'avatars';
  static const String galleryPath = 'gallery';
  static const String artistsPath = 'artists';
  static const String bannersPath = 'banners';
  static const String productsPath = 'GTM_products';

  static String get apiBaseUrl => '$supabaseUrl/rest/v1';

  static const String usersTable = 'users';
  static const String artistsTable = 'artists';
  static const String subscriptionsTable = 'subscriptions';
  static const String referralsTable = 'referrals';
  static const String giveawaysTable = 'giveaways';
  static const String artistGalleryTable = 'artist_gallery';
  static const String productsTable = 'products';

  static Map<String, String> get headers => {
    'apikey': supabaseAnonKey,
    'Authorization': 'Bearer $supabaseAnonKey',
    'Content-Type': 'application/json',
  };

  static String getStorageUrl(String path, String fileName) {
    return '$supabaseUrl/storage/v1/object/public/$storageBucket/$path/$fileName';
  }

  static String getTableUrl(String table) {
    return '$apiBaseUrl/$table';
  }

  static final String ratingApiBaseUrl = dotenv.env['RATING_API_BASE_URL'] ?? 'https://api.gtm.baby';
  static Map<String, String> get ratingApiHeaders => {'Content-Type': 'application/json'};

  static String get telegramBotToken => dotenv.env['TELEGRAM_BOT_TOKEN'] ?? '';

  static bool get isConfigured => supabaseUrl.isNotEmpty && supabaseAnonKey.isNotEmpty;
} 