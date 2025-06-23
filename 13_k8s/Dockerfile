FROM nginx:alpine

# Установим envsubst для подстановки переменных окружения
RUN apk add --no-cache gettext

# Копируем конфиг nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Копируем шаблон HTML
COPY index.template.html /usr/share/nginx/html/index.template.html

# Скрипт запуска, который генерирует HTML с именем пода
CMD ["/bin/sh", "-c", "envsubst '$$POD_NAME' < /usr/share/nginx/html/index.template.html > /usr/share/nginx/html/index.html && nginx -g 'daemon off;'"]
