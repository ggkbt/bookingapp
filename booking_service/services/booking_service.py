# /booking_service/services/booking_service.py

from datetime import date
from uuid import UUID, uuid4

import requests
from fastapi import Depends, HTTPException

import booking_service.settings
from booking_service import rabbitmq
from booking_service.models.booking import Booking, BookingStatuses
from booking_service.repositories.db_booking_repo import BookingRepo


class BookingService:
    booking_repo: BookingRepo

    def __init__(self, booking_repo: BookingRepo = Depends(BookingRepo)) -> None:
        self.booking_repo = booking_repo

    def get_bookings(self) -> list[Booking]:
        return self.booking_repo.get_bookings()

    def create_booking(self, room_id: UUID, start_date: date, end_date: date) -> Booking:
        url = f"{booking_service.settings.settings.room_service_url}/rooms/{room_id}/book"
        data = {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            booking = Booking(id=uuid4(), room_id=room_id, start_date=start_date, end_date=end_date,
                              status=BookingStatuses.CREATED)
            return self.booking_repo.create_booking(booking)
        else:
            detail = response.json().get('detail', 'Failed to book room')
            raise HTTPException(status_code=response.status_code, detail=detail)

    async def cancel_booking(self, booking_id: UUID) -> Booking:
        booking = self.booking_repo.get_booking_by_id(booking_id)
        if not booking:
            raise ValueError("Booking not found")
        if booking.status == BookingStatuses.COMPLETED:
            raise ValueError("Cannot cancel a completed booking")
        if booking.status == BookingStatuses.CANCELED:
            raise ValueError("Already canceled")
        booking.status = BookingStatuses.CANCELED

        message = {
            "room_id": str(booking.room_id),
            "start_date": booking.start_date.isoformat(),
            "end_date": booking.end_date.isoformat()
        }
        await rabbitmq.publish_message('room_cancellation_queue', message)

        return self.booking_repo.set_status(booking)

    def confirm_booking(self, booking_id: UUID) -> Booking:
        booking = self.booking_repo.get_booking_by_id(booking_id)
        if not booking:
            raise ValueError("Booking not found")
        if booking.status == BookingStatuses.COMPLETED:
            raise ValueError("Booking is completed")
        if booking.status == BookingStatuses.CANCELED:
            raise ValueError("Cannot confirm a canceled booking")
        booking.status = BookingStatuses.CONFIRMED
        return self.booking_repo.set_status(booking)

    def complete_booking(self, booking_id: UUID) -> Booking:
        booking = self.booking_repo.get_booking_by_id(booking_id)
        if not booking:
            raise ValueError("Booking not found")
        if booking.status == BookingStatuses.COMPLETED:
            raise ValueError("Already completed")
        if booking.status == BookingStatuses.CANCELED:
            raise ValueError("Cannot complete a canceled booking")
        booking.status = BookingStatuses.COMPLETED
        return self.booking_repo.set_status(booking)

    def get_booking_by_id(self, booking_id: UUID) -> Booking:
        booking = self.booking_repo.get_booking_by_id(booking_id)
        if not booking:
            raise ValueError("Booking not found")
        return booking
