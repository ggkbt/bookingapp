# /room_service/Dockerfile

FROM python:3.10

# Выбор папки, в которой будет вестись работа
WORKDIR /room

# Установка зависимостей проекта
COPY requirements.txt /room/
RUN pip install --no-cache-dir --upgrade -r /room/requirements.txt

# Перенос проекта в образ
COPY /room_service/ /room/room_service

COPY /room_service/entrypoint.sh /room/entrypoint.sh

RUN chmod +x /room/entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["/room/entrypoint.sh"]