# /tests/unit/test_booked_period_model.py

import pytest
from uuid import uuid4, UUID
from datetime import date
from pydantic import ValidationError

from room_service.models.booked_period import BookedPeriod


@pytest.fixture()
def any_room_id() -> UUID:
    return uuid4()

@pytest.fixture()
def valid_dates() -> tuple[date, date]:
    return date(2024, 5, 1), date(2024, 5, 10)


def test_booked_period_creation(any_room_id: UUID, valid_dates: tuple[date, date]):
    period_id = uuid4()
    room_id = any_room_id
    start_date, end_date = valid_dates
    booked_period = BookedPeriod(id=period_id, room_id=room_id, start_date=start_date, end_date=end_date)

    assert booked_period.id == period_id
    assert booked_period.room_id == room_id
    assert booked_period.start_date == start_date
    assert booked_period.end_date == end_date


def test_booked_period_id_required(any_room_id: UUID, valid_dates: tuple[date, date]):
    room_id = any_room_id
    start_date, end_date = valid_dates
    with pytest.raises(ValidationError):
        BookedPeriod(room_id=room_id, start_date=start_date, end_date=end_date)


def test_booked_period_room_id_required(valid_dates: tuple[date, date]):
    period_id = uuid4()
    start_date, end_date = valid_dates
    with pytest.raises(ValidationError):
        BookedPeriod(id=period_id, start_date=start_date, end_date=end_date)


def test_booked_period_start_date_required(any_room_id: UUID):
    period_id = uuid4()
    room_id = any_room_id
    end_date = date(2024, 5, 10)
    with pytest.raises(ValidationError):
        BookedPeriod(id=period_id, room_id=room_id, end_date=end_date)


def test_booked_period_end_date_required(any_room_id: UUID):
    period_id = uuid4()
    room_id = any_room_id
    start_date = date(2024, 5, 1)
    with pytest.raises(ValidationError):
        BookedPeriod(id=period_id, room_id=room_id, start_date=start_date)
