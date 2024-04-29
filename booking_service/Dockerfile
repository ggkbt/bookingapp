# /booking_service/Dockerfile

FROM python:3.10

# Выбор папки, в которой будет вестись работа
WORKDIR /booking

# Установка зависимостей проекта
COPY requirements.txt /booking/
RUN pip install --no-cache-dir --upgrade -r /booking/requirements.txt

# Перенос проекта в образ
COPY /booking_service/ /booking/booking_service

COPY /booking_service/entrypoint.sh /booking/entrypoint.sh

RUN chmod +x /booking/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/booking/entrypoint.sh"]