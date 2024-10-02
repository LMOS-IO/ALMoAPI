from abc import ABC, abstractmethod
from typing import Optional
from auth.types import AuthPermission
from pydantic import SecretStr


class AuthInterface(ABC):
    """Interface for generic auth providers"""

    @abstractmethod
    def get_permission(self, token: SecretStr) -> AuthPermission:
        """Get the permission level of a token"""
        raise NotImplementedError

    @abstractmethod
    def set_token(self, token: SecretStr, permission: AuthPermission) -> None:
        """Set a token in the auth provider"""
        raise NotImplementedError

    @abstractmethod
    def add_token(
        self, permission: AuthPermission, expiration: Optional[int] = None
    ) -> SecretStr:
        """Add a token to the auth provider"""
        raise NotImplementedError

    def authenticate(self, token: SecretStr, *roles: AuthPermission) -> bool:
        """Authenticate a token"""
        return any(role == self.get_permission(token) for role in roles)
