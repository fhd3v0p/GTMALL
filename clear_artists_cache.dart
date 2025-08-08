import 'package:flutter/material.dart';
import 'lib/services/artists_service.dart';

void main() {
  runApp(CacheClearApp());
}

class CacheClearApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Cache Clear',
      home: CacheClearScreen(),
    );
  }
}

class CacheClearScreen extends StatefulWidget {
  @override
  _CacheClearScreenState createState() => _CacheClearScreenState();
}

class _CacheClearScreenState extends State<CacheClearScreen> {
  String _status = 'Готов к очистке кэша';

  Future<void> _clearCache() async {
    setState(() {
      _status = 'Очищаем кэш артистов...';
    });

    try {
      // Очищаем кэш артистов
      ArtistsService.clearCache();
      
      setState(() {
        _status = '✅ Кэш артистов очищен!';
      });
      
      // Ждем немного и показываем статистику
      await Future.delayed(Duration(seconds: 2));
      
      final stats = await ArtistsService.getStats();
      setState(() {
        _status = '📊 Статистика:\n'
            'Города: ${stats['cities_count']}\n'
            'Категории: ${stats['categories_count']}\n'
            'Артисты: ${stats['artists_count']}\n'
            'Размер кэша: ${stats['cache_size']}';
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
        title: Text('Очистка кэша артистов'),
        backgroundColor: Colors.black,
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
              onPressed: _clearCache,
              child: Text('Очистить кэш'),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.red,
                foregroundColor: Colors.white,
              ),
            ),
          ],
        ),
      ),
    );
  }
} 