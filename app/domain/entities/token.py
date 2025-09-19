import jwt
from typing import List
from pydantic import BaseModel, Field
from app.config.settings import settings

class Token(BaseModel):
    sub: str = Field(..., description="Subject: Unique identifier for the client (client_id)")
    aud: str = Field(..., description="Audience: Intended recipient of the token")
    iss: str = Field(..., description="Issuer: Entity that issued the token")
    exp: int = Field(..., description="Expiration time (as UNIX timestamp): Token expiry in seconds since epoch")
    nbf: int = Field(..., description="Not Before (as UNIX timestamp): Token is valid from this time")
    iat: int = Field(..., description="Issued At (as UNIX timestamp): Time at which the token was issued")
    jti: str = Field(..., description="JWT ID: Unique identifier for this token")
    roles: List[str] = Field(..., description="Roles: List of roles or permissions assigned to the subject")

    def to_jwt(self, secret: str = settings.SECRET_KEY, algorithm: str = "HS256") -> str:
        payload = {
            "sub": self.sub,
            "aud": self.aud,
            "iss": self.iss,
            "exp": self.exp,
            "nbf": self.nbf,
            "iat": self.iat,
            "jti": self.jti,
            "roles": self.roles,
            "azp": self.sub,
        }
        return jwt.encode(payload, secret, algorithm=algorithm)
