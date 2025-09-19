from pydantic import BaseModel
from app.config.settings import settings

class ClientCredentials(BaseModel):
    client_id: str
    client_secret: str
    redirect_uris: list[str] = []
    scopes: list[str] = []