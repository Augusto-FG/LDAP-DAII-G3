from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.config.settings import settings
from app.domain.services.user_service import UserService
from app.config.ldap_singleton import ldap_port_instance

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.get("/{user_id}")
async def get_user(user_id: str):
    # Dummy user retrieval logic, replace with real DB query
    user_entity = UserService(ldap_port_instance)
    user_entity.dummy_service_method()
    if user_id == "1":
        return {"id": "1", "username": "admin"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )