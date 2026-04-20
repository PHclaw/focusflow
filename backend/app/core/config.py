from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost/focusflow"
    secret_key: str = "focusflow-secret-key-change-in-production"
    cors_origins: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    class Config:
        env_file = ".env"

settings = Settings()
