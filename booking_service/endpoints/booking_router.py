# /booking_service/endpoints/booking_router.py

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from booking_service.models.booking import Booking, CreateBookingRequest
from booking_service.services.booking_service import BookingService

booking_router = APIRouter(prefix='/bookings', tags=['Bookings'])


@booking_router.get('/', response_model=List[Booking])
def read_bookings(booking_service: BookingService = Depends(BookingService)) -> List[Booking]:
    return booking_service.get_bookings()


@booking_router.post('/', response_model=Booking)
def add_booking(booking_data: CreateBookingRequest,
                booking_service: BookingService = Depends(BookingService)) -> Booking:
    try:
        booking = booking_service.create_booking(booking_data.id, booking_data.room_id, booking_data.start_date, booking_data.end_date)
        return booking
    except KeyError as e:
        raise HTTPException(status_code=400, detail=str(e))


@booking_router.post('/{booking_id}/cancel', response_model=Booking)
async def cancel_booking(booking_id: UUID, booking_service: BookingService = Depends(BookingService)) -> Booking:
    try:
        booking = await booking_service.cancel_booking(booking_id)
        return booking
    except KeyError:
        raise HTTPException(404, f'Booking with id={id} not found')
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@booking_router.post('/{booking_id}/confirm', response_model=Booking)
def confirm_booking(booking_id: UUID, booking_service: BookingService = Depends(BookingService)) -> Booking:
    try:
        booking = booking_service.confirm_booking(booking_id)
        return booking
    except KeyError:
        raise HTTPException(404, f'Booking with id={id} not found')
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@booking_router.post('/{booking_id}/complete', response_model=Booking)
def complete_booking(booking_id: UUID, booking_service: BookingService = Depends(BookingService)) -> Booking:
    try:
        booking = booking_service.complete_booking(booking_id)
        return booking
    except KeyError:
        raise HTTPException(404, f'Booking with id={id} not found')
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@booking_router.get('/{booking_id}', response_model=Booking)
def get_booking(booking_id: UUID, booking_service: BookingService = Depends(BookingService)) -> Booking:
    try:
        booking = booking_service.get_booking_by_id(booking_id)
        return booking
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Booking with id={booking_id} not found")
