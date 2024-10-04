from typing import Optional
from auth.interface import AuthInterface
from auth.types import AuthPermission
from pydantic import SecretStr


class NoAuthProvider(AuthInterface):
    """No auth provider"""

    async def get_permission(self, token: SecretStr) -> AuthPermission:
        """Get the permission level of a token"""
        return AuthPermission.admin

    async def set_token(self, token: SecretStr, permission: AuthPermission) -> None:
        """Set a token in the auth provider"""
        pass

    async def add_token(
        self, permission: AuthPermission, expiration: Optional[int] = None
    ) -> SecretStr:
        """Add a token to the auth provider"""
        return SecretStr("dummy api token")

    async def authenticate(self, token: SecretStr, *roles: AuthPermission) -> bool:
        """Authenticate a token"""
        return True
