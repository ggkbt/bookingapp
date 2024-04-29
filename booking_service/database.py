# /booking_service/database.py

from booking_service.schemas.booking import Booking
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from booking_service.schemas.base_schema import Base
from booking_service.settings import settings

engine = create_engine(settings.postgres_url, echo=True)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
