import 'dart:convert';
import 'dart:typed_data';
import 'package:http/http.dart' as http;
import '../cdn_config.dart';
import '../api_config.dart';

class CdnService {
  static const String _minioEndpoint = CdnConfig.minioEndpoint;
  static const String _bucketName = CdnConfig.bucketName;
  static const String _accessKey = CdnConfig.accessKey;
  static const String _secretKey = CdnConfig.secretKey;

  static const String _baseUrl = CdnConfig.cdnBaseUrl;

  /// Загружает изображение из CDN
  static Future<Uint8List?> loadImage(String filename) async {
    try {
      final url = CdnConfig.getImageUrl(filename);
      final response = await http.get(Uri.parse(url));
      
      if (response.statusCode == 200) {
        return response.bodyBytes;
      } else {
        print('❌ Ошибка загрузки изображения $filename: ${response.statusCode}');
        return null;
      }
    } catch (e) {
      print('❌ Ошибка загрузки изображения $filename: $e');
      return null;
    }
  }

  /// Загружает аватар артиста из CDN
  static Future<Uint8List?> loadArtistAvatar(String artistName) async {
    try {
      final url = CdnConfig.getArtistAvatarUrl(artistName);
      final response = await http.get(Uri.parse(url));
      
      if (response.statusCode == 200) {
        return response.bodyBytes;
      } else {
        print('❌ Ошибка загрузки аватара $artistName: ${response.statusCode}');
        return null;
      }
    } catch (e) {
      print('❌ Ошибка загрузки аватара $artistName: $e');
      return null;
    }
  }

  /// Загружает изображение галереи артиста из CDN
  static Future<Uint8List?> loadArtistGalleryImage(String artistName, int imageNumber) async {
    try {
      final url = CdnConfig.getArtistGalleryUrl(artistName, imageNumber);
      final response = await http.get(Uri.parse(url));
      
      if (response.statusCode == 200) {
        return response.bodyBytes;
      } else {
        print('❌ Ошибка загрузки галереи $artistName/gallery$imageNumber.jpg: ${response.statusCode}');
        return null;
      }
    } catch (e) {
      print('❌ Ошибка загрузки галереи $artistName/gallery$imageNumber.jpg: $e');
      return null;
    }
  }

  /// Загружает шрифт из CDN
  static Future<Uint8List?> loadFont(String fontName) async {
    try {
      final url = CdnConfig.getFontUrl(fontName);
      final response = await http.get(Uri.parse(url));
      
      if (response.statusCode == 200) {
        return response.bodyBytes;
      } else {
        print('❌ Ошибка загрузки шрифта $fontName: ${response.statusCode}');
        return null;
      }
    } catch (e) {
      print('❌ Ошибка загрузки шрифта $fontName: $e');
      return null;
    }
  }

  /// Загружает видео из CDN
  static Future<Uint8List?> loadVideo(String filename) async {
    try {
      final url = CdnConfig.getVideoUrl(filename);
      final response = await http.get(Uri.parse(url));
      
      if (response.statusCode == 200) {
        return response.bodyBytes;
      } else {
        print('❌ Ошибка загрузки видео $filename: ${response.statusCode}');
        return null;
      }
    } catch (e) {
      print('❌ Ошибка загрузки видео $filename: $e');
      return null;
    }
  }

  /// Проверяет доступность CDN
  static Future<bool> checkCdnAvailability() async {
    try {
      final testUrl = CdnConfig.getImageUrl('giveaway_banner.png');
      final response = await http.get(Uri.parse(testUrl));
      return response.statusCode == 200;
    } catch (e) {
      print('❌ CDN недоступен: $e');
      return false;
    }
  }

  /// Получить URL для аватара
  static String getAvatarUrl(String filename) {
    return '${ApiConfig.avatarCdnUrl}/$filename';
  }

  /// Получить URL для аватара артиста
  static String getArtistAvatarUrl(String artistName, String filename) {
    return '${ApiConfig.artistCdnUrl}/$artistName/$filename';
  }

  /// Получить URL для галереи артиста
  static String getArtistGalleryUrl(String artistName, String filename) {
    return '${ApiConfig.artistCdnUrl}/$artistName/$filename';
  }

  /// Получить URL для баннера
  static String getBannerUrl(String filename) {
    return '${ApiConfig.bannerCdnUrl}/$filename';
  }

  /// Получить информацию об артисте
  static Future<Map<String, dynamic>?> getArtistInfo(String artistName) async {
    try {
      // Загружаем bio и links из CDN
      final bio = await loadArtistBio(artistName);
      final links = await loadArtistLinks(artistName);
      
      if (bio == null && links == null) {
        return null;
      }
      
      return {
        'bio': bio ?? '',
        'links': links ?? {},
        'avatar_url': CdnConfig.getArtistAvatarUrl(artistName),
      };
    } catch (e) {
      print('❌ Ошибка получения информации об артисте $artistName: $e');
      return null;
    }
  }

  /// Загружает bio артиста из CDN
  static Future<String?> loadArtistBio(String artistName) async {
    try {
      final url = CdnConfig.getArtistBioUrl(artistName);
      final response = await http.get(Uri.parse(url));
      
      if (response.statusCode == 200) {
        return response.body;
      } else {
        print('❌ Ошибка загрузки bio $artistName: ${response.statusCode}');
        return null;
      }
    } catch (e) {
      print('❌ Ошибка загрузки bio $artistName: $e');
      return null;
    }
  }

  /// Загружает links артиста из CDN
  static Future<Map<String, dynamic>?> loadArtistLinks(String artistName) async {
    try {
      final url = CdnConfig.getArtistLinksUrl(artistName);
      final response = await http.get(Uri.parse(url));
      
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        print('❌ Ошибка загрузки links $artistName: ${response.statusCode}');
        return null;
      }
    } catch (e) {
      print('❌ Ошибка загрузки links $artistName: $e');
      return null;
    }
  }

  /// Получить список файлов артиста
  static Future<List<String>> getArtistFiles(String artistName) async {
    try {
      final response = await http.get(Uri.parse('${ApiConfig.artistCdnUrl}/$artistName/'));
      
      if (response.statusCode == 200) {
        // Парсим HTML для получения списка файлов
        final body = response.body;
        final files = <String>[];
        
        // Простой парсинг для получения .jpg и .png файлов
        final regex = RegExp(r'href="([^"]*\.(jpg|png|jpeg))"');
        final matches = regex.allMatches(body);
        
        for (final match in matches) {
          files.add(match.group(1)!);
        }
        
        return files;
      }
    } catch (e) {
      print('Ошибка получения файлов артиста: $e');
    }
    return [];
  }

  /// Проверить доступность файла
  static Future<bool> isFileAvailable(String url) async {
    try {
      final response = await http.head(Uri.parse(url));
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }

  /// Получить размер файла
  static Future<int?> getFileSize(String url) async {
    try {
      final response = await http.head(Uri.parse(url));
      if (response.statusCode == 200) {
        final contentLength = response.headers['content-length'];
        return contentLength != null ? int.tryParse(contentLength) : null;
      }
    } catch (e) {
      print('Ошибка получения размера файла: $e');
    }
    return null;
  }

  /// Получает список всех доступных артистов
  static List<String> getAvailableArtists() {
    return CdnConfig.availableArtists;
  }

  /// Получает список всех основных изображений
  static List<String> getMainImages() {
    return CdnConfig.mainImages;
  }

  /// Получает список всех аватаров
  static List<String> getAvatars() {
    return CdnConfig.avatars;
  }
} 