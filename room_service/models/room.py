# /booking_service/models/room.py

from datetime import date
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class Room(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    room_number: str


class CreateRoomRequest(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    room_number: str


class BookRoomRequest(BaseModel):
    start_date: date
    end_date: date


class UpdateRoomRequest(BaseModel):
    room_number: Optional[str] = None
