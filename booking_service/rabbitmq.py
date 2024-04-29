# /booking_service/rabbitmq.py

import json

import aio_pika

from booking_service.settings import settings


async def publish_message(queue_name, message):
    connection = await aio_pika.connect_robust(settings.amqp_url)
    async with connection:
        channel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(message).encode()),
            routing_key=queue_name
        )
