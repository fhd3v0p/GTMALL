#!/bin/bash

# Скрипт для добавления SSH ключа на сервер 31.56.39.165
# Используйте этот скрипт, если у вас есть другой способ доступа к серверу

SERVER_IP="31.56.39.165"
PUBLIC_KEY_FILE="id_rsa_31_56_39_165.pub"

echo "Добавление SSH ключа на сервер $SERVER_IP..."

# Проверяем, что публичный ключ существует
if [ ! -f "$PUBLIC_KEY_FILE" ]; then
    echo "Ошибка: Файл $PUBLIC_KEY_FILE не найден!"
    exit 1
fi

# Читаем публичный ключ
PUBLIC_KEY=$(cat "$PUBLIC_KEY_FILE")

echo "Публичный ключ:"
echo "$PUBLIC_KEY"
echo ""

echo "Для добавления ключа на сервер выполните следующие команды на сервере $SERVER_IP:"
echo ""
echo "1. Подключитесь к серверу другим способом (например, через пароль)"
echo "2. Выполните команду:"
echo "   echo '$PUBLIC_KEY' >> ~/.ssh/authorized_keys"
echo "3. Установите правильные права:"
echo "   chmod 600 ~/.ssh/authorized_keys"
echo "   chmod 700 ~/.ssh"
echo ""
echo "Или выполните автоматически (если у вас есть доступ по паролю):"
echo "ssh root@$SERVER_IP 'echo \"$PUBLIC_KEY\" >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys && chmod 700 ~/.ssh'" 