
from app.domain.entities.user import User
from app.ports.outbound.ldap_port import LDAPPort

class UserService:
    def __init__(self, ldap_port: LDAPPort):
        self.ldap_port = ldap_port

    def get_user(self, username: str) -> User:
        entry = self.ldap_port.get_user(username)
        return User(**entry)

    def dummy_service_method(self):
        print("This is a dummy method in UserService")
        return self.ldap_port.dummy_method()