# /tests/e2e/test_booking_router.py

import time
from datetime import date
from uuid import uuid4

import pytest
import requests

from booking_service.models.booking import Booking, BookingStatuses
from room_service.models.room import Room

time.sleep(5)
base_url = 'http://localhost:8000/api'
room_service_url = 'http://localhost:8001/api'
rooms = [Room.model_validate(d) for d in requests.get(f'{room_service_url}/rooms').json()]


@pytest.fixture(scope='session')
def booking_data() -> tuple[date, date]:
    return date(2024, 5, 1), date(2024, 5, 5)


@pytest.fixture(scope='session')
def second_booking_data() -> tuple[date, date]:
    return date(2024, 6, 7), date(2024, 6, 10)


def test_get_bookings_empty() -> None:
    assert requests.get(f'{base_url}/bookings').json() == []


def test_add_booking_first_success(
        booking_data: tuple[date, date]
) -> None:
    start_date, end_date = booking_data
    response = requests.post(f'{base_url}/bookings', json={
        'room_id': str(rooms[0].id),
        'start_date': str(start_date),
        'end_date': str(end_date)
    })
    booking = Booking.model_validate(response.json())
    assert str(booking.room_id) == str(rooms[0].id)
    assert booking.start_date == start_date
    assert booking.end_date == end_date
    assert booking.status == BookingStatuses.CREATED


def test_add_booking_first_repeat_error(
        booking_data: tuple[date, date]
) -> None:
    start_date, end_date = booking_data
    response = requests.post(f'{base_url}/bookings', json={
        'room_id': str(rooms[0].id),
        'start_date': str(start_date),
        'end_date': str(end_date)
    })
    assert response.status_code == 400


def test_add_booking_end_date_before_start_date_error() -> None:
    response = requests.post(f'{base_url}/bookings', json={
        'room_id': str(rooms[0].id),
        'start_date': str(date(2024, 5, 10)),
        'end_date': str(date(2024, 5, 1))
    })
    assert response.status_code == 400


def test_add_booking_second_success(
        second_booking_data: tuple[date, date]
) -> None:
    start_date, end_date = second_booking_data
    response = requests.post(f'{base_url}/bookings', json={
        'room_id': str(rooms[1].id),
        'start_date': str(start_date),
        'end_date': str(end_date)
    })
    booking = Booking.model_validate(response.json())
    assert str(booking.room_id) == str(rooms[1].id)
    assert booking.start_date == start_date
    assert booking.end_date == end_date
    assert booking.status == BookingStatuses.CREATED


def test_get_bookings_full() -> None:
    bookings = [Booking.model_validate(d) for d in requests.get(f'{base_url}/bookings').json()]
    assert len(bookings) == 2
    assert bookings[0].room_id == rooms[0].id
    assert bookings[1].room_id == rooms[1].id


def test_cancel_booking_not_found() -> None:
    response = requests.post(f'{base_url}/bookings/{uuid4()}/cancel')
    assert response.status_code == 404


def test_cancel_booking_success() -> None:
    bookings = [Booking.model_validate(d) for d in requests.get(f'{base_url}/bookings').json()]
    response = requests.post(f'{base_url}/bookings/{str(bookings[0].id)}/cancel')
    booking = Booking.model_validate_json(response.text)
    assert booking.id == bookings[0].id
    assert booking.status == BookingStatuses.CANCELED


def test_confirm_booking_not_found() -> None:
    response = requests.post(f'{base_url}/bookings/{uuid4()}/confirm')
    assert response.status_code == 404


def test_confirm_booking() -> None:
    bookings = [Booking.model_validate(d) for d in requests.get(f'{base_url}/bookings').json()]
    response = requests.post(f'{base_url}/bookings/{str(bookings[1].id)}/confirm')
    booking = Booking.model_validate_json(response.text)
    assert booking.id == bookings[1].id
    assert booking.status == BookingStatuses.CONFIRMED


def test_complete_booking_not_found() -> None:
    response = requests.post(f'{base_url}/bookings/{uuid4()}/complete')
    assert response.status_code == 404


def test_complete_booking() -> None:
    bookings = [Booking.model_validate(d) for d in requests.get(f'{base_url}/bookings').json()]
    response = requests.post(f'{base_url}/bookings/{str(bookings[1].id)}/complete')
    booking = Booking.model_validate_json(response.text)
    assert booking.id == bookings[1].id
    assert booking.status == BookingStatuses.COMPLETED


def test_cancel_booking_error() -> None:
    time.sleep(3)
    bookings = [Booking.model_validate(d) for d in requests.get(f'{base_url}/bookings').json()]
    response1 = requests.post(f'{base_url}/bookings/{str(bookings[0].id)}/cancel')
    response2 = requests.post(f'{base_url}/bookings/{str(bookings[1].id)}/cancel')
    assert response1.status_code == 400
    assert response2.status_code == 400


def test_confirm_booking_error() -> None:
    bookings = [Booking.model_validate(d) for d in requests.get(f'{base_url}/bookings').json()]
    response1 = requests.post(f'{base_url}/bookings/{str(bookings[0].id)}/confirm')
    response2 = requests.post(f'{base_url}/bookings/{str(bookings[1].id)}/confirm')
    assert response1.status_code == 400
    assert response2.status_code == 400


def test_complete_booking_error() -> None:
    bookings = [Booking.model_validate(d) for d in requests.get(f'{base_url}/bookings').json()]
    response1 = requests.post(f'{base_url}/bookings/{str(bookings[0].id)}/complete')
    response2 = requests.post(f'{base_url}/bookings/{str(bookings[1].id)}/complete')
    assert response1.status_code == 400
    assert response2.status_code == 400


def test_get_booking_by_id() -> None:
    bookings = [Booking.model_validate(d) for d in requests.get(f'{base_url}/bookings').json()]
    response = requests.get(f'{base_url}/bookings/{str(bookings[0].id)}')
    booking = Booking.model_validate(response.json())
    assert booking.id == bookings[0].id
    assert booking.room_id == bookings[0].room_id
    assert booking.start_date == bookings[0].start_date
    assert booking.end_date == bookings[0].end_date
