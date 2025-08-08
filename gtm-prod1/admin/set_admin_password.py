#!/usr/bin/env python3
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gtm_admin_panel.settings')
django.setup()

from django.contrib.auth.models import User

def set_admin_password():
    try:
        # Находим пользователя admin
        admin_user = User.objects.get(username='admin')
        admin_user.set_password('gtm_admin_2024')
        admin_user.save()
        print("✅ Пароль для пользователя 'admin' установлен: gtm_admin_2024")
        
        # Находим пользователя gtm-admin
        gtm_admin_user = User.objects.get(username='gtm-admin')
        gtm_admin_user.set_password('gtm_admin_2024')
        gtm_admin_user.save()
        print("✅ Пароль для пользователя 'gtm-admin' установлен: gtm_admin_2024")
        
    except User.DoesNotExist:
        print("❌ Пользователь не найден")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == '__main__':
    set_admin_password() 