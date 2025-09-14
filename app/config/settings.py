import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str
    LOG_LEVEL: str
    DATABASE_URL: str
    QUEUE_URL: str
    LDAP_URL: str
    LDAP_BIND_DN: str
    LDAP_BIND_PASSWORD: str
    model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(__file__), ".env"), extra="ignore")
        
@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()