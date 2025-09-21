from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # va a la raíz del proyecto

class Settings(BaseSettings):
    APP_NAME: str
    LOG_LEVEL: str
    DATABASE_URL: str
    QUEUE_URL: str
    LDAP_URL: str
    LDAP_BIND_DN: str
    LDAP_BIND_PASSWORD: str
    SECRET_KEY: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",  # ahora busca .env en la raíz del proyecto
        extra="ignore"
    )

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
