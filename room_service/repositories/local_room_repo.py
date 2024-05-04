from datetime import date
from uuid import UUID, uuid4

from models.booked_period import BookedPeriod
from room_service.models.room import Room

rooms: list[Room] = []
booked_periods: list[BookedPeriod] = []


class RoomRepo:
    def __init__(self, clear: bool = False) -> None:
        if clear:
            rooms.clear()
            booked_periods.clear()

    def get_rooms(self) -> list[Room]:
        return rooms

    def get_room_by_id(self, id: UUID) -> Room:
        for r in rooms:
            if r.id == id:
                return r
        raise KeyError("Room not found")

    def create_room(self, room_id: UUID, room_number: str) -> Room:
        room = Room(id=room_id, room_number=room_number)
        if any(r.id == room.id for r in rooms):
            raise ValueError("Room with this ID already exists")
        rooms.append(room)
        return room


    def book_room_period(self, room_id: UUID, start_date: date, end_date: date) -> Room:
        room = self.get_room_by_id(room_id)
        for period in booked_periods:
            if (period.room_id == room_id and
                    period.start_date <= end_date and
                    period.end_date >= start_date):
                raise ValueError("Room is unavailable on selected dates")

        new_period = BookedPeriod(id=uuid4(), room_id=room_id, start_date=start_date, end_date=end_date)
        booked_periods.append(new_period)
        return room

    def free_room_period(self, room_id: UUID, start_date: date, end_date: date):
        global booked_periods
        booked_periods = [
            period for period in booked_periods
            if not (period.room_id == room_id and
                    period.start_date == start_date and
                    period.end_date == end_date)
        ]

    def has_no_rooms(self):
        return len(rooms) == 0
