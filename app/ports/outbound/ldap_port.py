import structlog
from app.controllers.ldap_base_controller import LDAPBaseController
from app.domain.entities.user import User

logger = structlog.get_logger()

class LDAPPort:
    def __init__(self, ldap_controller: LDAPBaseController):
        self.ldap_controller = ldap_controller
        logger.info("Initializing LDAPPort with controller:", controller=ldap_controller)
        if not isinstance(ldap_controller, LDAPBaseController):
            raise ValueError("ldap_controller must be an instance of LDAPBaseController")
        
    async def get_user(self, username: str):
        logger.info("LDAPPort: Getting user")
        logger.info("Fetching user from LDAP:", username=username)
        self.ldap_controller.connect()
        base_dn = "ou=users,dc=example,dc=com"  # Change as needed
        search_filter = f"(uid={username})"
        result = self.ldap_controller.search(base_dn, search_filter, scope="SUBTREE")
        self.ldap_controller.disconnect()
        # If result is a tuple, get the first element
        if isinstance(result, tuple):
            result = result[0]
        # If result is a list, get the first dict
        if isinstance(result, list):
            if result:
                entry = result[0]
            else:
                entry = None
        else:
            entry = result
        return entry
    
    async def dummy_method(self):
        print("This is a dummy method in LDAPPort")
        return "This is a dummy method in LDAPPort"

