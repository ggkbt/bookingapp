# /room_service/schemas/rooms.py

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from .base_schema import Base


class Room(Base):
    __tablename__ = 'rooms'

    id = Column(UUID(as_uuid=True), primary_key=True)
    room_number = Column(String, unique=True, nullable=False)