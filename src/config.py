import os
from dotenv import load_dotenv

from pathlib import Path

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Fast api"
    PROJECT_VERSION: str = "1.0.0"
    POSTGRES_USER: str = os.getenv("POSTGRES_USER","dev" )
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD","Fastapi_699699")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "fastapi_b_db")
    SECRET_AUTH: str = os.getenv("SECRET_AUTH")
    DATABASE_URL: str = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}?async_fallback=True"
    app_title: str = 'Code review '
    description: str = 'Код ревью сервис '

settings = Settings()