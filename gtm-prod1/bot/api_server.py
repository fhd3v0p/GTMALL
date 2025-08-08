#!/usr/bin/env python3
"""
GTM API Server
Простой API сервер для обработки запросов от Flutter
"""

import os
import logging
import asyncio
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Импортируем Supabase клиент
from supabase_client import supabase_client

load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Разрешаем CORS для Flutter Web

@app.route('/api/check_subscription', methods=['POST'])
async def check_subscription():
    """Проверка подписки пользователя"""
    try:
        data = request.get_json()
        telegram_id = data.get('telegram_id')
        
        if not telegram_id:
            return jsonify({'error': 'telegram_id is required'}), 400
        
        # Получаем статистику пользователя
        user_stats = await supabase_client.get_user_stats(telegram_id)
        
        return jsonify({
            'success': True,
            'subscription_tickets': user_stats.get('subscription_tickets', 0),
            'referral_tickets': user_stats.get('referral_tickets', 0),
            'total_tickets': user_stats.get('total_tickets', 0),
            'referral_code': user_stats.get('referral_code', ''),
            'ticket_awarded': False,  # Будет обновлено после проверки
            'message': 'Статистика получена'
        })
        
    except Exception as e:
        logger.error(f"Ошибка проверки подписки: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/user_tickets/<int:telegram_id>', methods=['GET'])
async def get_user_tickets(telegram_id):
    """Получение билетов пользователя"""
    try:
        user_stats = await supabase_client.get_user_stats(telegram_id)
        
        return jsonify({
            'subscription_tickets': user_stats.get('subscription_tickets', 0),
            'referral_tickets': user_stats.get('referral_tickets', 0),
            'total_tickets': user_stats.get('total_tickets', 0),
            'referral_code': user_stats.get('referral_code', '')
        })
        
    except Exception as e:
        logger.error(f"Ошибка получения билетов: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/total_tickets_stats', methods=['GET'])
async def get_total_tickets_stats():
    """Получение общей статистики билетов"""
    try:
        stats = await supabase_client.get_tickets_stats()
        
        return jsonify({
            'total_subscription_tickets': stats.get('total_subscription_tickets', 0),
            'total_referral_tickets': stats.get('total_referral_tickets', 0),
            'total_user_tickets': stats.get('total_user_tickets', 0)
        })
        
    except Exception as e:
        logger.error(f"Ошибка получения статистики: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/telegram_bot/check', methods=['POST'])
async def call_telegram_bot_check():
    """Вызов команды /check у Telegram бота"""
    try:
        data = request.get_json()
        telegram_id = data.get('telegram_id')
        
        if not telegram_id:
            return jsonify({'error': 'telegram_id is required'}), 400
        
        # Здесь можно добавить логику вызова бота
        # Пока возвращаем заглушку
        result = await supabase_client.check_subscription_and_award_ticket(telegram_id, True)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Ошибка вызова бота: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Проверка здоровья API"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'GTM API Server'
    })

if __name__ == '__main__':
    port = int(os.getenv('API_PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    logger.info(f"🚀 Запуск GTM API Server на порту {port}")
    app.run(host='0.0.0.0', port=port, debug=debug) 