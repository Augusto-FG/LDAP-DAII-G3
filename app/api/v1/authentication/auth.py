from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from app.config.settings import settings
from app.controllers.OpenLDAP.openldap_controller import OpenLDAPController
from app.domain.entities.token import Token
from app.domain.entities.client_credentials import ClientCredentials
from app.domain.services.user_service import UserService
from app.config.ldap_singleton import get_ldap_port_instance
from app.domain.services.token_service import TokenService

from datetime import datetime, timezone, timedelta
now = datetime.now(timezone.utc)

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login(request: LoginRequest):
    # Dummy authentication logic, replace with real LDAP or DB check
    if request.username == "admin" and request.password == "admin":
        return {"message": "Login successful"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials"
    )
    
@router.post("/token")
async def token(request: ClientCredentials):
    # Dummy token generation logic, replace with real token generation
    token_service = TokenService(UserService(await get_ldap_port_instance()))
    token = token_service.generate_token(request)
    return token.to_jwt()
    # raise HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED,
    #     detail="Invalid client credentials"
    # )
    
@router.get("/test")
async def test_endpoint():
    # test LDAP connection or other settings usage
    ldap_controller = OpenLDAPController()
    ldap_controller.connect()
    # entries = ldap_controller.search("cn=test2,dc=ldap,dc=com", "(objectClass=*)")
    # ldap_controller.add_entry("cn=test2,dc=ldap,dc=com", {"objectClass": ["top", "person"], "sn": "Test"})
    # ldap_controller.modify_entry("cn=test2,dc=ldap,dc=com", {"telephoneNumber": "+54 11 5555 5555", "description": "Test user"})
    # # entries_2 = ldap_controller.search("cn=test2,dc=ldap,dc=com", "(objectClass=*)")
    # entries, search_result = ldap_controller.search("cn=test2,dc=ldap,dc=com", "(objectClass=*)", scope='BASE')
    # entries_2_serialized, search_result_2 = ldap_controller.search("cn=test2,dc=ldap,dc=com", "(objectClass=*)", scope='BASE')
    # # entries_2_serialized = [
    # #     {"dn": e.entry_dn, "attributes": e.entry_attributes_as_dict}
    # #     for e in entries_2
    # # ]
    # print(f"Second search result: {entries_2_serialized}")
    # print(settings.LDAP_BIND_DN)
    # ldap_controller.disconnect()
    # entries_2_serialized = [
    #         {"dn": e.entry_dn, "attributes": e.entry_attributes_as_dict}
    #         for e in entries_2
    #     ]
    # print(f"Second search result: {search_result_2}, Entries: {entries_2_serialized}")

    # return {
    #     "message": f"This is a test endpoint v1, using settings: {settings.APP_NAME}",
    #     "entries": [e.entry_attributes_as_dict for e in entries],
    #     "entry": entries_2_serialized
    # }
    
    print(f"Connected: {ldap_controller.check_connection()}")

    # Check base DN existence
    base_entries, base_result = ldap_controller.search("dc=ldap,dc=com", "(objectClass=*)", scope='BASE')
    print(f"Base DN check: {base_result}, Entries: {[{e.entry_dn: e.entry_attributes_as_dict} for e in base_entries]}")

    # First search for test2
    entries, search_result = ldap_controller.search("cn=test2,dc=ldap,dc=com", "(objectClass=*)", scope='BASE')
    print(f"First search result: {search_result}, Entries: {[{e.entry_dn: e.entry_attributes_as_dict} for e in entries]}")

    # Delete existing entry if it exists (to avoid "already exists" error)
    if entries:
        delete_result = ldap_controller.delete_entry("cn=test2,dc=ldap,dc=com")
        print(f"Delete result: {delete_result}")

    # Add entry
    add_result = ldap_controller.add_entry(
        "cn=test2,dc=ldap,dc=com",
        {"objectClass": ["top", "person"], "sn": "Test", "cn": "test2"}
    )
    print(f"Add result: {add_result}")

    # Modify entry
    modify_result = ldap_controller.modify_entry(
        "cn=test2,dc=ldap,dc=com",
        {"telephoneNumber": "+54 11 5555 5555", "description": "Test user"}
    )
    print(f"Modify result: {modify_result}")

    # Second search
    entries_2, search_result_2 = ldap_controller.search("cn=test2,dc=ldap,dc=com", "(objectClass=*)", scope='BASE')
    entries_2_serialized = [
        {"dn": e.entry_dn, "attributes": e.entry_attributes_as_dict}
        for e in entries_2
    ]
    print(f"Second search result: {search_result_2}, Entries: {entries_2_serialized}")

    return {
        "message": f"This is a test endpoint v1, using settings: {settings.APP_NAME}",
        "entries": [e.entry_attributes_as_dict for e in entries],
        "entry": entries_2_serialized
    }