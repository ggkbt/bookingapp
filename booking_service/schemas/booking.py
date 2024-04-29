# /booking_service/schemas/booking.py

from sqlalchemy import Column, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID

from booking_service.models.booking import BookingStatuses
from booking_service.schemas.base_schema import Base


class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(UUID(as_uuid=True), primary_key=True)
    room_id = Column(UUID(as_uuid=True), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(Enum(BookingStatuses), nullable=False)

    def __repr__(self):
        return f"<Booking {self.id} {self.room_number}>"
