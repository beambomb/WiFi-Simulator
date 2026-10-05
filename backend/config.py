import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "3D CAD WiFi Simulator"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "wifi-cad-simulator-super-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./wifi_simulator.db")
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:8000"]

    class Config:
        env_file = ".env"

settings = Settings()
