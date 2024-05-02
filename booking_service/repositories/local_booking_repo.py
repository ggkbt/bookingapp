# /booking_service/repositories/local_booking_repo.py
from datetime import date
from uuid import UUID, uuid4
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

    def create_booking(self, room_id: UUID, start_date: date, end_date: date) -> Booking:
        booking = Booking(id=uuid4(), room_id=room_id, start_date=start_date, end_date=end_date,
                          status=BookingStatuses.CREATED)
        bookings.append(booking)
        return booking

    def set_status(self, booking: Booking) -> Booking:
        for b in bookings:
            if b.id == booking.id:
                b.status = booking.status
                return booking

        raise KeyError("Booking not found")
