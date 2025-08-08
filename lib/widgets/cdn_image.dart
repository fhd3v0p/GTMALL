import 'package:flutter/material.dart';
import '../services/cdn_service.dart';

class CdnImage extends StatelessWidget {
  final String url;
  final double? width;
  final double? height;
  final BoxFit? fit;
  final Widget? placeholder;
  final Widget? errorWidget;
  final BorderRadius? borderRadius;

  const CdnImage({
    Key? key,
    required this.url,
    this.width,
    this.height,
    this.fit,
    this.placeholder,
    this.errorWidget,
    this.borderRadius,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: borderRadius ?? BorderRadius.zero,
      child: Image.network(
        url,
        width: width,
        height: height,
        fit: fit ?? BoxFit.cover,
        loadingBuilder: (context, child, loadingProgress) {
          if (loadingProgress == null) return child;
          return placeholder ?? 
            Container(
              color: Colors.grey[300],
              child: const Center(
                child: CircularProgressIndicator(),
              ),
            );
        },
        errorBuilder: (context, error, stackTrace) {
          return errorWidget ?? 
            Container(
              color: Colors.grey[200],
              child: const Center(
                child: Icon(
                  Icons.error_outline,
                  color: Colors.grey,
                  size: 32,
                ),
              ),
            );
        },
        headers: const {
          'User-Agent': 'GTM-App/1.0',
        },
      ),
    );
  }
}

/// Виджет для отображения аватара артиста
class ArtistAvatar extends StatelessWidget {
  final String artistName;
  final double? width;
  final double? height;
  final BoxFit? fit;
  final BorderRadius? borderRadius;

  const ArtistAvatar({
    Key? key,
    required this.artistName,
    this.width,
    this.height,
    this.fit,
    this.borderRadius,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final avatarUrl = CdnService.getArtistAvatarUrl(artistName, 'avatar.png');
    
    return CdnImage(
      url: avatarUrl,
      width: width,
      height: height,
      fit: fit,
      borderRadius: borderRadius,
      placeholder: Container(
        color: Colors.grey[300],
        child: Center(
          child: Text(
            artistName[0].toUpperCase(),
            style: const TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.bold,
              color: Colors.grey,
            ),
          ),
        ),
      ),
    );
  }
}

/// Виджет для отображения баннера
class BannerImage extends StatelessWidget {
  final String filename;
  final double? width;
  final double? height;
  final BoxFit? fit;
  final BorderRadius? borderRadius;

  const BannerImage({
    Key? key,
    required this.filename,
    this.width,
    this.height,
    this.fit,
    this.borderRadius,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final bannerUrl = CdnService.getBannerUrl(filename);
    
    return CdnImage(
      url: bannerUrl,
      width: width,
      height: height,
      fit: fit,
      borderRadius: borderRadius,
    );
  }
}

/// Виджет для отображения галереи артиста
class ArtistGallery extends StatelessWidget {
  final String artistName;
  final List<String> filenames;
  final double itemWidth;
  final double itemHeight;
  final int crossAxisCount;
  final double spacing;
  final double runSpacing;

  const ArtistGallery({
    Key? key,
    required this.artistName,
    required this.filenames,
    this.itemWidth = 120,
    this.itemHeight = 120,
    this.crossAxisCount = 3,
    this.spacing = 8,
    this.runSpacing = 8,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return GridView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: crossAxisCount,
        childAspectRatio: itemWidth / itemHeight,
        crossAxisSpacing: spacing,
        mainAxisSpacing: runSpacing,
      ),
      itemCount: filenames.length,
      itemBuilder: (context, index) {
        final filename = filenames[index];
        final imageUrl = CdnService.getArtistGalleryUrl(artistName, filename);
        
        return CdnImage(
          url: imageUrl,
          borderRadius: BorderRadius.circular(8),
        );
      },
    );
  }
} 