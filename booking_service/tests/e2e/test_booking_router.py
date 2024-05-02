# /tests/e2e/test_booking_router.py

import time
import pytest
import requests
from uuid import UUID, uuid4
from datetime import date

from booking_service.models.booking import Booking, BookingStatuses

time.sleep(5)
base_url = 'http://localhost:8080/api'


@pytest.fixture(scope='session')
def first_booking_data() -> tuple[UUID, UUID, date, date]:
    return uuid4(), uuid4(), date(2024, 5, 1), date(2024, 5, 3)


@pytest.fixture(scope='session')
def second_booking_data() -> tuple[UUID, UUID, date, date]:
    return uuid4(), uuid4(), date(2024, 5, 2), date(2024, 5, 4)


def test_get_bookings_empty() -> None:
    assert requests.get(f'{base_url}/bookings').json() == []


def test_add_booking_first_success(
        first_booking_data: tuple[UUID, UUID, date, date]
) -> None:
    _, room_id, start_date, end_date = first_booking_data
    response = requests.post(f'{base_url}/bookings', json={
        'room_id': room_id.hex,
        'start_date': str(start_date),
        'end_date': str(end_date)
    })
    booking = Booking.model_validate(response.json())
    assert booking.room_id == room_id
    assert booking.start_date == start_date
    assert booking.end_date == end_date
    assert booking.status == BookingStatuses.CREATED


def test_add_booking_first_repeat_error(
        first_booking_data: tuple[UUID, UUID, date, date]
) -> None:
    _, room_id, start_date, end_date = first_booking_data
    response = requests.post(f'{base_url}/bookings', json={
        'room_id': room_id.hex,
        'start_date': str(start_date),
        'end_date': str(end_date)
    })
    assert response.status_code == 400


def test_add_booking_second_success(
        second_booking_data: tuple[UUID, UUID, date, date]
) -> None:
    _, room_id, start_date, end_date = second_booking_data
    response = requests.post(f'{base_url}/bookings', json={
        'room_id': room_id.hex,
        'start_date': str(start_date),
        'end_date': str(end_date)
    })
    booking = Booking.model_validate(response.json())
    assert booking.room_id == room_id
    assert booking.start_date == start_date
    assert booking.end_date == end_date
    assert booking.status == BookingStatuses.CREATED


def test_get_bookings_full(
        first_booking_data: tuple[UUID, UUID, date, date],
        second_booking_data: tuple[UUID, UUID, date, date]
) -> None:
    bookings = [Booking.model_validate(d) for d in requests.get(f'{base_url}/bookings').json()]
    assert len(bookings) == 2
    assert bookings[0].room_id == first_booking_data[1]
    assert bookings[1].room_id == second_booking_data[1]


def test_cancel_booking_not_found() -> None:
    response = requests.post(f'{base_url}/bookings/{uuid4()}/cancel')
    assert response.status_code == 404


def test_cancel_booking_success(
        first_booking_data: tuple[UUID, UUID, date, date]
) -> None:
    booking_id = first_booking_data[0]
    response = requests.post(f'{base_url}/bookings/{booking_id}/cancel')
    booking = Booking.model_validate_json(response.text)
    assert booking.id == booking_id
    assert booking.status == BookingStatuses.CANCELED


def test_confirm_booking_status_error(
        first_booking_data: tuple[UUID, UUID, date, date]
) -> None:
    booking_id = first_booking_data[0]
    response = requests.post(f'{base_url}/bookings/{booking_id}/confirm')
    assert response.status_code == 400


def test_confirm_booking_not_found() -> None:
    response = requests.post(f'{base_url}/bookings/{uuid4()}/confirm')
    assert response.status_code == 404


def test_confirm_booking(
        second_booking_data: tuple[UUID, UUID, date, date]
) -> None:
    booking_id = second_booking_data[0]
    response = requests.post(f'{base_url}/bookings/{booking_id}/confirm')
    booking = Booking.model_validate_json(response.text)
    assert booking.id == booking_id
    assert booking.status == BookingStatuses.CONFIRMED


def test_complete_booking_status_error(
        second_booking_data: tuple[UUID, UUID, date, date]
) -> None:
    booking_id = second_booking_data[0]
    response = requests.post(f'{base_url}/bookings/{booking_id}/complete')
    assert response.status_code == 400


def test_complete_booking_not_found() -> None:
    response = requests.post(f'{base_url}/bookings/{uuid4()}/complete')
    assert response.status_code == 404


def test_complete_booking(
        second_booking_data: tuple[UUID, UUID, date, date]
) -> None:
    booking_id = second_booking_data[0]
    response = requests.post(f'{base_url}/bookings/{booking_id}/complete')
    booking = Booking.model_validate_json(response.text)
    assert booking.id == booking_id
    assert booking.status == BookingStatuses.COMPLETED


def test_get_booking_by_id(
        first_booking_data: tuple[UUID, UUID, date, date]
) -> None:
    booking_id = first_booking_data[0]
    response = requests.get(f'{base_url}/bookings/{booking_id}')
    booking = Booking.model_validate(response.json())
    assert booking.room_id == first_booking_data[1]
    assert booking.start_date == first_booking_data[2]
    assert booking.end_date == first_booking_data[3]
