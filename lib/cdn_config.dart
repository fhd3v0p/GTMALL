import 'dart:io';

class CdnConfig {
  // MinIO CDN конфигурация через API прокси
  static const String minioEndpoint = 'https://gtm.baby/api/minio/download/gtm-assets';
  static const String bucketName = 'gtm-assets';
  static const String accessKey = 'gtmadmin';
  static const String secretKey = 'gtm123456';
  
  // CDN URLs для разных типов файлов
  static const String cdnBaseUrl = '$minioEndpoint';
  
  // Пути к различным категориям файлов
  static const String imagesPath = '$cdnBaseUrl/assets/images';
  static const String artistsPath = '$cdnBaseUrl/assets/artists';
  static const String fontsPath = '$cdnBaseUrl/assets/fonts';
  static const String videosPath = '$cdnBaseUrl/assets/videos';
  
  // Методы для получения URL файлов через API прокси
  static String getImageUrl(String filename) {
    return '$cdnBaseUrl/$filename';
  }
  
  static String getArtistAvatarUrl(String artistName) {
    return '$cdnBaseUrl/artists/$artistName/avatar.png';
  }
  
  static String getArtistGalleryUrl(String artistName, int imageNumber) {
    return '$cdnBaseUrl/artists/$artistName/gallery$imageNumber.jpg';
  }
  
  static String getArtistBioUrl(String artistName) {
    return '$cdnBaseUrl/artists/$artistName/bio.txt';
  }
  
  static String getArtistLinksUrl(String artistName) {
    return '$cdnBaseUrl/artists/$artistName/links.json';
  }
  
  static String getFontUrl(String fontName) {
    return '$cdnBaseUrl/fonts/$fontName';
  }
  
  static String getVideoUrl(String filename) {
    return '$cdnBaseUrl/$filename';
  }
  
  // Список доступных артистов (из MinIO)
  static const List<String> availableArtists = [
    'alena',
    'aspergill',
    'Blodivamp',
    'EMI',
    'Lin++',
    'msk_tattoo_Alena',
    'msk_tattoo_EMI',
    'MurderDoll',
    'naidi',
    'Клубника',
    'Чучундра'
  ];
  
  // Список основных изображений
  static const List<String> mainImages = [
    'giveaway_banner.png',
    'main_banner.png',
    'master_cloud_banner.png',
    'role_selection_banner.png',
    'city_selection_banner.png',
    'master_detail_banner.png',
    'master_detail_back_banner.png',
    'master_detail_logo_banner.png',
    'master_join_banner.png',
    'giveaway_back_banner.png',
    'center_memoji.png'
  ];
  
  // Список аватаров
  static const List<String> avatars = [
    'avatar1.png',
    'avatar2.png',
    'avatar3.png',
    'avatar4.png',
    'avatar5.png',
    'avatar6.png'
  ];
  
  // Список изображений мастеров
  static const List<String> masters = [
    'm1.png',
    'm2.png',
    'm3.png',
    'm4.png',
    'm5.png',
    'm6.png'
  ];
  
  // Список шрифтов
  static const List<String> fonts = [
    'Lepka.otf',
    'NauryzKeds.ttf',
    'OpenSans_Condensed-Bold.ttf',
    'OpenSans_Condensed-Regular.ttf'
  ];
  
  // Список видео
  static const List<String> videos = [
    'FSR.mp4'
  ];
} 