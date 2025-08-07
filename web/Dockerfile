FROM nginx:alpine

# Копирование собранного Flutter приложения
COPY . /usr/share/nginx/html/

# Копирование конфигурации nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Установка прав доступа
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html

# Открытие порта
EXPOSE 80

# Запуск nginx
CMD ["nginx", "-g", "daemon off;"] 