#!/bin/sh

uvicorn booking_service.main:app --host 0.0.0.0 --port ${SERVICE_PORT}