# /booking_service/settings.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    amqp_url: str
    postgres_url: str
    room_service_url: str

    model_config = SettingsConfigDict(env_file='bookings.env')


settings = Settings()
