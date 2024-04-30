#!/bin/sh

uvicorn room_service.main:app --host 0.0.0.0 --port ${PORT}