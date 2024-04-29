# /room_service/database.py

from room_service.schemas.room import Room
from room_service.schemas.booked_period import BookedPeriod
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from room_service.schemas.base_schema import Base
from room_service.settings import settings


engine = create_engine(settings.postgres_url, echo=True)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
