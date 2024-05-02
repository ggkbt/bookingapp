# /booking_service/repositories/local_booking_repo.py

from uuid import UUID
from booking_service.models.booking import Booking

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

    def create_booking(self, booking: Booking) -> Booking:
        if any(b for b in bookings if b.id == booking.id):
            raise KeyError("Booking ID already exists")

        bookings.append(booking)
        return booking

    def set_status(self, booking: Booking) -> Booking:
        for b in bookings:
            if b.id == booking.id:
                b.status = booking.status
                return booking

        raise KeyError("Booking not found")
