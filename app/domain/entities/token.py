from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    expires_in: int
    scope: str
    issued_at: int
    issuer: str
    
class TokenData(BaseModel):
    username: str
    scopes: list[str]