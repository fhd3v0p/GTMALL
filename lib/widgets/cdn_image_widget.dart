import 'package:flutter/material.dart';
import 'dart:typed_data';
import '../services/cdn_service.dart';

class CdnImageWidget extends StatefulWidget {
  final String imageUrl;
  final double? width;
  final double? height;
  final BoxFit? fit;
  final Widget? placeholder;
  final Widget? errorWidget;

  const CdnImageWidget({
    Key? key,
    required this.imageUrl,
    this.width,
    this.height,
    this.fit,
    this.placeholder,
    this.errorWidget,
  }) : super(key: key);

  @override
  State<CdnImageWidget> createState() => _CdnImageWidgetState();
}

class _CdnImageWidgetState extends State<CdnImageWidget> {
  Uint8List? _imageData;
  bool _isLoading = true;
  bool _hasError = false;

  @override
  void initState() {
    super.initState();
    _loadImage();
  }

  Future<void> _loadImage() async {
    try {
      setState(() {
        _isLoading = true;
        _hasError = false;
      });

      // Пытаемся загрузить из CDN
      final cdnData = await CdnService.loadImage(widget.imageUrl);
      
      if (cdnData != null) {
        setState(() {
          _imageData = cdnData;
          _isLoading = false;
        });
      } else {
        // Если CDN недоступен, используем локальный ассет
        setState(() {
          _isLoading = false;
          _hasError = true;
        });
      }
    } catch (e) {
      setState(() {
        _isLoading = false;
        _hasError = true;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return Container(
        width: widget.width,
        height: widget.height,
        child: widget.placeholder ?? 
          const Center(child: CircularProgressIndicator()),
      );
    }

    if (_hasError || _imageData == null) {
      return Container(
        width: widget.width,
        height: widget.height,
        child: widget.errorWidget ?? 
          const Center(child: Icon(Icons.error)),
      );
    }

    return Image.memory(
      _imageData!,
      width: widget.width,
      height: widget.height,
      fit: widget.fit ?? BoxFit.cover,
    );
  }
}

class CdnArtistAvatarWidget extends StatefulWidget {
  final String artistName;
  final double? width;
  final double? height;
  final BoxFit? fit;

  const CdnArtistAvatarWidget({
    Key? key,
    required this.artistName,
    this.width,
    this.height,
    this.fit,
  }) : super(key: key);

  @override
  State<CdnArtistAvatarWidget> createState() => _CdnArtistAvatarWidgetState();
}

class _CdnArtistAvatarWidgetState extends State<CdnArtistAvatarWidget> {
  Uint8List? _imageData;
  bool _isLoading = true;
  bool _hasError = false;

  @override
  void initState() {
    super.initState();
    _loadAvatar();
  }

  Future<void> _loadAvatar() async {
    try {
      setState(() {
        _isLoading = true;
        _hasError = false;
      });

      final avatarData = await CdnService.loadArtistAvatar(widget.artistName);
      
      if (avatarData != null) {
        setState(() {
          _imageData = avatarData;
          _isLoading = false;
        });
      } else {
        setState(() {
          _isLoading = false;
          _hasError = true;
        });
      }
    } catch (e) {
      setState(() {
        _isLoading = false;
        _hasError = true;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return Container(
        width: widget.width,
        height: widget.height,
        child: const Center(child: CircularProgressIndicator()),
      );
    }

    if (_hasError || _imageData == null) {
      return Container(
        width: widget.width,
        height: widget.height,
        child: const Center(child: Icon(Icons.person)),
      );
    }

    return Image.memory(
      _imageData!,
      width: widget.width,
      height: widget.height,
      fit: widget.fit ?? BoxFit.cover,
    );
  }
} 