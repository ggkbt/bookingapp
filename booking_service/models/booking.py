# /booking_service/models/booking.py

import enum
from datetime import date
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


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
    id: UUID = Field(default_factory=uuid4)
    room_id: UUID
    start_date: date
    end_date: date
