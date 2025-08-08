# GTM API main (Flask)
# Скопируйте сюда ваш основной api_main.py
#!/usr/bin/env python3
"""
GTM API Server - Единый функциональный сервер на PostgreSQL
Объединяет лучшие функции всех версий API
"""

import os
import json
import logging
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from functools import wraps
import base64
import uuid
import mimetypes

import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Импортируем единую конфигурацию
from config import config

# Настройка логирования
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format=config.LOG_FORMAT
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, origins=config.CORS_ORIGINS)

# Настройки файлового хранилища
os.makedirs(config.UPLOAD_DIR, exist_ok=True)
os.makedirs(os.path.join(config.UPLOAD_DIR, 'avatars'), exist_ok=True)
os.makedirs(os.path.join(config.UPLOAD_DIR, 'gallery'), exist_ok=True)
os.makedirs(os.path.join(config.UPLOAD_DIR, 'products'), exist_ok=True)

def get_db_connection():
    """Получение подключения к базе данных"""
    return psycopg2.connect(config.DATABASE_URL)

def log_api_call(f):
    """Декоратор для логирования API вызовов"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        logger.info(f"API Call: {request.method} {request.path} - {request.remote_addr}")
        return f(*args, **kwargs)
    return decorated_function

class FileStorage:
    """Абстракция для файлового хранилища"""
    
    def __init__(self):
        self.base_url = f"{config.API_BASE_URL}/files"
        
    def upload_file(self, file_data: bytes, file_name: str, content_type: str = None, category: str = "general") -> Optional[str]:
        """Загрузка файла"""
        try:
            if not content_type:
                content_type = mimetypes.guess_type(file_name)[0] or 'application/octet-stream'
            
            # Генерируем уникальное имя файла
            file_extension = os.path.splitext(file_name)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            
            # Определяем путь для сохранения
            if category == "avatar":
                file_path = os.path.join(config.UPLOAD_DIR, "avatars", unique_filename)
            elif category == "gallery":
                file_path = os.path.join(config.UPLOAD_DIR, "gallery", unique_filename)
            elif category == "product":
                file_path = os.path.join(config.UPLOAD_DIR, "products", unique_filename)
            else:
                file_path = os.path.join(config.UPLOAD_DIR, unique_filename)
            
            # Сохраняем файл
            with open(file_path, 'wb') as f:
                f.write(file_data)
            
            # Возвращаем URL файла
            file_url = f"{self.base_url}/{category}/{unique_filename}"
            logger.info(f"File uploaded successfully: {file_url}")
            return file_url
            
        except Exception as e:
            logger.error(f"Error uploading file: {e}")
            return None

# Инициализируем файловое хранилище
file_storage = FileStorage()

# ============================================================================
# ОСНОВНЫЕ ЭНДПОИНТЫ
# ============================================================================

@app.route('/api/health', methods=['GET'])
@log_api_call
def health_check():
    """Проверка здоровья системы"""
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.now().isoformat(),
            'version': config.VERSION,
            'environment': config.ENVIRONMENT
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/health', methods=['GET'])
def health_check_root():
    """Корневая проверка здоровья"""
    return health_check()

@app.route('/api/', methods=['GET'])
@log_api_call
def api_root():
    """Корневой эндпоинт API"""
    return jsonify({
        'message': f'{config.PROJECT_NAME} API Server v{config.VERSION}',
        'status': 'running',
        'database': 'PostgreSQL',
        'environment': config.ENVIRONMENT,
        'endpoints': {
            'health': '/api/health',
            'masters': '/api/masters',
            'artists': '/api/admin/artists',
            'products': '/api/products',
            'users': '/api/user/<user_id>/stats',
            'admin': '/api/admin/*',
            'giveaway': '/api/giveaway/*',
            'referral': '/api/referral/*'
        }
    })

@app.route('/', methods=['GET'])
def root():
    """Корневой эндпоинт"""
    return jsonify({
        'message': config.PROJECT_NAME,
        'version': config.VERSION,
        'environment': config.ENVIRONMENT,
        'endpoints': {
            'health': '/api/health',
            'artists': '/api/admin/artists',
            'masters': '/api/masters'
        }
    })

# ============================================================================
# ФАЙЛОВЫЙ СЕРВИС
# ============================================================================

@app.route('/files/<category>/<filename>')
def serve_file(category, filename):
    """Сервис для раздачи файлов"""
    try:
        file_path = os.path.join(config.UPLOAD_DIR, category, filename)
        if os.path.exists(file_path):
            return send_from_directory(os.path.join(config.UPLOAD_DIR, category), filename)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        logger.error(f"Error serving file: {e}")
        return jsonify({'error': 'Internal server error'}), 500

# ============================================================================
# КОНФИГУРАЦИЯ
# ============================================================================

@app.route('/api/config', methods=['GET'])
@log_api_call
def get_config():
    """Получение конфигурации (только для админов)"""
    try:
        # Проверяем API ключ если требуется
        if config.API_KEY_REQUIRED:
            api_key = request.headers.get(config.API_KEY_HEADER)
            if not api_key:
                return jsonify({'error': 'API key required'}), 401
        
        return jsonify(config.get_summary())
    except Exception as e:
        logger.error(f"Error getting config: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/config/validate', methods=['GET'])
@log_api_call
def validate_config():
    """Проверка конфигурации"""
    try:
        validation_result = config.validate()
        return jsonify(validation_result)
    except Exception as e:
        logger.error(f"Error validating config: {e}")
        return jsonify({'error': str(e)}), 500

# ============================================================================
# МАСТЕРЫ И АРТИСТЫ
# ============================================================================

@app.route('/api/masters', methods=['GET'])
@log_api_call
def get_masters():
    """Получение списка мастеров с фильтрацией"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Параметры фильтрации
        city = request.args.get('city')
        category = request.args.get('category')
        
        # Базовый запрос
        query = """
            SELECT a.id, a.name, a.bio, a.avatar_url, a.telegram, a.telegram_url,
                   a.tiktok, a.tiktok_url, a.pinterest, a.pinterest_url,
                   a.booking_url, a.location_html, a.gallery_html
            FROM artists a
            WHERE a.is_active = true
        """
        params = []
        
        # Добавляем фильтры
        if city:
            query += """
                AND EXISTS (
                    SELECT 1 FROM artist_cities ac 
                    JOIN cities c ON ac.city_id = c.id 
                    WHERE ac.artist_id = a.id AND c.name = %s
                )
            """
            params.append(city)
        
        if category:
            query += """
                AND EXISTS (
                    SELECT 1 FROM artist_categories ac 
                    JOIN categories c ON ac.category_id = c.id 
                    WHERE ac.artist_id = a.id AND c.name = %s
                )
            """
            params.append(category)
        
        query += " ORDER BY a.name"
        
        cursor.execute(query, params)
        artists = cursor.fetchall()
        
        # Преобразуем в формат для фронтенда
        masters = []
        for artist in artists:
            # Получаем категории
            cursor.execute("""
                SELECT c.name FROM artist_categories ac 
                JOIN categories c ON ac.category_id = c.id 
                WHERE ac.artist_id = %s
            """, (artist['id'],))
            categories = [row['name'] for row in cursor.fetchall()]
            
            # Получаем города
            cursor.execute("""
                SELECT c.name FROM artist_cities ac 
                JOIN cities c ON ac.city_id = c.id 
                WHERE ac.artist_id = %s
            """, (artist['id'],))
            cities = [row['name'] for row in cursor.fetchall()]
            
            master = {
                'id': artist['id'],
                'name': artist['name'],
                'bio': artist['bio'],
                'avatar': artist['avatar_url'],
                'category': categories[0] if categories else '',
                'categories': categories,
                'city': cities[0] if cities else '',
                'cities': cities,
                'telegram': artist['telegram'],
                'telegramUrl': artist['telegram_url'],
                'tiktok': artist['tiktok'],
                'tiktokUrl': artist['tiktok_url'],
                'pinterest': artist['pinterest'],
                'pinterestUrl': artist['pinterest_url'],
                'bookingUrl': artist['booking_url'],
                'locationHtml': artist['location_html'],
                'galleryHtml': artist['gallery_html']
            }
            masters.append(master)
        
        cursor.close()
        conn.close()
        
        return jsonify(masters)
    except Exception as e:
        logger.error(f"Error getting masters: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/masters/<int:master_id>/rating', methods=['GET'])
@log_api_call
def get_master_rating(master_id):
    """Получение рейтинга мастера"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT AVG(rating) as average_rating, COUNT(*) as total_ratings
            FROM master_ratings 
            WHERE master_id = %s
        """, (master_id,))
        
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        return jsonify({
            'master_id': master_id,
            'average_rating': float(result['average_rating']) if result['average_rating'] else 0,
            'total_ratings': result['total_ratings']
        })
    except Exception as e:
        logger.error(f"Error getting master rating: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/masters/<int:master_id>/rate', methods=['POST'])
@log_api_call
def rate_master(master_id):
    """Оценка мастера"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        rating = data.get('rating')
        comment = data.get('comment', '')
        
        if not user_id or not rating:
            return jsonify({'error': 'Missing user_id or rating'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO master_ratings (master_id, user_id, rating, comment)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (master_id, user_id) 
            DO UPDATE SET rating = EXCLUDED.rating, comment = EXCLUDED.comment
        """, (master_id, user_id, rating, comment))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Rating submitted successfully'})
    except Exception as e:
        logger.error(f"Error rating master: {e}")
        return jsonify({'error': str(e)}), 500

# ============================================================================
# АДМИН ПАНЕЛЬ ДЛЯ АРТИСТОВ
# ============================================================================

@app.route('/api/admin/artists', methods=['GET'])
@log_api_call
def get_artists():
    """Получение всех артистов (админ)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT id, name, bio, avatar_url, telegram, telegram_url,
                   tiktok, tiktok_url, pinterest, pinterest_url,
                   booking_url, location_html, gallery_html, created_at
            FROM artists 
            ORDER BY name
        """)
        
        artists = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify([dict(artist) for artist in artists])
    except Exception as e:
        logger.error(f"Error getting artists: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/artists', methods=['POST'])
@log_api_call
def create_artist():
    """Создание нового артиста"""
    try:
        data = request.get_json()
        name = data.get('name')
        bio = data.get('bio')
        
        if not name:
            return jsonify({'error': 'Name is required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO artists (name, bio) 
            VALUES (%s, %s) 
            RETURNING id
        """, (name, bio))
        
        artist_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            'message': 'Artist created successfully',
            'artist_id': artist_id
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating artist: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/artists/<int:artist_id>', methods=['GET'])
@log_api_call
def get_artist(artist_id):
    """Получение артиста по ID"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT id, name, bio, avatar_url, telegram, telegram_url,
                   tiktok, tiktok_url, pinterest, pinterest_url,
                   booking_url, location_html, gallery_html, created_at
            FROM artists 
            WHERE id = %s
        """, (artist_id,))
        
        artist = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not artist:
            return jsonify({'error': 'Artist not found'}), 404
        
        return jsonify(dict(artist))
    except Exception as e:
        logger.error(f"Error getting artist: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/artists/<int:artist_id>', methods=['PUT'])
@log_api_call
def update_artist(artist_id):
    """Обновление артиста"""
    try:
        data = request.get_json()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE artists 
            SET name = %s, bio = %s, telegram = %s, telegram_url = %s,
                tiktok = %s, tiktok_url = %s, pinterest = %s, pinterest_url = %s,
                booking_url = %s, location_html = %s, gallery_html = %s
            WHERE id = %s
        """, (
            data.get('name'), data.get('bio'), data.get('telegram'), data.get('telegram_url'),
            data.get('tiktok'), data.get('tiktok_url'), data.get('pinterest'), data.get('pinterest_url'),
            data.get('booking_url'), data.get('location_html'), data.get('gallery_html'), artist_id
        ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Artist updated successfully'})
    except Exception as e:
        logger.error(f"Error updating artist: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/artists/<int:artist_id>', methods=['DELETE'])
@log_api_call
def delete_artist(artist_id):
    """Удаление артиста"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM artists WHERE id = %s", (artist_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Artist deleted successfully'})
    except Exception as e:
        logger.error(f"Error deleting artist: {e}")
        return jsonify({'error': str(e)}), 500

# ============================================================================
# ЗАГРУЗКА ФАЙЛОВ
# ============================================================================

@app.route('/api/admin/artists/<int:artist_id>/avatar', methods=['POST'])
@log_api_call
def upload_artist_avatar(artist_id):
    """Загрузка аватара артиста"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Проверяем тип файла
        if not file.filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            return jsonify({'error': 'Invalid file type. Only images are allowed.'}), 400
        
        # Читаем файл
        file_data = file.read()
        
        # Загружаем файл
        avatar_url = file_storage.upload_file(file_data, file.filename, category="avatar")
        
        if not avatar_url:
            return jsonify({'error': 'Failed to upload avatar'}), 500
        
        # Обновляем URL в базе данных
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE artists SET avatar_url = %s WHERE id = %s
        """, (avatar_url, artist_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            'message': 'Avatar uploaded successfully',
            'avatar_url': avatar_url
        })
        
    except Exception as e:
        logger.error(f"Error uploading avatar: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/artists/<int:artist_id>/gallery', methods=['POST'])
@log_api_call
def upload_gallery_image(artist_id):
    """Загрузка изображения в галерею"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Проверяем тип файла
        if not file.filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            return jsonify({'error': 'Invalid file type. Only images are allowed.'}), 400
        
        # Читаем файл
        file_data = file.read()
        
        # Загружаем файл
        image_url = file_storage.upload_file(file_data, file.filename, category="gallery")
        
        if not image_url:
            return jsonify({'error': 'Failed to upload image'}), 500
        
        return jsonify({
            'message': 'Gallery image uploaded successfully',
            'image_url': image_url
        })
        
    except Exception as e:
        logger.error(f"Error uploading gallery image: {e}")
        return jsonify({'error': str(e)}), 500

# ============================================================================
# КАТЕГОРИИ И ГОРОДА
# ============================================================================

@app.route('/api/categories', methods=['GET'])
@log_api_call
def get_categories():
    """Получение всех категорий"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT id, name, type, created_at 
            FROM categories 
            ORDER BY type, name
        """)
        categories = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        # Группируем категории по типу
        products = []
        services = []
        
        for category in categories:
            cat_dict = dict(category)
            if cat_dict['type'] == 'product':
                products.append(cat_dict)
            else:
                services.append(cat_dict)
        
        return jsonify({
            'products': products,
            'services': services,
            'all': [dict(category) for category in categories]
        })
    except Exception as e:
        logger.error(f"Error getting categories: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/cities', methods=['GET'])
@log_api_call
def get_cities():
    """Получение всех городов"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("SELECT id, name FROM cities ORDER BY name")
        cities = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify([dict(city) for city in cities])
    except Exception as e:
        logger.error(f"Error getting cities: {e}")
        return jsonify({'error': str(e)}), 500

# ============================================================================
# ПОЛЬЗОВАТЕЛИ И СТАТИСТИКА
# ============================================================================

@app.route('/api/user/<int:user_id>/tickets', methods=['GET'])
@log_api_call
def get_user_tickets(user_id):
    """Получение билетов пользователя"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Получаем информацию о пользователе и билетах
        cursor.execute("""
            SELECT telegram_id, username, first_name, tickets_count, 
                   has_subscription_ticket, referral_code
            FROM users 
            WHERE telegram_id = %s
        """, (user_id,))
        
        user = cursor.fetchone()
        if not user:
            # Создаем нового пользователя если не найден
            cursor.execute("""
                INSERT INTO users (telegram_id, tickets_count, has_subscription_ticket)
                VALUES (%s, 0, false)
                RETURNING telegram_id, username, first_name, tickets_count, 
                         has_subscription_ticket, referral_code
            """, (user_id,))
            user = cursor.fetchone()
            conn.commit()
        
        # Получаем общее количество билетов
        cursor.execute("""
            SELECT SUM(tickets_count) as total_tickets FROM users
        """)
        
        total_result = cursor.fetchone()
        total_tickets = total_result['total_tickets'] if total_result and total_result['total_tickets'] else 0
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'tickets': user['tickets_count'] or 0,
            'total_tickets': total_tickets,
            'username': user['username'] or '',
            'subscription_tickets': 1 if user['has_subscription_ticket'] else 0,
            'referral_tickets': max(0, (user['tickets_count'] or 0) - (1 if user['has_subscription_ticket'] else 0)),
            'referral_code': user['referral_code'] or str(user_id)
        })
    except Exception as e:
        logger.error(f"Error getting user tickets: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/user/<int:user_id>/stats', methods=['GET'])
@log_api_call
def get_user_stats(user_id):
    """Получение статистики пользователя"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Основная информация о пользователе
        cursor.execute("""
            SELECT telegram_id, username, first_name, last_name, 
                   created_at, tickets_count, has_subscription_ticket,
                   referral_code
            FROM users 
            WHERE telegram_id = %s
        """, (user_id,))
        
        user = cursor.fetchone()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Подсчитываем приглашенных друзей
        cursor.execute("""
            SELECT COUNT(*) as invited_count
            FROM users 
            WHERE referred_by = %s
        """, (user_id,))
        
        referral_stats = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'user_id': user['telegram_id'],
            'username': user['username'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'registered_at': user['created_at'].isoformat() if user['created_at'] else None,
            'tickets': {
                'total': user['tickets_count'] or 0,
                'subscription': 1 if user['has_subscription_ticket'] else 0,
                'referral': max(0, (user['tickets_count'] or 0) - (1 if user['has_subscription_ticket'] else 0))
            },
            'referrals': {
                'code': user['referral_code'] or str(user_id),
                'invited_count': referral_stats['invited_count'] or 0
            }
        })
    except Exception as e:
        logger.error(f"Error getting user stats: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/referral/<int:user_id>', methods=['GET'])
@log_api_call
def get_referral_info(user_id):
    """Получение реферальной информации"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Информация о пользователе
        cursor.execute("""
            SELECT referral_code, tickets_count, has_subscription_ticket
            FROM users 
            WHERE telegram_id = %s
        """, (user_id,))
        
        user_info = cursor.fetchone()
        if not user_info:
            return jsonify({'error': 'User not found'}), 404
        
        # Приглашенные пользователи
        cursor.execute("""
            SELECT COUNT(*) as invited_count,
                   array_agg(username) as invited_usernames
            FROM users 
            WHERE referred_by = %s
        """, (user_id,))
        
        invited_stats = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        referral_tickets = max(0, (user_info['tickets_count'] or 0) - (1 if user_info['has_subscription_ticket'] else 0))
        
        return jsonify({
            'user_id': user_id,
            'referral_code': user_info['referral_code'] or str(user_id),
            'referral_link': f"https://t.me/GTM_ROBOT?start={user_info['referral_code'] or user_id}",
            'invited_count': invited_stats['invited_count'] or 0,
            'invited_usernames': invited_stats['invited_usernames'] or [],
            'total_tickets': referral_tickets,
            'total_referral_xp': (invited_stats['invited_count'] or 0) * 100
        })
    except Exception as e:
        logger.error(f"Error getting referral info: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/referral/<int:user_id>/invited', methods=['GET'])
@log_api_call
def get_invited_users(user_id):
    """Получение приглашенных пользователей"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT telegram_id, username, first_name, last_name, created_at
            FROM users 
            WHERE referred_by = %s
            ORDER BY created_at DESC
        """, (user_id,))
        
        invited_users = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify([{
            'user_id': user['telegram_id'],
            'username': user['username'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'joined_at': user['created_at'].isoformat() if user['created_at'] else None
        } for user in invited_users])
    except Exception as e:
        logger.error(f"Error getting invited users: {e}")
        return jsonify({'error': str(e)}), 500

# ============================================================================
# РОЗЫГРЫШИ
# ============================================================================

@app.route('/api/giveaway/prizes', methods=['GET'])
@log_api_call
def get_giveaway_prizes():
    """Получение призов розыгрыша"""
    try:
        prizes = [
            {
                'id': 1,
                'title': 'Золотое яблоко',
                'description': 'Сертификат на 20,000₽ в Золотом Яблоке',
                'value': '20,000₽',
                'quantity': 1,
                'category': 'main'
            },
            {
                'id': 2,
                'title': 'Бьюти-услуги',
                'description': '4 победителя могут выбрать татуировки, пирсинг или стрижки',
                'value': '100,000₽',
                'quantity': 4,
                'category': 'beauty'
            },
            {
                'id': 3,
                'title': 'Telegram Premium',
                'description': '3 подписки на 3 месяца',
                'value': '3,500₽',
                'quantity': 3,
                'category': 'digital'
            },
            {
                'id': 4,
                'title': 'GTM x CRYSQUAD',
                'description': 'Эксклюзивный мерч',
                'value': '3,999₽',
                'quantity': 'limited',
                'category': 'merch'
            },
            {
                'id': 5,
                'title': 'Скидки всем',
                'description': '8% скидка всем участникам с 1+ билетом',
                'value': '8%',
                'quantity': 'unlimited',
                'category': 'discount'
            }
        ]
        
        return jsonify({
            'prizes': prizes,
            'total_value': '130,000₽+',
            'deadline': '2025-08-11T18:00:00'
        })
    except Exception as e:
        logger.error(f"Error getting giveaway prizes: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/giveaway/status', methods=['GET'])
@log_api_call
def get_giveaway_status():
    """Получение статуса розыгрыша"""
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'error': 'user_id parameter required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Получаем информацию о пользователе
        cursor.execute("""
            SELECT tickets_count, has_subscription_ticket
            FROM users 
            WHERE telegram_id = %s
        """, (int(user_id),))
        
        user = cursor.fetchone()
        if not user:
            # Создаем пользователя если не найден
            cursor.execute("""
                INSERT INTO users (telegram_id, tickets_count, has_subscription_ticket)
                VALUES (%s, 0, false)
                RETURNING tickets_count, has_subscription_ticket
            """, (int(user_id),))
            user = cursor.fetchone()
            conn.commit()
        
        # Подсчитываем приглашенных друзей
        cursor.execute("""
            SELECT COUNT(*) as invited_count
            FROM users 
            WHERE referred_by = %s
        """, (int(user_id),))
        
        invited_stats = cursor.fetchone()
        invited_friends = invited_stats['invited_count'] or 0
        
        cursor.close()
        conn.close()
        
        is_in_folder = user['has_subscription_ticket'] or False
        folder_count = 1 if is_in_folder else 0
        
        return jsonify({
            'is_in_folder': is_in_folder,
            'invited_friends': invited_friends,
            'folder_counter': f"{folder_count}/1",
            'friends_counter': f"{invited_friends}/10",
            'total_tickets': folder_count + invited_friends,
            'giveaway_active': True,
            'deadline': '2025-08-11T18:00:00'
        })
    except Exception as e:
        logger.error(f"Error getting giveaway status: {e}")
        return jsonify({'error': str(e)}), 500

# ============================================================================
# БИЛЕТЫ
# ============================================================================

@app.route('/api/tickets/total', methods=['GET'])
@log_api_call
def get_total_tickets():
    """Получение общего количества билетов"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT 
                SUM(tickets_count) as total_tickets,
                COUNT(*) as total_users,
                COUNT(CASE WHEN has_subscription_ticket THEN 1 END) as subscribed_users
            FROM users
        """)
        
        stats = cursor.fetchone()
        cursor.close()
        conn.close()
        
        return jsonify({
            'total_tickets': stats['total_tickets'] or 0,
            'total_users': stats['total_users'] or 0,
            'subscribed_users': stats['subscribed_users'] or 0
        })
    except Exception as e:
        logger.error(f"Error getting total tickets: {e}")
        return jsonify({'error': str(e)}), 500

# ============================================================================
# ПОДПИСКИ
# ============================================================================

@app.route('/api/check-subscription', methods=['POST'])
@log_api_call
def check_subscription():
    """Проверка подписки пользователя"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        channel_id = data.get('channel_id')
        
        if not user_id or not channel_id:
            return jsonify({'error': 'Missing user_id or channel_id'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT is_active, subscription_type, created_at
            FROM subscriptions 
            WHERE user_id = %s AND channel_id = %s
        """, (user_id, channel_id))
        
        subscription = cursor.fetchone()
        cursor.close()
        conn.close()
        
        return jsonify({
            'user_id': user_id,
            'channel_id': channel_id,
            'is_subscribed': bool(subscription and subscription['is_active']),
            'subscription_type': subscription['subscription_type'] if subscription else None
        })
    except Exception as e:
        logger.error(f"Error checking subscription: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/subscription-channels', methods=['GET'])
@log_api_call
def get_subscription_channels():
    """Получение каналов подписок"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT id, name, channel_id, description, is_active
            FROM subscription_channels 
            WHERE is_active = true
            ORDER BY name
        """)
        
        channels = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify([dict(channel) for channel in channels])
    except Exception as e:
        logger.error(f"Error getting subscription channels: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/telegram_bot/check', methods=['POST'])
@log_api_call  
def telegram_bot_check():
    """Вызов команды /check у Telegram бота"""
    try:
        data = request.get_json()
        telegram_id = data.get('telegram_id')
        
        if not telegram_id:
            return jsonify({'error': 'telegram_id is required'}), 400
        
        # Каналы для проверки подписки (те же что в боте)
        subscription_channels = [
            {'channel_id': -1002088959587, 'channel_name': 'Режь меня всерьёз'},
            {'channel_id': -1001971855072, 'channel_name': 'Чучундра'},
            {'channel_id': -1002133674248, 'channel_name': 'naidenka_tattoo'},
            {'channel_id': -1001508215942, 'channel_name': 'Lin++'},
            {'channel_id': -1001555462429, 'channel_name': 'MurderdOll'},
            {'channel_id': -1002132954014, 'channel_name': 'Потеряшка'},
            {'channel_id': -1001689395571, 'channel_name': 'EMI'},
            {'channel_id': -1001767997947, 'channel_name': 'bloodivamp'},
            {'channel_id': -1001973736826, 'channel_name': 'Gothams top model'},
        ]
        
        # Проверяем подписки через Telegram Bot API
        telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN', '7533650686:AAEU4_nJZHGfzOv9XL4m_fDVt0q3dMDPQX8')
        subscribed_count = 0
        
        for channel in subscription_channels:
            try:
                # Проверяем статус пользователя в канале
                check_url = f"https://api.telegram.org/bot{telegram_bot_token}/getChatMember"
                check_response = requests.get(check_url, params={
                    'chat_id': channel['channel_id'],
                    'user_id': telegram_id
                })
                
                if check_response.status_code == 200:
                    member_data = check_response.json()
                    if member_data.get('ok') and member_data.get('result'):
                        status = member_data['result'].get('status')
                        if status in ['member', 'administrator', 'creator']:
                            subscribed_count += 1
                            
            except Exception as e:
                logger.warning(f"Ошибка проверки канала {channel['channel_name']}: {e}")
        
        # Пользователь подписан на все каналы?
        is_subscribed_to_all = subscribed_count == len(subscription_channels)
        
        # Вызываем функцию Supabase для начисления билета
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT * FROM check_subscription_and_award_ticket(%s, %s)
        """, (telegram_id, is_subscribed_to_all))
        
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if result:
            return jsonify({
                'success': True,
                'subscribed': is_subscribed_to_all,
                'subscribed_channels': subscribed_count,
                'total_channels': len(subscription_channels),
                'ticket_awarded': result.get('ticket_awarded', False),
                'subscription_tickets': result.get('subscription_tickets', 0),
                'referral_tickets': result.get('referral_tickets', 0),
                'total_tickets': result.get('total_tickets', 0),
                'message': f'Подписок: {subscribed_count}/{len(subscription_channels)}'
            })
        else:
            return jsonify({
                'success': False,
                'subscribed': False,
                'ticket_awarded': False,
                'message': 'Ошибка проверки подписки'
            }), 400
        
    except Exception as e:
        logger.error(f"Ошибка вызова telegram bot check: {e}")
        return jsonify({'error': str(e)}), 500

# ============================================================================
# АДМИН ЭНДПОИНТЫ
# ============================================================================

@app.route('/api/admin/users', methods=['GET'])
@log_api_call
def admin_get_users():
    """Получение всех пользователей (админ)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT user_id, username, first_name, last_name, 
                   registered_at, last_activity, referral_count,
                   total_referral_xp, tasks_completed
            FROM users 
            ORDER BY registered_at DESC
        """)
        
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify([dict(user) for user in users])
    except Exception as e:
        logger.error(f"Error getting users: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/analytics', methods=['GET'])
@log_api_call
def admin_get_analytics():
    """Получение аналитики (админ)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Общая статистика
        cursor.execute("SELECT COUNT(*) as total_users FROM users")
        total_users = cursor.fetchone()['total_users']
        
        cursor.execute("SELECT COUNT(*) as total_artists FROM artists")
        total_artists = cursor.fetchone()['total_artists']
        
        cursor.execute("SELECT COUNT(*) as total_tickets FROM tickets")
        total_tickets = cursor.fetchone()['total_tickets']
        
        # Новые пользователи за последние 7 дней
        cursor.execute("""
            SELECT COUNT(*) as new_users_week
            FROM users 
            WHERE registered_at >= CURRENT_DATE - INTERVAL '7 days'
        """)
        new_users_week = cursor.fetchone()['new_users_week']
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'total_users': total_users,
            'total_artists': total_artists,
            'total_tickets': total_tickets,
            'new_users_week': new_users_week
        })
    except Exception as e:
        logger.error(f"Error getting analytics: {e}")
        return jsonify({'error': str(e)}), 500

# ============================================================================
# ЛОГИРОВАНИЕ
# ============================================================================

@app.route('/api/log-referral-stats', methods=['POST'])
@log_api_call
def log_referral_stats():
    """Логирование реферальной статистики"""
    try:
        data = request.get_json()
        if not data or 'user_id' not in data:
            return jsonify({'error': 'user_id required'}), 400
        
        user_id = data['user_id']
        logger.info(f"Logged referral stats for user {user_id}")
        
        return jsonify({'success': True, 'message': 'Referral stats logged'})
    except Exception as e:
        logger.error(f"Error logging referral stats: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/log-task-completion', methods=['POST'])
@log_api_call
def log_task_completion():
    """Логирование выполнения задач"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        user_id = data.get('user_id')
        task_name = data.get('task_name')
        task_number = data.get('task_number')
        
        logger.info(f"Task completed: user={user_id}, task={task_name}, number={task_number}")
        
        return jsonify({'success': True, 'message': 'Task completion logged'})
    except Exception as e:
        logger.error(f"Error logging task completion: {e}")
        return jsonify({'error': str(e)}), 500

# ============================================================================
# LEGACY ЭНДПОИНТЫ ДЛЯ ОБРАТНОЙ СОВМЕСТИМОСТИ
# ============================================================================

@app.route('/api/rating', methods=['GET'])
@log_api_call
def get_rating():
    """Legacy endpoint для получения рейтинга"""
    master_id = request.args.get('master_id')
    user_id = request.args.get('user_id')
    
    if not master_id or not user_id:
        return jsonify({'error': 'master_id and user_id parameters are required'}), 400
    
    return get_master_rating(int(master_id))

@app.route('/api/rate', methods=['POST'])
@log_api_call
def rate_master_legacy():
    """Legacy endpoint для установки рейтинга"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    master_id = data.get('master_id')
    user_id = data.get('user_id')
    rating = data.get('rating')
    
    if not master_id or not user_id or rating is None:
        return jsonify({'error': 'master_id, user_id and rating are required'}), 400
    
    return rate_master(int(master_id))

@app.route('/api/artists', methods=['GET'])
@log_api_call
def get_artists_legacy():
    """Legacy endpoint для получения артистов"""
    return get_masters()

# ============================================================================
# КОРЗИНА
# ============================================================================

@app.route('/api/cart/<user_id>', methods=['GET'])
@log_api_call
def get_user_cart(user_id: str):
    """Получение корзины пользователя"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT uc.*, p.name, p.price, p.avatar, p.master_name
            FROM user_cart uc
            JOIN products p ON uc.product_id = p.id
            WHERE uc.user_id = %s
        """, (user_id,))
        
        cart_items = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify({
            'user_id': user_id,
            'items': [dict(item) for item in cart_items],
            'total_items': len(cart_items)
        })
    except Exception as e:
        logger.error(f"Error getting user cart: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/cart/<user_id>/items', methods=['POST'])
@log_api_call
def add_to_cart(user_id: str):
    """Добавление товара в корзину"""
    try:
        data = request.get_json()
        
        if not data or 'product_id' not in data:
            return jsonify({'error': 'Missing product_id'}), 400
        
        product_id = data['product_id']
        quantity = data.get('quantity', 1)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Проверяем, есть ли уже товар в корзине
        cursor.execute("""
            SELECT quantity FROM user_cart 
            WHERE user_id = %s AND product_id = %s
        """, (user_id, product_id))
        
        existing = cursor.fetchone()
        
        if existing:
            # Обновляем количество
            new_quantity = existing[0] + quantity
            cursor.execute("""
                UPDATE user_cart SET quantity = %s, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = %s AND product_id = %s
            """, (new_quantity, user_id, product_id))
        else:
            # Добавляем новый товар
            cursor.execute("""
                INSERT INTO user_cart (user_id, product_id, quantity)
                VALUES (%s, %s, %s)
            """, (user_id, product_id, quantity))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Added to cart successfully'})
    except Exception as e:
        logger.error(f"Error adding to cart: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/cart/<user_id>/items/<product_id>', methods=['PUT'])
@log_api_call
def update_cart_item(user_id: str, product_id: str):
    """Обновление количества товара в корзине"""
    try:
        data = request.get_json()
        
        if not data or 'quantity' not in data:
            return jsonify({'error': 'Missing quantity'}), 400
        
        quantity = data['quantity']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if quantity <= 0:
            # Удаляем товар если количество <= 0
            cursor.execute("""
                DELETE FROM user_cart 
                WHERE user_id = %s AND product_id = %s
            """, (user_id, product_id))
        else:
            # Обновляем количество
            cursor.execute("""
                UPDATE user_cart SET quantity = %s, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = %s AND product_id = %s
            """, (quantity, user_id, product_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Cart updated successfully'})
    except Exception as e:
        logger.error(f"Error updating cart item: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/cart/<user_id>/items/<product_id>', methods=['DELETE'])
@log_api_call
def remove_from_cart(user_id: str, product_id: str):
    """Удаление товара из корзины"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            DELETE FROM user_cart 
            WHERE user_id = %s AND product_id = %s
        """, (user_id, product_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Removed from cart successfully'})
    except Exception as e:
        logger.error(f"Error removing from cart: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/cart/<user_id>', methods=['DELETE'])
@log_api_call
def clear_cart(user_id: str):
    """Очистка корзины пользователя"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM user_cart WHERE user_id = %s", (user_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Cart cleared successfully'})
    except Exception as e:
        logger.error(f"Error clearing cart: {e}")
        return jsonify({'error': str(e)}), 500

# ============================================================================
# ПРОДАЖИ
# ============================================================================

@app.route('/api/sales', methods=['POST'])
@log_api_call
def log_sale():
    """Логирование продажи"""
    try:
        data = request.get_json()
        
        if not data or 'user_id' not in data or 'product_id' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
        
        user_id = data['user_id']
        product_id = data['product_id']
        quantity = data.get('quantity', 1)
        price = data.get('price', 0)
        discount = data.get('discount', 0)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Получаем информацию о товаре
        cursor.execute("""
            SELECT price FROM products WHERE id = %s
        """, (product_id,))
        
        product_result = cursor.fetchone()
        if not product_result:
            return jsonify({'error': 'Product not found'}), 404
        
        actual_price = product_result[0] or price
        total_amount = actual_price * quantity - discount
        
        # Логируем продажу
        cursor.execute("""
            INSERT INTO sales (user_id, product_id, quantity, price, total_amount, discount)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (user_id, product_id, quantity, actual_price, total_amount, discount))
        
        # Удаляем товар из корзины
        cursor.execute("""
            DELETE FROM user_cart 
            WHERE user_id = %s AND product_id = %s
        """, (user_id, product_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            'message': 'Sale logged successfully',
            'sale_id': cursor.fetchone()[0] if cursor.fetchone() else None
        })
    except Exception as e:
        logger.error(f"Error logging sale: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/sales/<user_id>', methods=['GET'])
@log_api_call
def get_user_sales(user_id: str):
    """Получение продаж пользователя"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT s.*, p.name as product_name, p.avatar
            FROM sales s
            JOIN products p ON s.product_id = p.id
            WHERE s.user_id = %s
            ORDER BY s.created_at DESC
        """, (user_id,))
        
        sales = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify([dict(sale) for sale in sales])
    except Exception as e:
        logger.error(f"Error getting user sales: {e}")
        return jsonify({'error': str(e)}), 500

# ============================================================================
# ТОВАРЫ
# ============================================================================

@app.route('/api/products', methods=['GET'])
@log_api_call
def get_products():
    """Получение всех товаров"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT p.*, 
                   COALESCE(pg.images, '[]') as gallery
            FROM products p
            LEFT JOIN (
                SELECT product_id, 
                       json_agg(image_url) as images
                FROM product_gallery 
                GROUP BY product_id
            ) pg ON p.id = pg.product_id
            WHERE p.is_available = true
            ORDER BY p.created_at DESC
        """)
        
        products = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify([dict(product) for product in products])
    except Exception as e:
        logger.error(f"Error getting products: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/products/<product_id>', methods=['GET'])
@log_api_call
def get_product(product_id: str):
    """Получение конкретного товара"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT p.*, 
                   COALESCE(pg.images, '[]') as gallery
            FROM products p
            LEFT JOIN (
                SELECT product_id, 
                       json_agg(image_url) as images
                FROM product_gallery 
                GROUP BY product_id
            ) pg ON p.id = pg.product_id
            WHERE p.id = %s AND p.is_available = true
        """, (product_id,))
        
        product = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Если галерея пустая, пытаемся получить из JSON поля
        if not product['gallery'] or product['gallery'] == '[]':
            try:
                # Проверяем, есть ли галерея в JSON поле
                if product.get('gallery_json'):
                    import json
                    product['gallery'] = json.loads(product['gallery_json'])
                else:
                    product['gallery'] = []
            except:
                product['gallery'] = []
        
        product = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        return jsonify(dict(product))
    except Exception as e:
        logger.error(f"Error getting product: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/products/category/<category>', methods=['GET'])
@log_api_call
def get_products_by_category(category: str):
    """Получение товаров по категории"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT p.*, 
                   COALESCE(pg.images, '[]') as gallery
            FROM products p
            LEFT JOIN (
                SELECT product_id, 
                       json_agg(image_url) as images
                FROM product_gallery 
                GROUP BY product_id
            ) pg ON p.id = pg.product_id
            WHERE p.category = %s AND p.is_available = true
            ORDER BY p.created_at DESC
        """, (category,))
        
        products = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify([dict(product) for product in products])
    except Exception as e:
        logger.error(f"Error getting products by category: {e}")
        return jsonify({'error': str(e)}), 500

# ============================================================================
# АДМИН ПАНЕЛЬ - ТОВАРЫ (РАСШИРЕННАЯ ВЕРСИЯ)
# ============================================================================

@app.route('/api/admin/products', methods=['GET'])
@log_api_call
def admin_get_products():
    """Получение всех товаров для админки"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT p.*, 
                   COALESCE(pg.images, '[]') as gallery
            FROM products p
            LEFT JOIN (
                SELECT product_id, 
                       json_agg(image_url) as images
                FROM product_gallery 
                GROUP BY product_id
            ) pg ON p.id = pg.product_id
            ORDER BY p.created_at DESC
        """)
        
        products = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify([dict(product) for product in products])
    except Exception as e:
        logger.error(f"Error getting products: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/products/upload-image', methods=['POST'])
@log_api_call
def upload_product_image():
    """Загрузка главной фото товара"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Проверяем тип файла
        if not file.filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            return jsonify({'error': 'Invalid file type. Only images are allowed.'}), 400
        
        # Читаем файл
        file_data = file.read()
        
        # Загружаем файл
        image_url = file_storage.upload_file(file_data, file.filename, category="product")
        
        if not image_url:
            return jsonify({'error': 'Failed to upload image'}), 500
        
        return jsonify({
            'message': 'Product image uploaded successfully',
            'image_url': image_url
        })
        
    except Exception as e:
        logger.error(f"Error uploading product image: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/products/upload-gallery', methods=['POST'])
@log_api_call
def upload_product_gallery():
    """Загрузка галереи товара"""
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No files provided'}), 400
        
        files = request.files.getlist('files')
        if not files or files[0].filename == '':
            return jsonify({'error': 'No files selected'}), 400
        
        uploaded_urls = []
        
        for file in files:
            if file.filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                file_data = file.read()
                image_url = file_storage.upload_file(file_data, file.filename, category="product")
                if image_url:
                    uploaded_urls.append(image_url)
        
        return jsonify({
            'message': f'{len(uploaded_urls)} images uploaded successfully',
            'image_urls': uploaded_urls
        })
        
    except Exception as e:
        logger.error(f"Error uploading product gallery: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/products/create', methods=['POST'])
@log_api_call
def create_product_enhanced():
    """Создание нового товара с расширенными полями"""
    try:
        data = request.get_json()
        
        if not data or 'name' not in data or 'price' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO products (
                id, name, category, brand, description, summary, price, old_price,
                discount_percent, size, size_type, size_clothing, size_pants, 
                size_shoes_eu, color, master_id, master_name, master_telegram, avatar
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            data.get('id'), data.get('name'), data.get('category'), data.get('brand'),
            data.get('description'), data.get('summary'), data.get('price'), data.get('old_price'),
            data.get('discount_percent', 0), data.get('size'), data.get('size_type', 'clothing'),
            data.get('size_clothing'), data.get('size_pants'), data.get('size_shoes_eu'),
            data.get('color'), data.get('master_id'), data.get('master_name'), 
            data.get('master_telegram'), data.get('avatar')
        ))
        
        product_id = cursor.fetchone()[0]
        
        # Добавляем галерею если есть
        if 'gallery' in data and isinstance(data['gallery'], list):
            for image_url in data['gallery']:
                cursor.execute("""
                    INSERT INTO product_gallery (product_id, image_url)
                    VALUES (%s, %s)
                """, (product_id, image_url))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            'message': 'Product created successfully',
            'product_id': product_id
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/products/<product_id>/update', methods=['PUT'])
@log_api_call
def update_product_enhanced(product_id: str):
    """Обновление товара с расширенными полями"""
    try:
        data = request.get_json()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE products 
            SET name = %s, category = %s, brand = %s, description = %s, summary = %s,
                price = %s, old_price = %s, discount_percent = %s, size = %s, size_type = %s,
                size_clothing = %s, size_pants = %s, size_shoes_eu = %s, color = %s,
                master_id = %s, master_name = %s, master_telegram = %s, avatar = %s,
                is_available = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (
            data.get('name'), data.get('category'), data.get('brand'),
            data.get('description'), data.get('summary'), data.get('price'), data.get('old_price'),
            data.get('discount_percent'), data.get('size'), data.get('size_type'),
            data.get('size_clothing'), data.get('size_pants'), data.get('size_shoes_eu'),
            data.get('color'), data.get('master_id'), data.get('master_name'), 
            data.get('master_telegram'), data.get('avatar'), data.get('is_available', True), product_id
        ))
        
        # Обновляем галерею если есть
        if 'gallery' in data:
            cursor.execute("DELETE FROM product_gallery WHERE product_id = %s", (product_id,))
            if isinstance(data['gallery'], list):
                for image_url in data['gallery']:
                    cursor.execute("""
                        INSERT INTO product_gallery (product_id, image_url)
                        VALUES (%s, %s)
                    """, (product_id, image_url))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Product updated successfully'})
    except Exception as e:
        logger.error(f"Error updating product: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/products/<product_id>', methods=['DELETE'])
@log_api_call
def delete_product(product_id: str):
    """Удаление товара"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Удаляем галерею
        cursor.execute("DELETE FROM product_gallery WHERE product_id = %s", (product_id,))
        
        # Удаляем из корзин
        cursor.execute("DELETE FROM user_cart WHERE product_id = %s", (product_id,))
        
        # Удаляем товар
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Product deleted successfully'})
    except Exception as e:
        logger.error(f"Error deleting product: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/products/sizes', methods=['GET'])
@log_api_call
def get_product_sizes():
    """Получение доступных размеров"""
    return jsonify({
        'clothing_sizes': ['XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL'],
        'pants_sizes': ['26', '28', '30', '32', '34', '36', '38', '40', '42', '44'],
        'shoes_eu_sizes': list(range(35, 46)),  # EU 35-45
        'size_types': ['clothing', 'shoes', 'one_size']
    })

@app.route('/api/admin/cart-summary', methods=['GET'])
@log_api_call
def get_cart_summary():
    """Получение сводки корзины для админки"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Общая статистика корзины
        cursor.execute("""
            SELECT 
                COUNT(DISTINCT user_id) as active_users,
                COUNT(*) as total_items,
                SUM(quantity) as total_quantity,
                AVG(quantity) as avg_quantity_per_item
            FROM user_cart
        """)
        
        cart_stats = cursor.fetchone()
        
        # Топ товаров в корзинах
        cursor.execute("""
            SELECT 
                p.name, p.category, p.price,
                COUNT(uc.id) as in_carts_count,
                SUM(uc.quantity) as total_quantity
            FROM user_cart uc
            JOIN products p ON uc.product_id = p.id
            GROUP BY p.id, p.name, p.category, p.price
            ORDER BY in_carts_count DESC
            LIMIT 10
        """)
        
        top_products = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'cart_statistics': dict(cart_stats),
            'top_products_in_carts': [dict(product) for product in top_products]
        })
    except Exception as e:
        logger.error(f"Error getting cart summary: {e}")
        return jsonify({'error': str(e)}), 500

# ============================================================================
# СТАТИСТИКА И АНАЛИТИКА
# ============================================================================

@app.route('/api/admin/statistics', methods=['GET'])
@log_api_call
def get_admin_statistics():
    """Получение статистики для админки"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Общая статистика
        cursor.execute("SELECT COUNT(*) as total_users FROM users")
        total_users = cursor.fetchone()['total_users']
        
        cursor.execute("SELECT COUNT(*) as total_artists FROM artists")
        total_artists = cursor.fetchone()['total_artists']
        
        cursor.execute("SELECT COUNT(*) as total_products FROM products")
        total_products = cursor.fetchone()['total_products']
        
        cursor.execute("SELECT COUNT(*) as total_sales FROM sales")
        total_sales = cursor.fetchone()['total_sales']
        
        # Статистика корзин
        cursor.execute("SELECT COUNT(DISTINCT user_id) as users_with_cart FROM user_cart")
        users_with_cart = cursor.fetchone()['users_with_cart']
        
        cursor.execute("SELECT COUNT(*) as total_cart_items FROM user_cart")
        total_cart_items = cursor.fetchone()['total_cart_items']
        
        # Доходы
        cursor.execute("SELECT COALESCE(SUM(total_amount), 0) as total_revenue FROM sales")
        total_revenue = cursor.fetchone()['total_revenue']
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'users': {
                'total': total_users,
                'with_cart': users_with_cart
            },
            'artists': {
                'total': total_artists
            },
            'products': {
                'total': total_products
            },
            'sales': {
                'total': total_sales,
                'revenue': float(total_revenue)
            },
            'cart': {
                'total_items': total_cart_items
            }
        })
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        return jsonify({'error': str(e)}), 500

# ============================================================================
# ОБРАБОТКА ОШИБОК
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# ============================================================================
# ЗАПУСК СЕРВЕРА
# ============================================================================

if __name__ == '__main__':
    # Проверяем конфигурацию при запуске
    validation = config.validate()
    if not validation['valid']:
        logger.error("Configuration validation failed:")
        for error in validation['errors']:
            logger.error(f"  - {error}")
        exit(1)
    
    if validation['warnings']:
        logger.warning("Configuration warnings:")
        for warning in validation['warnings']:
            logger.warning(f"  - {warning}")
    
    logger.info(f"Starting {config.PROJECT_NAME} API Server v{config.VERSION}")
    logger.info(f"Environment: {config.ENVIRONMENT}")
    logger.info(f"Database: {config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}")
    logger.info(f"Server: {config.API_HOST}:{config.API_PORT}")
    
    app.run(
        host=config.API_HOST, 
        port=config.API_PORT, 
        debug=config.DEBUG
    )