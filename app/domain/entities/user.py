from pydantic import BaseModel, EmailStr, Field
from typing import List
from .roles import Role

class User(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    roles: List[Role] = Field(default_factory=list)
    id: str = Field(default_factory=lambda: "user_" + str(id(object())))
    is_active: bool = True
    phone_number: List[str] = Field(default_factory=list)
    address: str = ""
    full_name: str = ""
    dnPath: str = "" # Distinguished Name Path in LDAP, just one domain
    created_at: str = Field(default_factory=lambda: "2024-01-01T00:00:00Z") # Placeholder for creation timestamp
    updated_at: str = Field(default_factory=lambda: "2024-01-01T00:00:00Z") # Placeholder for update timestamp
