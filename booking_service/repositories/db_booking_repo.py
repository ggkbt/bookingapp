# /booking_service/repositories/db_booking_repo.py

from uuid import UUID
from sqlalchemy.orm import Session
from booking_service.database import get_db
from booking_service.models.booking import Booking
from booking_service.schemas.booking import Booking as DBBooking


class BookingRepo:
    db: Session

    def __init__(self) -> None:
        self.db = next(get_db())

    def _map_to_model(self, booking: DBBooking) -> Booking:
        return Booking.from_orm(booking)

    def get_bookings(self) -> list[Booking]:
        bookings = self.db.query(DBBooking).all()
        return [self._map_to_model(b) for b in bookings]

    def get_booking_by_id(self, id: UUID) -> Booking:
        booking = self.db.query(DBBooking).filter(DBBooking.id == id).first()
        if booking is None:
            raise KeyError
        return self._map_to_model(booking)

    def create_booking(self, booking: Booking) -> Booking:
        db_booking = DBBooking(**booking.dict())
        self.db.add(db_booking)
        self.db.commit()
        return self._map_to_model(db_booking)

    def set_status(self, booking: Booking) -> Booking:
        db_booking = self.db.query(DBBooking).filter(
            DBBooking.id == booking.id).first()
        db_booking.status = booking.status
        self.db.commit()
        return self._map_to_model(db_booking)
