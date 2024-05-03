# /tests/unit/test_room_service.py

from datetime import date
from uuid import uuid4, UUID

import pytest

from room_service.repositories.local_room_repo import RoomRepo
from room_service.services.room_service import RoomService


@pytest.fixture(scope='session')
def room_service() -> RoomService:
    return RoomService(RoomRepo(clear=True))


@pytest.fixture(scope='session')
def room_data() -> tuple[UUID, str]:
    return uuid4(), "101"


def test_empty_rooms_before_creation(room_service: RoomService) -> None:
    assert room_service.get_rooms() == []


def test_add_demo_rooms(room_service: RoomService) -> None:
    room_service.add_demo_rooms_if_empty()
    rooms = room_service.get_rooms()
    assert len(rooms) == 5


def test_create_room(room_service: RoomService, room_data: tuple[UUID, str]) -> None:
    room_id, room_number = room_data
    room = room_service.create_room(room_id, room_number)
    rooms = room_service.get_rooms()
    assert room.room_number == room_number
    assert room.id == room_id
    assert len(rooms) == 6


def test_duplicate_room_id(room_service: RoomService, room_data: tuple[UUID, str]) -> None:
    room_id, room_number = room_data
    with pytest.raises(ValueError):
        room_service.create_room(room_id, "Another Room Number")


def test_book_room_period(room_service: RoomService, room_data: tuple[UUID, str]) -> None:
    room_id, room_number = room_data
    start_date = date(2024, 5, 1)
    end_date = date(2024, 5, 3)
    booked_room = room_service.book_room(room_id, start_date, end_date)
    assert booked_room.room_number == room_number
    assert booked_room.id == room_id


def test_book_room_period_again_error(room_service: RoomService, room_data: tuple[UUID, str]) -> None:
    room_id, room_number = room_data
    start_date = date(2024, 5, 1)
    end_date = date(2024, 5, 3)
    with pytest.raises(ValueError):
        room_service.book_room(room_id, start_date, end_date)


def test_free_room_period(room_service: RoomService, room_data: tuple[UUID, str]) -> None:
    room_id, room_number = room_data
    start_date = date(2024, 5, 1)
    end_date = date(2024, 5, 3)
    room_service.free_room_period(room_id, start_date, end_date)


def test_book_room_period_again(room_service: RoomService, room_data: tuple[UUID, str]) -> None:
    room_id, room_number = room_data
    start_date = date(2024, 5, 1)
    end_date = date(2024, 5, 3)
    booked_room = room_service.book_room(room_id, start_date, end_date)
    assert booked_room.room_number == room_number
    assert booked_room.id == room_id


def test_book_room_period_invalid_dates(room_service: RoomService, room_data: tuple[UUID, str]) -> None:
    room_id, room_number = room_data
    start_date = date(2024, 5, 3)
    end_date = date(2024, 5, 1)
    with pytest.raises(ValueError):
        room_service.book_room(room_id, start_date, end_date)
