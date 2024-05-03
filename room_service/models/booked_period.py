# /booking_service/models/booked_period.py

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BookedPeriod(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    room_id: UUID
    start_date: date
    end_date: date
