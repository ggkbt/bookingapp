# /booking_service/main.py

from fastapi import FastAPI

from booking_service.endpoints.booking_router import booking_router

app = FastAPI(title='Booking Service')

app.include_router(booking_router, prefix='/api')
