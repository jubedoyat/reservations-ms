from pydantic import Field
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # App
    PROJECT_NAME: str = "Reservations Microservice"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # API
    API_V1_STR: str = "/api/v1"
    ALLOWED_ORIGINS: List[str] = ["*"]

    # Database
    MONGODB_URI: str = Field(..., env="MONGODB_URI")
    DB_NAME: str = "flights-reserves"

    RESERVATION_SERVICE_URL: str = "http://localhost:8002"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = "HS256"
    
settings = Settings()
