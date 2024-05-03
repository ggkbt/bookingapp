# /tests/unit/test_room_model.py

from uuid import uuid4

import pytest
from pydantic import ValidationError

from room_service.models.room import Room


@pytest.fixture()
def any_room_number() -> str:
    return "101A"


def test_room_creation(any_room_number: str):
    id = uuid4()
    room_number = any_room_number
    room = Room(id=id, room_number=room_number)

    assert dict(room) == {
        'id': id,
        'room_number': room_number,
    }


def test_room_id_required(any_room_number: str):
    with pytest.raises(ValidationError):
        Room(room_number=any_room_number)


def test_room_number_required():
    with pytest.raises(ValidationError):
        Room(id=uuid4())
