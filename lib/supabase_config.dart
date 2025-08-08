class SupabaseConfig {
  // Supabase Configuration для проекта rxmtovqxjsvogyywyrha
  static const String supabaseUrl = 'https://rxmtovqxjsvogyywyrha.supabase.co';
  static const String supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1Mjg1NTAsImV4cCI6MjA3MDEwNDU1MH0.gDkJybktFoi486hbIVwppDfmVQlAR0fM4o4Sl1-AxhE';
  
  // Supabase Storage Configuration
  static const String storageBucket = 'gtm-assets';
  
  // Storage Paths
  static const String avatarsPath = 'avatars';
  static const String galleryPath = 'gallery';
  static const String artistsPath = 'artists';
  static const String bannersPath = 'banners';
  
  // API Endpoints
  static const String apiBaseUrl = '$supabaseUrl/rest/v1';
  
  // Database Tables
  static const String usersTable = 'users';
  static const String artistsTable = 'artists';
  static const String subscriptionsTable = 'subscriptions';
  static const String referralsTable = 'referrals';
  static const String giveawaysTable = 'giveaways';
  static const String artistGalleryTable = 'artist_gallery';
  
  // Headers for Supabase API
  static Map<String, String> get headers => {
    'apikey': supabaseAnonKey,
    'Authorization': 'Bearer $supabaseAnonKey',
    'Content-Type': 'application/json',
  };
  
  // Storage URLs
  static String getStorageUrl(String path, String fileName) {
    return '$supabaseUrl/storage/v1/object/public/$storageBucket/$path/$fileName';
  }
  
  // API URLs
  static String getTableUrl(String table) {
    return '$apiBaseUrl/$table';
  }
  
  // Validation
  static bool get isConfigured {
    return supabaseUrl != 'https://your-project.supabase.co' && 
           supabaseAnonKey != 'your-anon-key-here';
  }
  
  // Пример URL для баннера
  static const String citySelectionBannerUrl = 'https://rxmtovqxjsvogyywyrha.supabase.co/storage/v1/object/public/gtm-assets/banners/city_selection_banner.png';
} 