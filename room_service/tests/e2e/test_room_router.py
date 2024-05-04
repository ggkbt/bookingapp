# /tests/e2e/test_room_router.py

import pytest
import requests
from uuid import uuid4, UUID
from datetime import date

from room_service.models.room import Room

base_url = 'http://localhost:8001/api'


@pytest.fixture(scope='session')
def first_room_data() -> tuple[UUID, str]:
    return uuid4(), "106"


@pytest.fixture(scope='session')
def second_room_data() -> tuple[UUID, str]:
    return uuid4(), "107"


def test_add_demo_rooms() -> None:
    response = requests.post(f'{base_url}/rooms/add_demo')
    assert response.status_code == 200
    rooms = [Room.model_validate(r) for r in response.json()]
    assert len(rooms) == 5


def test_create_room_success(first_room_data: tuple[UUID, str]) -> None:
    room_id, room_number = first_room_data
    response = requests.post(f'{base_url}/rooms', json={
        'id': room_id.hex,
        'room_number': room_number
    })
    assert response.status_code == 200
    room = Room.model_validate(response.json())
    assert room.id == room_id
    assert room.room_number == room_number


def test_create_room_duplicate_id(first_room_data: tuple[UUID, str]) -> None:
    room_id, room_number = first_room_data
    response = requests.post(f'{base_url}/rooms', json={
        'id': room_id.hex,
        'room_number': room_number
    })
    assert response.status_code == 400


def test_create_second_room_success(second_room_data: tuple[UUID, str]) -> None:
    room_id, room_number = second_room_data
    response = requests.post(f'{base_url}/rooms', json={
        'id': room_id.hex,
        'room_number': room_number
    })
    assert response.status_code == 200
    room = Room.model_validate(response.json())
    assert room.id == room_id
    assert room.room_number == room_number


def test_read_rooms(
        first_room_data: tuple[UUID, str],
        second_room_data: tuple[UUID, str]
) -> None:
    response = requests.get(f'{base_url}/rooms')
    rooms = [Room.model_validate(r) for r in response.json()]
    room_ids = {room['id'] for room in rooms}
    ids_to_check = {first_room_data[0], second_room_data[0]}
    assert response.status_code == 200
    assert len(rooms) == 7
    assert ids_to_check.issubset(room_ids)


def test_book_room(first_room_data: tuple[UUID, str]) -> None:
    room_id, room_number = first_room_data
    booking_data = {
        "start_date": str(date(2024, 1, 1)),
        "end_date": str(date(2024, 1, 5))
    }
    response = requests.post(f'{base_url}/rooms/{room_id.hex}/book', json=booking_data)
    assert response.status_code == 200
    booked_room = Room.model_validate(response.json())
    assert booked_room.id == room_id


def test_book_room_repeat_error(first_room_data: tuple[UUID, str]) -> None:
    room_id, room_number = first_room_data
    booking_data = {
        "start_date": str(date(2024, 1, 1)),
        "end_date": str(date(2024, 1, 5))
    }
    response = requests.post(f'{base_url}/rooms/{room_id.hex}/book', json=booking_data)
    assert response.status_code == 400


def test_book_room_invalid_dates(first_room_data: tuple[UUID, str]) -> None:
    room_id, room_number = first_room_data
    booking_data = {
        "start_date": str(date(2024, 1, 10)),
        "end_date": str(date(2024, 1, 5))
    }
    response = requests.post(f'{base_url}/rooms/{room_id.hex}/book', json=booking_data)
    assert response.status_code == 400
