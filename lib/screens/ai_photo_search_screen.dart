import 'package:flutter/material.dart';
import 'master_cloud_screen.dart' as mcs;
import '../services/telegram_webapp_service.dart';

import '../models/photo_upload_model.dart';
import 'dart:math';
import '../models/master_model.dart';
import 'master_detail_screen.dart';
import 'choose_search_mode_screen.dart';
import 'welcome_screen.dart';

class AiPhotoSearchScreen extends StatefulWidget {
  const AiPhotoSearchScreen({super.key});

  @override
  State<AiPhotoSearchScreen> createState() => _AiPhotoSearchScreenState();
}

class _AiPhotoSearchScreenState extends State<AiPhotoSearchScreen> {
  late List<String> categories;
  String? selectedCategory;
  bool _isUploading = false;
  PhotoUploadModel? _lastUploadedPhoto;

  @override
  void initState() {
    super.initState();
    // Получаем категории из master_cloud_screen.dart
    categories = mcs.MasterCloudScreen.categories;
    selectedCategory = categories.isNotEmpty ? categories.first : null;
    TelegramWebAppService.disableVerticalSwipe();
  }

  Future<void> _uploadPhoto() async {
    if (selectedCategory == null) {
      _showError('Пожалуйста, выберите категорию');
      return;
    }

    // Убираем проверку на Telegram Web App - теперь работает везде

    setState(() {
      _isUploading = true;
    });

    try {
      final photoUpload = await TelegramWebAppService.uploadPhoto({
        'category': selectedCategory!,
        'description': 'AI photo search reference',
      });

      if (photoUpload == true) {
        setState(() {
          _lastUploadedPhoto = null; // Заглушка, так как uploadPhoto возвращает bool
        });
        // Список папок артистов как в master_cloud_screen.dart
        final artistFolders = [
          'assets/artists/Lin++',
          'assets/artists/Blodivamp',
          'assets/artists/Aspergill',
          'assets/artists/EMI',
          'assets/artists/Naidi',
          'assets/artists/MurderDoll',
          'assets/artists/poterya',
          'assets/artists/alena',
          'assets/artists/msk_tattoo_EMI',
          'assets/artists/msk_tattoo_Alena',
        ];
        // Показать экран загрузки с анимацией (welcome-style)
        await Navigator.of(context).push(PageRouteBuilder(
          opaque: false,
          pageBuilder: (_, __, ___) => const _AiPhotoLoadingScreen(),
        ));
        final allMasters = await MasterModel.loadAllFromFolders(artistFolders);
        final filtered = allMasters.where((m) => m.category == selectedCategory).toList();
        if (filtered.isNotEmpty) {
          final randomArtist = filtered[Random().nextInt(filtered.length)];
          Navigator.of(context).push(
            MaterialPageRoute(
              builder: (_) => _AiPhotoResultScreen(master: randomArtist),
            ),
          );
        } else {
          _showError('Не найдено артистов в выбранной категории');
        }
      }
    } catch (e) {
      _showError(e.toString());
    } finally {
      setState(() {
        _isUploading = false;
      });
    }
  }

  void _showError(String message) {
    TelegramWebAppService.showAlert(message);
  }

  void _showSuccess(String message) {
    TelegramWebAppService.showAlert(message);
  }



  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: Stack(
        children: [
          Positioned.fill(
            child: Image.asset(
              'assets/giveaway_banner.png',
              fit: BoxFit.cover,
            ),
          ),
          Positioned.fill(
            child: Container(
              color: Colors.black.withOpacity(0.45), // затемнение на весь баннер
            ),
          ),
          // Кнопка назад
          Positioned(
            top: 36,
            left: 12,
            child: IconButton(
              icon: const Icon(Icons.arrow_back_ios_new_rounded, color: Colors.white, size: 28),
              onPressed: () => Navigator.of(context).maybePop(),
              splashRadius: 24,
            ),
          ),
          Center(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 28),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.camera_alt_rounded, color: Colors.white, size: 60),
                  const SizedBox(height: 24),
                  const Text(
                    'Выберите категорию',
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      color: Colors.white,
                      fontFamily: 'NauryzKeds',
                      fontSize: 26,
                      fontWeight: FontWeight.bold,
                      letterSpacing: 1.2,
                    ),
                  ),
                  const SizedBox(height: 18),
                  DropdownButton<String>(
                    value: selectedCategory,
                    dropdownColor: Colors.black87,
                    iconEnabledColor: Colors.white,
                    style: const TextStyle(
                      color: Colors.white,
                      fontFamily: 'NauryzKeds',
                      fontSize: 18,
                    ),
                    items: categories
                        .map((cat) => DropdownMenuItem(
                              value: cat,
                              child: Text(cat),
                            ))
                        .toList(),
                    onChanged: (val) {
                      setState(() {
                        selectedCategory = val;
                      });
                    },
                  ),
                  const SizedBox(height: 32),
                  const Text(
                    'Загрузите фото-референс\nдля AI-подбора артиста',
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      color: Colors.white,
                      fontFamily: 'NauryzKeds',
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                      letterSpacing: 1.2,
                    ),
                  ),
                  const SizedBox(height: 16),
                  const Text(
                    'Поддерживаются только фото и видео файлы\nМаксимальный размер: 10MB',
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      color: Colors.white70,
                      fontFamily: 'NauryzKeds',
                      fontSize: 14,
                      fontWeight: FontWeight.w300,
                    ),
                  ),
                  const SizedBox(height: 32),
                  // Показываем информацию о последнем загруженном фото
                  if (_lastUploadedPhoto != null) ...[
                    Container(
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: Colors.green.withOpacity(0.2),
                        border: Border.all(color: Colors.green.withOpacity(0.5)),
                      ),
                      child: Column(
                        children: [
                          const Icon(Icons.check_circle, color: Colors.green, size: 24),
                          const SizedBox(height: 8),
                          Text(
                            'Фото загружено: ${_lastUploadedPhoto!.fileName}',
                            style: const TextStyle(
                              color: Colors.green,
                              fontFamily: 'NauryzKeds',
                              fontSize: 14,
                            ),
                          ),
                          Text(
                            'Категория: ${_lastUploadedPhoto!.category}',
                            style: const TextStyle(
                              color: Colors.green,
                              fontFamily: 'NauryzKeds',
                              fontSize: 12,
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 24),
                  ],
                  ElevatedButton.icon(
                    onPressed: _isUploading ? null : _uploadPhoto,
                    icon: _isUploading 
                        ? const SizedBox(
                            width: 20,
                            height: 20,
                            child: CircularProgressIndicator(
                              strokeWidth: 2,
                              valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                            ),
                          )
                        : const Icon(Icons.upload_file_rounded, color: Colors.white),
                    label: Text(
                      _isUploading ? 'Загрузка...' : 'Загрузить фото',
                      style: const TextStyle(
                        fontFamily: 'NauryzKeds',
                        fontWeight: FontWeight.bold,
                        fontSize: 20,
                        color: Colors.white,
                        letterSpacing: 1.1,
                      ),
                    ),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: _isUploading 
                          ? Colors.white.withOpacity(0.04)
                          : Colors.white.withOpacity(0.08),
                      foregroundColor: Colors.white,
                      shape: const RoundedRectangleBorder(
                        borderRadius: BorderRadius.zero,
                        side: BorderSide(color: Colors.white, width: 1.5),
                      ),
                      padding: const EdgeInsets.symmetric(horizontal: 36, vertical: 22),
                      elevation: 0,
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _AiPhotoResultScreen extends StatelessWidget {
  final MasterModel master;
  const _AiPhotoResultScreen({required this.master});
  @override
  Widget build(BuildContext context) {
    final avatarSize = 90.0;
    final ImageProvider<Object> avatarProvider = master.avatar.startsWith('assets/')
        ? AssetImage(master.avatar) as ImageProvider<Object>
        : NetworkImage(master.avatar) as ImageProvider<Object>;
    return Scaffold(
      backgroundColor: Colors.black,
      body: Stack(
        children: [
          Positioned.fill(
            child: Image.asset(
              'assets/giveaway_banner.png',
              fit: BoxFit.cover,
            ),
          ),
          Positioned.fill(
            child: Container(
              color: Colors.black.withOpacity(0.45),
            ),
          ),
          Positioned(
            top: 36,
            left: 12,
            child: IconButton(
              icon: const Icon(Icons.arrow_back_ios_new_rounded, color: Colors.white, size: 28),
              onPressed: () => Navigator.of(context).maybePop(),
              splashRadius: 24,
            ),
          ),
          Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Container(
                  padding: const EdgeInsets.all(4),
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    border: Border.all(color: Colors.white, width: 2),
                    color: const Color(0xFFF3E0E6),
                  ),
                  child: CircleAvatar(
                    backgroundImage: avatarProvider,
                    radius: avatarSize / 2.3,
                    backgroundColor: Colors.transparent,
                  ),
                ),
                const SizedBox(height: 24),
                Text(
                  master.name,
                  style: const TextStyle(
                    color: Colors.white,
                    fontFamily: 'NauryzKeds',
                    fontSize: 22,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 32),
                _DetailModeButton(
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => MasterDetailScreen(master: master),
                      ),
                    );
                  },
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _AiPhotoLoadingScreen extends StatefulWidget {
  const _AiPhotoLoadingScreen();
  @override
  State<_AiPhotoLoadingScreen> createState() => _AiPhotoLoadingScreenState();
}
class _AiPhotoLoadingScreenState extends State<_AiPhotoLoadingScreen> with TickerProviderStateMixin {
  late final AnimationController _pulseController;
  late final Animation<double> _pulseAnimation;
  double _orbitAngle = 0.0;
  final List<String> avatars = [
    'assets/avatar1.png',
    'assets/avatar2.png',
    'assets/avatar3.png',
    'assets/avatar4.png',
    'assets/avatar5.png',
    'assets/avatar6.png',
  ];
  @override
  void initState() {
    super.initState();
    _pulseController = AnimationController(
      duration: const Duration(seconds: 2),
      vsync: this,
    )..repeat(reverse: true);
    _pulseAnimation = Tween<double>(begin: 0.95, end: 1.05).animate(
      CurvedAnimation(parent: _pulseController, curve: Curves.easeInOut),
    );
    _startOrbitAnimation();
    // Имитация загрузки 2.5 сек
    Future.delayed(const Duration(milliseconds: 2500), () {
      if (mounted) Navigator.of(context).pop();
    });
  }
  void _startOrbitAnimation() {
    const double baseSpeed = 0.012;
    const Duration frameDuration = Duration(milliseconds: 16);
    void tick() {
      if (!mounted) return;
      _orbitAngle += baseSpeed;
      if (_orbitAngle > 2 * pi) {
        _orbitAngle -= 2 * pi;
      }
      setState(() {});
      Future.delayed(frameDuration, tick);
    }
    tick();
  }
  @override
  void dispose() {
    _pulseController.dispose();
    super.dispose();
  }
  Offset calculateOrbitPosition(double angle, double radius) {
    return Offset(radius * cos(angle), radius * sin(angle));
  }
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black.withOpacity(0.7),
      body: Center(
        child: SizedBox(
          width: 320,
          height: 320,
          child: AnimatedBuilder(
            animation: _pulseController,
            builder: (context, _) {
              return Stack(
                alignment: Alignment.center,
                children: [
                  CustomPaint(
                    size: const Size(320, 320),
                    painter: DottedCirclePainter(),
                  ),
                  Transform.scale(
                    scale: _pulseAnimation.value,
                    child: Container(
                      width: 224,
                      height: 224,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        color: const Color(0xFFFF6EC7).withOpacity(0.4),
                      ),
                    ),
                  ),
                  Transform.scale(
                    scale: _pulseAnimation.value,
                    child: Container(
                      width: 120,
                      height: 120,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        color: const Color(0xFFFF6EC7).withOpacity(0.85),
                      ),
                    ),
                  ),
                  Container(
                    width: 320,
                    height: 320,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      color: const Color(0xFFFFB3E6).withOpacity(0.2),
                    ),
                  ),
                  for (int i = 0; i < 3; i++)
                    Transform.translate(
                      offset: calculateOrbitPosition(
                          _orbitAngle + (i * 2 * pi / 3), 160),
                      child: _framedMemoji(avatars[i]),
                    ),
                  for (int i = 0; i < 2; i++)
                    Transform.translate(
                      offset: calculateOrbitPosition(
                          -_orbitAngle + (i * pi), 112),
                      child: _framedMemoji(avatars[3 + i]),
                    ),
                  Transform.translate(
                    offset: calculateOrbitPosition(_orbitAngle, 86),
                    child: _framedMemoji(avatars[5]),
                  ),
                  Container(
                    padding: const EdgeInsets.all(3),
                    decoration: const BoxDecoration(
                      color: Color(0xFFF3E0E6),
                      shape: BoxShape.circle,
                    ),
                    child: const CircleAvatar(
                      radius: 36,
                      backgroundImage: AssetImage('assets/center_memoji.png'),
                      backgroundColor: Color(0xFF33272D),
                    ),
                  ),
                ],
              );
            },
          ),
        ),
      ),
    );
  }
  Widget _framedMemoji(String path) {
    return Container(
      padding: const EdgeInsets.all(2),
      decoration: const BoxDecoration(
        color: Color(0xFFF3E0E6),
        shape: BoxShape.circle,
      ),
      child: CircleAvatar(
        radius: 20,
        backgroundImage: AssetImage(path),
        backgroundColor: Colors.black,
      ),
    );
  }
}

class _DetailModeButton extends StatelessWidget {
  final VoidCallback onTap;
  final bool selected;
  const _DetailModeButton({required this.onTap, this.selected = false});
  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 180),
        width: double.infinity,
        padding: const EdgeInsets.symmetric(vertical: 28, horizontal: 18),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.zero,
          color: Colors.black.withOpacity(selected ? 0.45 : 0.45),
          border: Border.all(
            color: selected ? const Color(0xFFFF6EC7) : Colors.white,
            width: selected ? 3 : 1.5,
          ),
          boxShadow: selected
              ? [
                  BoxShadow(
                    color: const Color(0xFFFF6EC7).withOpacity(0.25),
                    blurRadius: 16,
                  ),
                ]
              : [],
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: const [
            Icon(Icons.arrow_forward, color: Colors.white, size: 32),
            SizedBox(width: 18),
            Text(
              'Подробнее',
              style: TextStyle(
                color: Colors.white,
                fontFamily: 'OpenSans',
                fontWeight: FontWeight.bold,
                fontSize: 22,
                letterSpacing: 1.1,
              ),
            ),
          ],
        ),
      ),
    );
  }
}