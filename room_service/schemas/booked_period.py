# /room_service/schemas/booked_period.py

from sqlalchemy import Column, Date, Integer
from sqlalchemy.dialects.postgresql import UUID

from .base_schema import Base


class BookedPeriod(Base):
    __tablename__ = 'booked_period'

    id = Column(Integer, primary_key=True)
    room_id = Column(UUID(as_uuid=True), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    def __repr__(self):
        return f"<BookedPeriod(room_id={self.room_id}, start={self.start_date}, end={self.end_date})>"
