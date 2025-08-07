#!/usr/bin/env python3
"""
API для обработки рейтингов артистов из Flutter приложения
+ Проверка подписок через Telegram Bot API и начисление билета
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import os

app = Flask(__name__)
CORS(app)

# Конфигурация Supabase
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://rxmtovqxjsvogyywyrha.supabase.co")
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY", "")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")

# Telegram Bot
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")

supabase_headers = {
    'apikey': SUPABASE_SERVICE_KEY or SUPABASE_ANON_KEY,
    'Authorization': f'Bearer {SUPABASE_SERVICE_KEY or SUPABASE_ANON_KEY}',
    'Content-Type': 'application/json'
}

SUBSCRIPTION_CHANNELS = [
    -1002088959587,
    -1001971855072,
    -1002133674248,
    -1001508215942,
    -1001555462429,
    -1002132954014,
    -1001689395571,
    -1001767997947,
    -1001973736826,
]

@app.route('/api/check-subscriptions', methods=['POST'])
def check_subscriptions():
    """Проверить подписку пользователя на все каналы и начислить билет 1 раз"""
    try:
        data = request.get_json() or {}
        telegram_id = data.get('telegram_id')
        if not telegram_id:
            return jsonify({'success': False, 'error': 'telegram_id required'}), 400

        if not TELEGRAM_BOT_TOKEN:
            return jsonify({'success': False, 'error': 'BOT TOKEN not configured'}), 500

        # Проверяем подписку на все каналы
        is_all = True
        not_subscribed = []
        for chat_id in SUBSCRIPTION_CHANNELS:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getChatMember"
            resp = requests.get(url, params={'chat_id': chat_id, 'user_id': telegram_id}, timeout=15)
            if resp.status_code != 200:
                is_all = False
                not_subscribed.append(chat_id)
                continue
            member = resp.json().get('result', {})
            status = member.get('status')
            if status not in ('member', 'administrator', 'creator'):
                is_all = False
                not_subscribed.append(chat_id)

        # Вызываем RPC для начисления билета
        rpc_url = f"{SUPABASE_URL}/rest/v1/rpc/check_subscription_and_award_ticket"
        rpc_body = {'p_telegram_id': int(telegram_id), 'p_is_subscribed': bool(is_all)}
        rpc_resp = requests.post(rpc_url, headers=supabase_headers, json=rpc_body, timeout=20)

        payload = {'success': False, 'is_subscribed_to_all': is_all, 'not_subscribed': not_subscribed}

        if rpc_resp.status_code == 200:
            body = rpc_resp.json()
            payload.update(body)
            payload['success'] = True
            return jsonify(payload)
        else:
            return jsonify({**payload, 'error': f'RPC error {rpc_resp.status_code}', 'rpc_body': rpc_resp.text}), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/rate-artist', methods=['POST'])
def rate_artist():
    """API эндпоинт для получения рейтингов из Flutter"""
    try:
        data = request.get_json()
        
        # Валидация данных
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
            
        artist_name = data.get('artist_name')
        user_id = data.get('user_id') 
        rating = data.get('rating')
        comment = data.get('comment', '')
        
        if not all([artist_name, user_id, rating]):
            return jsonify({"success": False, "error": "Missing required fields"}), 400
            
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            return jsonify({"success": False, "error": "Rating must be between 1 and 5"}), 400
        
        print(f"📝 Получен рейтинг от Flutter: {user_id} оценил {artist_name} на {rating} звезд")
        
        # Вызываем RPC функцию в Supabase для добавления рейтинга
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/rpc/add_artist_rating",
            headers=supabase_headers,
            json={
                "artist_name_param": artist_name,
                "user_id_param": str(user_id),
                "rating_param": rating,
                "comment_param": comment if comment else None
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print(f"✅ Рейтинг успешно сохранен для {artist_name}")
                
                # Получаем обновленную статистику
                stats_response = requests.post(
                    f"{SUPABASE_URL}/rest/v1/rpc/get_artist_rating",
                    headers=supabase_headers,
                    json={"artist_name_param": artist_name}
                )
                
                stats = {}
                if stats_response.status_code == 200:
                    stats = stats_response.json()
                
                return jsonify({
                    "success": True,
                    "message": "Rating saved successfully",
                    "stats": stats
                })
            else:
                error = result.get("error", "Unknown error")
                print(f"❌ Ошибка от Supabase: {error}")
                return jsonify({"success": False, "error": error}), 400
        else:
            print(f"❌ Ошибка HTTP от Supabase: {response.status_code}")
            return jsonify({"success": False, "error": f"Supabase error: {response.status_code}"}), 500
            
    except Exception as e:
        print(f"❌ Исключение в rate_artist: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/get-rating/<artist_name>', methods=['GET'])
def get_artist_rating(artist_name):
    """API эндпоинт для получения рейтинга артиста"""
    try:
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/rpc/get_artist_rating",
            headers=supabase_headers,
            json={"artist_name_param": artist_name}
        )
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": f"Failed to get rating: {response.status_code}"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Проверка работоспособности API"""
    return jsonify({"status": "ok", "message": "Rating API is working"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Запускаем Rating API на порту {port}")
    app.run(host='0.0.0.0', port=port, debug=True)