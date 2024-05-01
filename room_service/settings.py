# /room_service/settings.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    amqp_url: str
    postgres_drivername: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: str
    postgres_database: str

    model_config = SettingsConfigDict(env_file='rooms.env')


settings = Settings()
