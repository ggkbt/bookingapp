# /tests/unit/test_booking_service.py

import pytest
from uuid import uuid4, UUID
from datetime import date

from booking_service.services.booking_service import BookingService
from booking_service.models.booking import BookingStatuses
from booking_service.repositories.local_booking_repo import BookingRepo


@pytest.fixture(scope='session')
def booking_service() -> BookingService:
    return BookingService(BookingRepo(clear=True))


@pytest.fixture(scope='session')
def first_booking_data() -> tuple[UUID, UUID, date, date]:
    return uuid4(), uuid4(), date(2024, 5, 1), date(2024, 5, 3)


@pytest.fixture(scope='session')
def second_booking_data() -> tuple[UUID, UUID, date, date]:
    return uuid4(), uuid4(), date(2024, 5, 2), date(2024, 5, 4)


def test_empty_bookings(booking_service: BookingService) -> None:
    assert booking_service.get_bookings() == []


def test_create_first_booking(
        first_booking_data: tuple[UUID, UUID, date, date],
        booking_service: BookingService
) -> None:
    booking_id, room_id, start_date, end_date = first_booking_data
    booking = booking_service.create_booking(booking_id, room_id, start_date, end_date)
    assert booking.id == booking_id
    assert booking.room_id == room_id
    assert booking.start_date == start_date
    assert booking.end_date == end_date
    assert booking.status == BookingStatuses.CREATED


def test_create_second_booking(
        second_booking_data: tuple[UUID, UUID, date, date],
        booking_service: BookingService
) -> None:
    booking_id, room_id, start_date, end_date = second_booking_data
    booking = booking_service.create_booking(booking_id, room_id, start_date, end_date)
    assert booking.id == booking_id
    assert booking.room_id == room_id
    assert booking.start_date == start_date
    assert booking.end_date == end_date
    assert booking.status == BookingStatuses.CREATED


def test_get_bookings_full(
        first_booking_data: tuple[UUID, UUID, date, date],
        second_booking_data: tuple[UUID, UUID, date, date],
        booking_service: BookingService
) -> None:
    bookings = booking_service.get_bookings()
    assert len(bookings) == 2
    assert bookings[0].id == first_booking_data[0]
    assert bookings[1].start_date == second_booking_data[0]


def test_confirm_booking_not_found(
        booking_service: BookingService
) -> None:
    with pytest.raises(KeyError):
        booking_service.confirm_booking(uuid4())


def test_confirm_booking(
        first_booking_data: tuple[UUID, UUID, date, date],
        booking_service: BookingService
) -> None:
    booking = booking_service.confirm_booking(first_booking_data[0])
    assert booking.status == BookingStatuses.CONFIRMED


def test_complete_booking_not_found(
        booking_service: BookingService
) -> None:
    with pytest.raises(KeyError):
        booking_service.complete_booking(uuid4())


def test_complete_booking(
        first_booking_data: tuple[UUID, UUID, date, date],
        booking_service: BookingService
) -> None:
    booking = booking_service.complete_booking(first_booking_data[0])
    assert booking.status == BookingStatuses.COMPLETED


@pytest.mark.asyncio
async def test_cancel_completed_booking_status_error(
        first_booking_data: tuple[UUID, UUID, date, date],
        booking_service: BookingService
) -> None:
    with pytest.raises(ValueError):
        await booking_service.cancel_booking(first_booking_data[0])


def test_complete_completed_booking_status_error(
        first_booking_data: tuple[UUID, UUID, date, date],
        booking_service: BookingService
) -> None:
    with pytest.raises(ValueError):
        booking_service.complete_booking(first_booking_data[0])


def test_confirm_completed_booking_status_error(
        first_booking_data: tuple[UUID, UUID, date, date],
        booking_service: BookingService
) -> None:
    with pytest.raises(ValueError):
        booking_service.confirm_booking(first_booking_data[0])


@pytest.mark.asyncio
async def test_cancel_booking_not_found(
        booking_service: BookingService
) -> None:
    with pytest.raises(KeyError):
        await booking_service.cancel_booking(uuid4())


@pytest.mark.asyncio
async def test_cancel_booking(
        second_booking_data: tuple[UUID, UUID, date, date],
        booking_service: BookingService
) -> None:
    booking = await booking_service.cancel_booking(second_booking_data[0])
    assert booking.status == BookingStatuses.CANCELED


@pytest.mark.asyncio
async def test_cancel_canceled_booking_status_error(
        second_booking_data: tuple[UUID, UUID, date, date],
        booking_service: BookingService
) -> None:
    with pytest.raises(ValueError):
        await booking_service.cancel_booking(second_booking_data[0])


def test_confirm_canceled_booking_status_error(
        second_booking_data: tuple[UUID, UUID, date, date],
        booking_service: BookingService
) -> None:
    with pytest.raises(ValueError):
        booking_service.confirm_booking(second_booking_data[0])


def test_complete_canceled_booking_status_error(
        second_booking_data: tuple[UUID, UUID, date, date],
        booking_service: BookingService
) -> None:
    with pytest.raises(ValueError):
        booking_service.complete_booking(second_booking_data[0])
