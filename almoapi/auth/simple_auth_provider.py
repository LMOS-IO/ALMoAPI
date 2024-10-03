import secrets
from typing import Optional
from auth.interface import AuthInterface
from auth.types import AuthPermission
from pydantic import SecretStr


class SimpleAuthProvider(AuthInterface):
    """Simple auth provider"""

    def __init__(self):
        self.tokens = {}

    def get_permission(self, token: SecretStr) -> AuthPermission:
        """Get the permission level of a token"""
        if token.get_secret_value() not in self.tokens:
            return AuthPermission.unauthenticated
        return self.tokens[token.get_secret_value()].permission

    def set_token(self, token: SecretStr, permission: AuthPermission) -> None:
        """Set a token in the auth provider"""
        self.tokens[token.get_secret_value()] = permission

    def add_token(
        self, permission: AuthPermission, expiration: Optional[int] = None
    ) -> SecretStr:
        """Add a token to the auth provider"""
        token = SecretStr(secrets.token_hex(16))
        self.tokens[token.get_secret_value()] = permission
        return token
