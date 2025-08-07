#!/usr/bin/env python3
"""
API для обработки рейтингов артистов из Flutter приложения
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import os

app = Flask(__name__)
CORS(app)  # Разрешаем CORS для Flutter

# Конфигурация Supabase
SUPABASE_URL = "https://rxmtovqxjsvogyywyrha.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4bXRvdnF4anN2b2d5eXd5cmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ1Mjg1NTAsImV4cCI6MjA3MDEwNDU1MH0.gDkJybktFoi486hbIVwppDfmVQlAR0fM4o4Sl1-AxhE"

headers = {
    'apikey': SUPABASE_ANON_KEY,
    'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
    'Content-Type': 'application/json'
}

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
            headers=headers,
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
                    headers=headers,
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
            headers=headers,
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