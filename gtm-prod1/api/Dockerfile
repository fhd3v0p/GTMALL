FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копирование requirements
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY . .

# Создание директорий для загрузок и логов
RUN mkdir -p /app/uploads/avatars /app/uploads/gallery /app/uploads/products /app/logs

# Установка прав доступа
RUN chmod +x /app/api_main.py

# Открытие порта
EXPOSE 3001

# Запуск приложения
CMD ["python", "api_main.py"] 