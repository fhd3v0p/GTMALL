#!/usr/bin/env python3
"""
Скрипт для создания пользователей Django админки
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gtm_admin_panel.settings')
django.setup()

from django.contrib.auth.models import User

def create_admin_users():
    """Создание пользователей админки"""
    
    # Список пользователей для создания
    users = [
        {
            'username': 'admin',
            'email': 'admin@gtm.baby',
            'password': 'gtm_admin_2024',
            'first_name': 'Администратор',
            'last_name': 'GTM',
            'is_staff': True,
            'is_superuser': True,
        },
        {
            'username': 'manager',
            'email': 'manager@gtm.baby',
            'password': 'gtm_manager_2024',
            'first_name': 'Менеджер',
            'last_name': 'GTM',
            'is_staff': True,
            'is_superuser': False,
        },
        {
            'username': 'editor',
            'email': 'editor@gtm.baby',
            'password': 'gtm_editor_2024',
            'first_name': 'Редактор',
            'last_name': 'GTM',
            'is_staff': True,
            'is_superuser': False,
        }
    ]
    
    print("🔧 Создание пользователей Django админки...")
    
    for user_data in users:
        username = user_data['username']
        
        # Проверяем, существует ли пользователь
        if User.objects.filter(username=username).exists():
            print(f"⚠️  Пользователь '{username}' уже существует")
            continue
        
        # Создаем пользователя
        user = User.objects.create_user(
            username=username,
            email=user_data['email'],
            password=user_data['password'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            is_staff=user_data['is_staff'],
            is_superuser=user_data['is_superuser'],
        )
        
        print(f"✅ Создан пользователь: {username}")
        print(f"   Логин: {username}")
        print(f"   Пароль: {user_data['password']}")
        print(f"   Роль: {'Суперпользователь' if user_data['is_superuser'] else 'Персонал'}")
        print()
    
    print("🎉 Все пользователи созданы!")
    print("\n📋 ДОСТУП К АДМИНКЕ:")
    print("URL: http://localhost:8000/admin/")
    print("\n👤 ПОЛЬЗОВАТЕЛИ:")
    print("1. admin / gtm_admin_2024 (Суперпользователь)")
    print("2. manager / gtm_manager_2024 (Менеджер)")
    print("3. editor / gtm_editor_2024 (Редактор)")
    print("4. gtm-admin-i / [ваш пароль] (Суперпользователь)")

if __name__ == '__main__':
    create_admin_users() 