import structlog

logger = structlog.get_logger()

ldap_port_instance = None

async def get_ldap_port_instance():
    global ldap_port_instance
    if ldap_port_instance is None:
        from app.controllers.OpenLDAP.openldap_controller import OpenLDAPController
        from app.ports.outbound.ldap_port import LDAPPort
        ldap_controller = OpenLDAPController()
        logger.info("Creating new LDAPPort instance with OpenLDAPController.", controller=ldap_controller)
        ldap_port_instance = LDAPPort(ldap_controller)
        logger.info("LDAPPort singleton instance created.", instance=ldap_port_instance)
    return ldap_port_instance#