import 'package:flutter/material.dart';
import 'lib/services/artists_service.dart';

void main() {
  runApp(CacheClearApp());
}

class CacheClearApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Force Cache Clear',
      home: ForceCacheClearScreen(),
    );
  }
}

class ForceCacheClearScreen extends StatefulWidget {
  @override
  _ForceCacheClearScreenState createState() => _ForceCacheClearScreenState();
}

class _ForceCacheClearScreenState extends State<ForceCacheClearScreen> {
  String _status = 'Готов к принудительной очистке кэша';

  Future<void> _forceClearCache() async {
    setState(() {
      _status = 'Принудительно очищаем кэш артистов...';
    });

    try {
      // Принудительно очищаем кэш
      ArtistsService.forceClearCache();
      
      setState(() {
        _status = '✅ Кэш принудительно очищен!\n\nТеперь перезапустите приложение';
      });
      
    } catch (e) {
      setState(() {
        _status = '❌ Ошибка: $e';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Принудительная очистка кэша'),
        backgroundColor: Colors.red,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              _status,
              style: TextStyle(fontSize: 18),
              textAlign: TextAlign.center,
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: _forceClearCache,
              child: Text('Принудительно очистить кэш'),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.red,
                foregroundColor: Colors.white,
              ),
            ),
            SizedBox(height: 20),
            Text(
              'После очистки кэша:\n1. Перезапустите приложение\n2. Проверьте категорию GTM BRAND\n3. Артист GTM должен быть только там',
              style: TextStyle(fontSize: 14, color: Colors.grey),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }
} 