# /room_service/main.py

import asyncio

from fastapi import FastAPI

from room_service import rabbitmq
from room_service.endpoints.room_router import room_router

app = FastAPI(title='Room Service')


@app.on_event('startup')
def startup():
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(rabbitmq.consume(loop))


app.include_router(room_router, prefix='/api')
