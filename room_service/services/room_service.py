# /room_service/services/room_service.py

from uuid import UUID, uuid4
from fastapi import Depends
from datetime import date
from typing import List

from room_service.models.room import Room
from room_service.repositories.db_room_repo import RoomRepo


class RoomService:
    room_repo: RoomRepo

    def __init__(self, room_repo: RoomRepo = Depends(RoomRepo)) -> None:
        self.room_repo = room_repo

    def get_rooms(self) -> List[Room]:
        return self.room_repo.get_rooms()

    def create_room(self, room_id: UUID, room_number: str) -> Room:
        return self.room_repo.create_room(room_id=room_id, room_number=room_number)

    def free_room_period(self, room_id: UUID, start_date: date, end_date: date) -> bool:
        return self.room_repo.free_room_period(room_id, start_date, end_date)

    def book_room(self, room_id, start_date: date, end_date: date) -> Room:
        if start_date >= end_date:
            raise ValueError(f"Start date {start_date} must be before end date {end_date}.")
        return self.room_repo.book_room_period(room_id, start_date, end_date)

    def add_demo_rooms_if_empty(self):
        if self.room_repo.has_no_rooms():
            room_numbers = ["101", "102", "103", "104", "105"]
            for number in room_numbers:
                self.room_repo.create_room(room_id=uuid4(), room_number=number)
            return True
        return False
