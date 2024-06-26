# /booking_service/repositories/local_booking_repo.py

from datetime import date
from uuid import UUID

from booking_service.models.booking import Booking, BookingStatuses

bookings: list[Booking] = []


class BookingRepo:
    def __init__(self, clear: bool = False) -> None:
        if clear:
            bookings.clear()

    def get_bookings(self) -> list[Booking]:
        return bookings

    def get_booking_by_id(self, id: UUID) -> Booking:
        for b in bookings:
            if b.id == id:
                return b

        raise KeyError("Booking not found")

    def create_booking(self, id: UUID, room_id: UUID, start_date: date, end_date: date) -> Booking:
        if start_date >= end_date:
            raise ValueError(f"Start date {start_date} must be before end date {end_date}.")

        if len([b for b in bookings if b.id == id]) > 0:
            raise KeyError

        booking = Booking(id=id, room_id=room_id, start_date=start_date, end_date=end_date,
                          status=BookingStatuses.CREATED)
        bookings.append(booking)
        return booking

    def set_status(self, booking: Booking) -> Booking:
        for b in bookings:
            if b.id == booking.id:
                b.status = booking.status
                return booking

        raise KeyError("Booking not found")
