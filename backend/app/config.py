from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Investment Tracker"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "production"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # API Keys
    ALPHA_VANTAGE_API_KEY: str = ""
    TWELVE_DATA_API_KEY: str = ""

    # Backup
    BACKUP_ENABLED: bool = True
    BACKUP_RETENTION_DAYS: int = 30
    BACKUP_ENCRYPTION_KEY: str = ""

    # Price Updates
    PRICE_UPDATE_INTERVAL_MINUTES: int = 15
    PRICE_UPDATE_ENABLED: bool = True

    # Email (optional)
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Parse CORS origins if they're comma-separated
        if isinstance(self.BACKEND_CORS_ORIGINS, str):
            self.BACKEND_CORS_ORIGINS = [
                origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",")
            ]


settings = Settings()
