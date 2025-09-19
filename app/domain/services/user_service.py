import structlog
from app.domain.entities.user import User
from app.ports.outbound.ldap_port import LDAPPort

logger = structlog.get_logger()

class UserService:
    def __init__(self, ldap_port: LDAPPort):
        self.ldap_port = ldap_port

    async def get_user(self, username: str) -> User:
        logger.info("Fetching user from LDAP:", username=username)
        entry = await self.ldap_port.get_user(username)
        if entry is None:
            return None  # Let the API layer handle the 404
        return User(**entry)

    async def dummy_service_method(self):
        logger.info("Calling dummy service method")
        return await self.ldap_port.dummy_method()