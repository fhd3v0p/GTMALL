import requests
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import os
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import requests
import os
import json
from .models import User, TaskCompletion, ReferralInvite, GiveawayChannel, Artist, Product, SubscriptionChannel, City, Giveaway, Category, ArtistLinks
from django.utils import timezone

def check_service_status(url, timeout=5):
    """Проверяет статус сервиса"""
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200
    except:
        return False

def check_postgresql():
    """Проверяет статус PostgreSQL"""
    try:
        import psycopg2
        # Подключаемся к базе данных gtm_db с пользователем h0
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="gtm_db",
            user="h0"
        )
        conn.close()
        return True
    except Exception as e:
        print(f"PostgreSQL check error: {e}")
        return False

def check_redis():
    """Проверяет статус Redis"""
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        return True
    except:
        return False

def get_system_status():
    """Получает статус всех сервисов"""
    return {
        'gtm_api': check_service_status(f"{settings.GTM_API_URL}/health"),
        'minio_api': check_service_status(f"{settings.MINIO_API_URL}/minio/health/live"),
        'minio_admin': check_service_status(f"{settings.MINIO_ADMIN_URL}"),
        'web_server': check_service_status("http://localhost:3003"),
    }

def dashboard(request):
    """Главная страница админ-панели"""
    return render(request, 'admin_panel/dashboard.html')

def telegram_links(request):
    """Управление Telegram-ссылками"""
    return render(request, 'admin_panel/telegram_links.html')

def artists(request):
    """Управление артистами"""
    # Получаем артистов из БД
    artists_data = []
    artists_from_db = Artist.objects.all().prefetch_related('categories', 'cities')
    
    for artist in artists_from_db:
        # Получаем ссылки артиста через OneToOneField
        try:
            links = artist.artistlinks
        except ArtistLinks.DoesNotExist:
            links = None
            
        artists_data.append({
            'id': artist.id,
            'name': artist.name,
            'bio': artist.bio,
            'folder_name': artist.folder_name,
            'avatar_url': artist.avatar_url,
            'categories': [cat.name for cat in artist.categories.all()],
            'cities': [city.name for city in artist.cities.all()],
            'telegram': links.telegram if links else '',
            'instagram': links.instagram if links else '',
            'tiktok': links.tiktok if links else '',
            'pinterest': links.pinterest if links else '',
            'booking_url': links.booking_url if links else '',
            'created_at': artist.created_at
        })
    
    context = {
        'artists': artists_data
    }
    return render(request, 'admin_panel/artists.html', context)

def cities(request):
    """Управление городами"""
    # Здесь можно добавить логику для работы с городами
    cities_data = [
        {'name': 'Москва', 'active': True},
        {'name': 'Санкт-Петербург', 'active': True},
        {'name': 'Екатеринбург', 'active': False},
        {'name': 'Новосибирск', 'active': True},
    ]
    
    context = {
        'cities': cities_data
    }
    return render(request, 'admin_panel/cities.html', context)

def giveaway(request):
    """Управление Giveaway и Telegram-папкой"""
    # Здесь можно добавить логику для работы с Giveaway
    giveaway_data = {
        'active': True,
        'telegram_folder': 'giveaway_telegram',
        'participants': 150,
        'prize': 'Тату-сессия'
    }
    
    context = {
        'giveaway': giveaway_data
    }
    return render(request, 'admin_panel/giveaway.html', context)

def file_manager(request):
    """Управление файлами MinIO"""
    return render(request, 'admin_panel/file_manager.html')

def system_status(request):
    """Статус системы"""
    # Проверяем статус сервисов
    system_status = {
        'minio_admin': check_service_status('http://localhost:9001/minio/health/live'),
        'minio_api': check_service_status('http://localhost:9000/minio/health/live'),
        'gtm_api': check_service_status('http://localhost:3001/health'),
        'postgresql': check_postgresql(),
        'redis': check_redis(),
        'web_server': check_service_status('http://localhost:8888')
    }
    
    context = {
        'system_status': system_status
    }
    return render(request, 'admin_panel/system_status.html', context)

def check_service(url):
    """Проверка статуса сервиса"""
    try:
        response = requests.get(url, timeout=2)
        return {'status': 'online', 'code': response.status_code}
    except:
        return {'status': 'offline', 'code': None}

# API Views
@csrf_exempt
def api_system_status(request):
    """API для получения статуса системы"""
    if request.method == 'GET':
        services = {
            'minio_admin': check_service_status('http://localhost:9001/minio/health/live'),
            'minio_api': check_service_status('http://localhost:9000/minio/health/live'),
            'gtm_api': check_service_status('http://localhost:3001/health'),
            'postgresql': check_postgresql(),
            'redis': check_redis(),
            'web_server': check_service_status('http://localhost:8888')
        }
        return JsonResponse({'success': True, 'data': services})
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def api_telegram_links(request):
    """API для управления Telegram-ссылками"""
    if request.method == 'GET':
        links = [
            {'id': 1, 'name': 'GTM Model', 'url': 'https://t.me/gtm_model'},
            {'id': 2, 'name': 'GTM Giveaway', 'url': 'https://t.me/gtm_giveaway'},
        ]
        return JsonResponse({'success': True, 'data': links})
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def api_artists(request):
    """API для управления артистами"""
    if request.method == 'GET':
        artists = Artist.objects.all()
        data = []
        for artist in artists:
            data.append({
                'id': artist.id,
                'name': artist.name,
                'bio': artist.bio,
                'avatar_url': artist.get_avatar_url(),
                'gallery_urls': artist.get_gallery_urls(),
                'gallery_count': artist.get_gallery_count(),
                'folder_name': artist.folder_name,
                'created_at': artist.created_at.isoformat()
            })
        return JsonResponse({'success': True, 'data': data})
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
@require_http_methods(["POST"])
def api_create_artist(request):
    """API для создания артиста"""
    try:
        data = json.loads(request.body)
        
        # Создаем артиста
        artist = Artist.objects.create(
            name=data['name'],
            bio=data.get('bio', '')
        )
        
        # Добавляем категории
        if 'categories' in data:
            categories = Category.objects.filter(id__in=data['categories'])
            artist.categories.set(categories)
        
        # Добавляем города
        if 'cities' in data:
            cities = City.objects.filter(id__in=data['cities'])
            artist.cities.set(cities)
        
        # Создаем ссылки артиста
        ArtistLinks.objects.create(
            artist=artist,
            telegram=data.get('telegram', ''),
            telegram_url=data.get('telegram_url', ''),
            instagram=data.get('instagram', ''),
            tiktok=data.get('tiktok', ''),
            tiktok_url=data.get('tiktok_url', ''),
            pinterest=data.get('pinterest', ''),
            pinterest_url=data.get('pinterest_url', ''),
            booking_url=data.get('booking_url', ''),
            location_html=data.get('location_html', ''),
            gallery_html=data.get('gallery_html', '')
        )
        
        # Создаем папку в MinIO
        try:
            response = requests.post(
                'http://localhost:3001/api/admin/artists',
                json={
                    'artist_id': artist.id,
                    'name': artist.name,
                    'folder_name': artist.folder_name
                },
                headers={'Content-Type': 'application/json'}
            )
            if response.status_code != 201:
                print(f"Ошибка создания папки в MinIO: {response.status_code}")
        except Exception as e:
            print(f"Ошибка создания папки в MinIO: {e}")
        
        return JsonResponse({
            'success': True,
            'artist_id': artist.id,
            'folder_name': artist.folder_name
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@csrf_exempt
@require_http_methods(["PUT"])
def api_update_artist(request, artist_id):
    """API для обновления артиста"""
    try:
        data = json.loads(request.body)
        artist = Artist.objects.get(id=artist_id)
        
        # Обновляем основные поля
        artist.name = data.get('name', artist.name)
        artist.bio = data.get('bio', artist.bio)
        artist.save()
        
        # Обновляем категории
        if 'categories' in data:
            categories = Category.objects.filter(id__in=data['categories'])
            artist.categories.set(categories)
        
        # Обновляем города
        if 'cities' in data:
            cities = City.objects.filter(id__in=data['cities'])
            artist.cities.set(cities)
        
        # Обновляем ссылки
        try:
            links = artist.artistlinks_set.first()
            if links:
                links.telegram = data.get('telegram', links.telegram)
                links.telegram_url = data.get('telegram_url', links.telegram_url)
                links.instagram = data.get('instagram', links.instagram)
                links.tiktok = data.get('tiktok', links.tiktok)
                links.tiktok_url = data.get('tiktok_url', links.tiktok_url)
                links.pinterest = data.get('pinterest', links.pinterest)
                links.pinterest_url = data.get('pinterest_url', links.pinterest_url)
                links.booking_url = data.get('booking_url', links.booking_url)
                links.location_html = data.get('location_html', links.location_html)
                links.gallery_html = data.get('gallery_html', links.gallery_html)
                links.save()
        except:
            pass
        
        return JsonResponse({'success': True})
        
    except Artist.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Артист не найден'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["DELETE"])
def api_delete_artist(request, artist_id):
    """API для удаления артиста"""
    try:
        artist = Artist.objects.get(id=artist_id)
        
        # Удаляем папку из MinIO
        try:
            response = requests.delete(
                f'http://localhost:3001/api/admin/artists/{artist_id}',
                headers={'Content-Type': 'application/json'}
            )
        except Exception as e:
            print(f"Ошибка удаления папки из MinIO: {e}")
        
        # Удаляем артиста из БД
        artist.delete()
        
        return JsonResponse({'success': True})
        
    except Artist.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Артист не найден'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@csrf_exempt
def api_cities(request):
    """API для управления городами"""
    if request.method == 'GET':
        cities = City.objects.all()
        data = []
        for city in cities:
            data.append({
                'id': city.id,
                'name': city.name,
                'telegram_link': city.telegram_link,
                'is_active': city.is_active,
                'created_at': city.created_at.isoformat()
            })
        return JsonResponse({'success': True, 'data': data})
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def api_giveaway_telegram(request):
    """API для управления Giveaway и Telegram"""
    if request.method == 'GET':
        giveaways = Giveaway.objects.all()
        data = []
        for giveaway in giveaways:
            data.append({
                'id': giveaway.id,
                'name': giveaway.name,
                'prize': giveaway.prize,
                'telegram_folder': giveaway.telegram_folder,
                'status': giveaway.status,
                'current_participants': giveaway.current_participants,
                'max_participants': giveaway.max_participants
            })
        return JsonResponse({'success': True, 'data': data})
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def api_admin_analytics(request):
    """API для аналитики админ-панели"""
    if request.method == 'GET':
        analytics = {
            'total_users': User.objects.count(),
            'total_artists': Artist.objects.count(),
            'total_cities': City.objects.count(),
            'total_giveaways': Giveaway.objects.count(),
            'active_giveaways': Giveaway.objects.filter(status='active').count(),
            'total_products': Product.objects.count(),
            'total_channels': SubscriptionChannel.objects.count()
        }
        return JsonResponse({'success': True, 'data': analytics})
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def api_users(request):
    """API для управления пользователями"""
    if request.method == 'GET':
        users = User.objects.all()
        data = []
        for user in users:
            data.append({
                'user_id': user.user_id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'registered_at': user.registered_at.isoformat(),
                'last_activity': user.last_activity.isoformat()
            })
        return JsonResponse({'success': True, 'data': data})
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def api_products(request):
    """API для управления продуктами"""
    if request.method == 'GET':
        products = Product.objects.all()
        data = []
        for product in products:
            data.append({
                'id': product.id,
                'name': product.name,
                'category': product.category,
                'subcategory': product.subcategory,
                'brand': product.brand,
                'description': product.description,
                'summary': product.summary,
                'price': str(product.price) if product.price else None,
                'old_price': str(product.old_price) if product.old_price else None,
                'discount_percent': product.discount_percent,
                'final_price': str(product.get_final_price()),
                'size_type': product.size_type,
                'size_clothing': product.size_clothing,
                'size_pants': product.size_pants,
                'size_shoes_eu': product.size_shoes_eu,
                'display_size': product.get_display_size(),
                'color': product.color,
                'master_id': product.get_master_id(),
                'master_name': product.get_master_name(),
                'master_telegram': product.master_telegram,
                'avatar': product.get_avatar_url(),
                'gallery': product.get_gallery_urls(),
                'gallery_count': product.get_gallery_count(),
                'is_new': product.is_new,
                'is_available': product.is_available,
                'created_at': product.created_at.isoformat()
            })
        return JsonResponse({'success': True, 'data': data})
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def api_product_sizes(request):
    """API для получения доступных размеров"""
    if request.method == 'GET':
        sizes = {
            'clothing_sizes': ['XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL'],
            'pants_sizes': ['26', '28', '30', '32', '34', '36', '38', '40', '42', '44'],
            'shoes_eu_sizes': list(range(35, 46)),  # EU 35-45
            'size_types': [
                {'value': 'clothing', 'label': 'Одежда'},
                {'value': 'shoes', 'label': 'Обувь'},
                {'value': 'one_size', 'label': 'Один размер'}
            ]
        }
        return JsonResponse({'success': True, 'data': sizes})
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def api_cart_summary(request):
    """API для получения сводки корзины"""
    if request.method == 'GET':
        # Статистика корзины
        from django.db.models import Count, Sum, Avg
        
        cart_stats = {
            'total_users_with_cart': 0,  # Пока заглушка
            'total_items': 0,
            'total_quantity': 0,
            'avg_quantity': 0
        }
        
        # Топ товаров (пока заглушка)
        top_products = []
        
        return JsonResponse({
            'success': True, 
            'data': {
                'cart_statistics': cart_stats,
                'top_products_in_carts': top_products
            }
        })
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def api_categories(request):
    """API для получения категорий"""
    if request.method == 'GET':
        categories = Category.objects.all()
        data = []
        for category in categories:
            data.append({
                'id': category.id,
                'name': category.name,
                'type': category.type,
                'type_display': category.get_type_display()
            })
        return JsonResponse({'success': True, 'data': data})
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def api_products_by_master_and_category(request, master_id, category):
    """API для получения товаров мастера по категории"""
    if request.method == 'GET':
        try:
            # Получаем товары мастера по категории
            products = Product.objects.filter(
                master_id=master_id,
                category=category,
                is_available=True
            )
            
            data = []
            for product in products:
                data.append({
                    'id': product.id,
                    'name': product.name,
                    'category': product.category,
                    'subcategory': product.subcategory,
                    'brand': product.brand,
                    'description': product.description,
                    'summary': product.summary,
                    'price': str(product.price) if product.price else None,
                    'old_price': str(product.old_price) if product.old_price else None,
                    'discount_percent': product.discount_percent,
                    'final_price': str(product.get_final_price()),
                    'size_type': product.size_type,
                    'size_clothing': product.size_clothing,
                    'size_pants': product.size_pants,
                    'size_shoes_eu': product.size_shoes_eu,
                    'display_size': product.get_display_size(),
                    'color': product.color,
                    'master_id': product.get_master_id(),
                    'master_name': product.get_master_name(),
                    'master_telegram': product.master_telegram,
                    'avatar': product.get_avatar_url(),
                    'gallery': product.get_gallery_urls(),
                    'gallery_count': product.get_gallery_count(),
                    'is_new': product.is_new,
                    'is_available': product.is_available,
                    'created_at': product.created_at.isoformat()
                })
            
            return JsonResponse({
                'success': True, 
                'products': data,
                'count': len(data)
            })
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'error': str(e)
            }, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def api_artists_with_images(request):
    """API для получения артистов с изображениями и товарами"""
    if request.method == 'GET':
        try:
            artists = Artist.objects.all()
            data = []
            for artist in artists:
                # Получаем товары артиста
                products = Product.objects.filter(master=artist, is_available=True)
                products_data = []
                for product in products:
                    products_data.append({
                        'id': product.id,
                        'name': product.name,
                        'category': product.category,
                        'subcategory': product.subcategory,
                        'brand': product.brand,
                        'price': str(product.price) if product.price else None,
                        'final_price': str(product.get_final_price()),
                        'avatar': product.get_avatar_url(),
                        'gallery': product.get_gallery_urls(),
                        'gallery_count': product.get_gallery_count(),
                        'is_new': product.is_new,
                        'created_at': product.created_at.isoformat()
                    })
                
                data.append({
                    'id': artist.id,
                    'name': artist.name,
                    'bio': artist.bio,
                    'avatar_url': artist.get_avatar_url(),
                    'gallery_urls': artist.get_gallery_urls(),
                    'gallery_count': artist.get_gallery_count(),
                    'folder_name': artist.folder_name,
                    'products': products_data,
                    'products_count': len(products_data),
                    'created_at': artist.created_at.isoformat()
                })
            
            return JsonResponse({
                'success': True, 
                'data': data,
                'total_artists': len(data)
            })
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'error': str(e)
            }, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
