# /room_service/database.py

from room_service.schemas.room import Room
from room_service.schemas.booked_period import BookedPeriod
from sqlalchemy.engine import create_engine, URL
from sqlalchemy.orm import sessionmaker
from room_service.schemas.base_schema import Base
from room_service.settings import settings


url = URL.create(drivername=settings.postgres_drivername, username=settings.postgres_user,
                 password=settings.postgres_password, host=settings.postgres_host, port=settings.postgres_port,
                 database=settings.postgres_database)
engine = create_engine(url, echo=True)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
