import pytest
from unittest.mock import Mock
from datetime import datetime, timezone, timedelta
from app.domain.entities.token import Token
from app.domain.entities.client_credentials import ClientCredentials
from app.domain.services.token_service import TokenService

# Mock de UserService
mock_user_service = Mock()

# Instanciamos el TokenService con el mock
token_service = TokenService(user_service=mock_user_service)

# Creamos un ClientCredentials de prueba
client_credentials = ClientCredentials(client_id="client123", client_secret="secret")

def test_generate_token():
    token = token_service.generate_token(client_credentials)
    assert isinstance(token, Token)
    assert token.sub == "admin"
    assert token.aud == "ldap.com"
    assert token.iss == "auth_server"
    assert "user" in token.roles
    assert token.exp > datetime.now(timezone.utc).timestamp()

def test_refresh_token():
    token = token_service.generate_token(client_credentials)
    refreshed_token = token_service.refresh_token(token)
    assert isinstance(refreshed_token, Token)
    assert refreshed_token.sub == token.sub
    assert refreshed_token.aud == token.aud
    assert refreshed_token.iss == token.iss
    assert refreshed_token.roles == token.roles
    assert refreshed_token.jti == "refreshed_unique_token_id"
    assert refreshed_token.exp > token.exp - 1  # Nuevo expiration time

def test_validate_token_valid():
    token = token_service.generate_token(client_credentials)
    assert token_service.validate_token(token) == True

def test_validate_token_expired():
    expired_token = Token(
        sub="admin",
        aud="ldap.com",
        iss="auth_server",
        exp=int((datetime.now(timezone.utc) - timedelta(minutes=1)).timestamp()),  # Expirado
        nbf=int(datetime.now(timezone.utc).timestamp()),
        iat=int(datetime.now(timezone.utc).timestamp()),
        jti="expired_token",
        roles=["user"]
    )
    assert token_service.validate_token(expired_token) == False
