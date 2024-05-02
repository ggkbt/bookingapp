# /booking_service/models/booking.py

import enum
from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BookingStatuses(enum.Enum):
    CREATED = 'created'
    CONFIRMED = 'confirmed'
    CANCELED = 'canceled'
    COMPLETED = 'completed'


class Booking(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    room_id: UUID
    start_date: date
    end_date: date
    status: BookingStatuses


class CreateBookingRequest(BaseModel):
    room_id: UUID
    start_date: date
    end_date: date


class UpdateBookingRequest(BaseModel):
    room_id: Optional[UUID] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[BookingStatuses] = None
