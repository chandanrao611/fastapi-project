from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "FastAPI"
    DEBUG: bool = False
    PORT: int = 8000
    DATABASE_URL: str
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    SECRET_KEY: str

    class Config:
        env_file = "env/.env"
        case_sensitive = True

# Cache settings (important for performance)
@lru_cache
def get_settings():
    return Settings()

settings = get_settings()