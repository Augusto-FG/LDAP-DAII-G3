from app.controllers.ldap_base_controller import LDAPBaseController
from app.domain.entities.user import User

class LDAPPort:
    def __init__(self, ldap_controller: LDAPBaseController):
        self.ldap_controller = ldap_controller
        print("Initializing LDAPPort with controller:")
        print(ldap_controller)
        if not isinstance(ldap_controller, LDAPBaseController):
            raise ValueError("ldap_controller must be an instance of LDAPBaseController")
        
    async def get_user(self, user: User):
        self.ldap_controller.connect()
        entry = self.ldap_controller.search(user.username)
        self.ldap_controller.disconnect()
        return entry
    
    async def dummy_method(self):
        print("This is a dummy method in LDAPPort")
        return "This is a dummy method in LDAPPort"
    
