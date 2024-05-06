# /booking_service/repositories/db_booking_repo.py

import traceback
from datetime import date
from uuid import UUID

import requests
from sqlalchemy.orm import Session

import booking_service.settings
from booking_service.database import get_db
from booking_service.models.booking import Booking, BookingStatuses
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
            raise KeyError(f'Booking with id={id} not found')
        return self._map_to_model(booking)

    def delete_booking_by_id(self, booking_id: UUID):
        try:
            booking = self.db.query(DBBooking).filter(DBBooking.id == booking_id).one()
            self.db.delete(booking)
            self.db.commit()
            return True
        except:
            traceback.print_exc()
            raise KeyError(f'Booking with id={booking_id} not found')

    def create_booking(self, id: UUID, room_id: UUID, start_date: date, end_date: date) -> Booking:
        url = f"{booking_service.settings.settings.room_service_url}/rooms/{room_id}/book"
        data = {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            try:
                booking = Booking(id=id, room_id=room_id, start_date=start_date, end_date=end_date,
                                  status=BookingStatuses.CREATED)
                db_booking = DBBooking(**booking.dict())
                self.db.add(db_booking)
                self.db.commit()
                return self._map_to_model(db_booking)
            except:
                traceback.print_exc()
                raise KeyError(f'Booking with id={id} already exists')
        else:
            traceback.print_exc()
            raise KeyError(response.text)

    def set_status(self, booking: Booking) -> Booking:
        try:
            db_booking = self.db.query(DBBooking).filter(
                DBBooking.id == booking.id).first()
            db_booking.status = booking.status
            self.db.commit()
            return self._map_to_model(db_booking)
        except:
            traceback.print_exc()
            raise KeyError(f'Booking with id={id} not found')
