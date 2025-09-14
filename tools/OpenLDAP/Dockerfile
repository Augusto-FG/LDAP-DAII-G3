# Use the official OpenLDAP image as the base
FROM osixia/openldap:1.5.0

# Set environment variables for OpenLDAP
ENV LDAP_ORGANISATION="Example Inc." \
    LDAP_DOMAIN="example.com" \
    LDAP_ADMIN_PASSWORD="adminpassword"

# Expose LDAP and LDAPS ports
EXPOSE 389 636

# Copy custom LDIF files (optional, if you need to initialize with specific data)
# COPY init.ldif /container/service/slapd/assets/config/bootstrap/ldif/custom/

# Set the entrypoint to the OpenLDAP entrypoint script
ENTRYPOINT ["/container/tool/run"]

# Command to start the OpenLDAP server
CMD ["--copy-service"]