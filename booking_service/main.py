# /booking_service/main.py

from fastapi import FastAPI

from booking_service.auth.keycloak_router import keycloak_router
from booking_service.endpoints.booking_router import booking_router
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title='Booking Service')

app.include_router(booking_router, prefix='/api')
app.include_router(keycloak_router, prefix='/auth')

Instrumentator().instrument(app).expose(app)
