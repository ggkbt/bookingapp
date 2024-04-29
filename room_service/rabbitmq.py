# /room_service/rabbitmq.py

import json
import traceback
from asyncio import AbstractEventLoop

from aio_pika import connect_robust, IncomingMessage
from aio_pika.abc import AbstractRobustConnection

from room_service.repositories.db_room_repo import RoomRepo
from room_service.services.room_service import RoomService
from room_service.settings import settings


async def process_cancellation(msg: IncomingMessage):
    try:
        data = json.loads(msg.body.decode())
        room_id = data['room_id']
        start_date = data['start_date']
        end_date = data['end_date']
        RoomService(RoomRepo()).free_room_period(room_id, start_date=start_date, end_date=end_date)
    except Exception as e:
        traceback.print_exc()
        print(f"Failed to process message: {e}")
    finally:
        await msg.ack()


async def consume(loop: AbstractEventLoop) -> AbstractRobustConnection:
    connection = await connect_robust(settings.amqp_url, loop=loop)
    channel = await connection.channel()

    cancellation_queue = await channel.declare_queue('room_cancellation_queue', durable=True)

    await cancellation_queue.consume(process_cancellation)
    print('Started RabbitMQ consuming...')

    return connection
