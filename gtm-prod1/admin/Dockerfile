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

# Создание директорий для статических файлов и медиа
RUN mkdir -p /app/static /app/media

# Сборка статических файлов
RUN python manage.py collectstatic --noinput

# Установка прав доступа
RUN chmod +x /app/manage.py

# Открытие порта
EXPOSE 8000

# Запуск Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] 