# /booking_service/repositories/db_room_repo.py

import traceback
from datetime import date
from uuid import UUID

from sqlalchemy.orm import Session

from room_service.database import get_db
from room_service.models.room import Room
from room_service.schemas.booked_period import BookedPeriod
from room_service.schemas.room import Room as DBRoom


class RoomRepo:
    db: Session

    def __init__(self) -> None:
        self.db = next(get_db())

    def _map_to_model(self, room: DBRoom) -> Room:
        return Room.from_orm(room)

    def _map_to_schema(self, room: Room) -> DBRoom:
        data = dict(room)
        return DBRoom(**data)

    def get_rooms(self) -> list[Room]:
        rooms = []
        for r in self.db.query(DBRoom).all():
            rooms.append(self._map_to_model(r))
        return rooms

    def get_room_by_id(self, id: UUID) -> Room:
        room = self.db.query(DBRoom).filter(DBRoom.id == id).first()
        if room is None:
            raise KeyError("Room not found")
        return self._map_to_model(room)

    def create_room(self, room: Room) -> Room:
        try:
            db_room = self._map_to_schema(room)
            self.db.add(db_room)
            self.db.commit()
            return self._map_to_model(db_room)
        except:
            traceback.print_exc()
            self.db.rollback()
            raise

    def book_room_period(self, room_id: UUID, start_date: date, end_date: date) -> Room:
        room = self.db.query(DBRoom).filter(DBRoom.id == room_id).first()
        if room is None:
            raise KeyError("Room not found")

        overlapping_periods = self.db.query(BookedPeriod).filter(
            BookedPeriod.room_id == room_id,
            BookedPeriod.start_date <= end_date,
            BookedPeriod.end_date >= start_date
        ).all()

        if overlapping_periods:
            raise ValueError("Room is unavailable on selected dates")

        try:
            new_period = BookedPeriod(room_id=room_id, start_date=start_date, end_date=end_date)
            self.db.add(new_period)
            self.db.commit()
            return self._map_to_model(room)
        except:
            traceback.print_exc()
            self.db.rollback()
            raise

    def free_room_period(self, room_id: UUID, start_date: date, end_date: date):
        room = self.db.query(DBRoom).filter(DBRoom.id == room_id).first()
        if room is None:
            raise KeyError("Room not found")
        self.db.query(BookedPeriod).filter(
            BookedPeriod.room_id == room_id,
            BookedPeriod.start_date == start_date,
            BookedPeriod.end_date == end_date
        ).delete()
        self.db.commit()

    def has_no_rooms(self):
        return self.db.query(DBRoom).count() == 0
