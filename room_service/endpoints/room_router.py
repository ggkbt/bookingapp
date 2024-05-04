# /booking_service/endpoints/room_router.py

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from room_service.models.room import Room, CreateRoomRequest, BookRoomRequest
from room_service.services.room_service import RoomService

room_router = APIRouter(prefix='/rooms', tags=['Rooms'])


@room_router.get('/', response_model=List[Room])
def read_rooms(room_service: RoomService = Depends(RoomService)) -> List[Room]:
    return room_service.get_rooms()


@room_router.post('/', response_model=Room)
def add_room(room_data: CreateRoomRequest, room_service: RoomService = Depends(RoomService)) -> Room:
    try:
        room = room_service.create_room(room_data.id, room_data.room_number)
        return room
    except KeyError as e:
        raise HTTPException(status_code=400, detail=str(e))


@room_router.post('/{room_id}/book', response_model=Room)
def book_room(room_id: UUID, booking_data: BookRoomRequest, room_service: RoomService = Depends(RoomService)) -> Room:
    try:
        room = room_service.book_room(room_id, booking_data.start_date, booking_data.end_date)
        return room
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@room_router.post('/add_demo', response_model=List[Room])
def add_demo_rooms(room_service: RoomService = Depends(RoomService)) -> List[Room]:
    try:
        return room_service.add_demo_rooms_if_empty()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
