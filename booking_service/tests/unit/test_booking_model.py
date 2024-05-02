# /tests/unit/test_booking_model.py

import pytest
from uuid import uuid4, UUID
from datetime import date
from pydantic import ValidationError

from booking_service.models.booking import Booking, BookingStatuses


@pytest.fixture()
def any_room_id() -> UUID:
    return uuid4()


def test_booking_creation(any_room_id: UUID):
    id = uuid4()
    start_date = date(2024, 5, 1)
    end_date = date(2024, 5, 3)
    status = BookingStatuses.CREATED
    booking = Booking(id=id, room_id=any_room_id, start_date=start_date, end_date=end_date, status=status)

    assert dict(booking) == {
        'id': id,
        'room_id': any_room_id,
        'start_date': start_date,
        'end_date': end_date,
        'status': status,
    }


def test_booking_room_id_required():
    with pytest.raises(ValidationError):
        Booking(id=uuid4(), start_date=date(2024, 5, 1), end_date=date(2024, 5, 3), status=BookingStatuses.CREATED)


def test_booking_start_date_required(any_room_id: UUID):
    with pytest.raises(ValidationError):
        Booking(id=uuid4(), room_id=any_room_id, end_date=date(2024, 5, 3), status=BookingStatuses.CREATED)


def test_booking_end_date_required(any_room_id: UUID):
    with pytest.raises(ValidationError):
        Booking(id=uuid4(), room_id=any_room_id, start_date=date(2024, 5, 1), status=BookingStatuses.CREATED)


def test_booking_status_required(any_room_id: UUID):
    with pytest.raises(ValidationError):
        Booking(id=uuid4(), room_id=any_room_id, start_date=date(2024, 5, 1), end_date=date(2024, 5, 3))
