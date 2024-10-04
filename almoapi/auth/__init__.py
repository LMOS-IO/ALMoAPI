# TODO: convert to the generic interface

from fastapi import Header, HTTPException, Request
from loguru import logger

from auth.types import AuthPermission
from auth.utils import get_test_key
from auth.interface import AuthInterface
from config.config import config
from config.auth import AuthProvider

from auth.no_auth_provider import NoAuthProvider
from auth.simple_auth_provider import SimpleAuthProvider
from auth.redis_auth_provider import RedisAuthProvider

provider_map = {
    AuthProvider.NO_AUTH: NoAuthProvider,
    AuthProvider.SIMPLE_AUTH: SimpleAuthProvider,
    AuthProvider.REDIS_AUTH: RedisAuthProvider,
}


class AuthProviderManager:
    """Singleton class for managing auth providers"""

    provider: AuthInterface

    def setup(self):
        """Initialize the auth provider manager"""

        provider_name = AuthProvider.SIMPLE_AUTH  # default auth provider

        for provider in config.auth.model_fields:
            if getattr(config.auth, provider).enable:
                provider_name = provider

        logger.info(f"Auth provider: {provider_name}")

        self.provider = provider_map.get(provider_name)()

    async def get_key_permission(self, request: Request):
        test_key = get_test_key(request)
        return await self.provider.get_permission(test_key)

    def require_permission(self, *roles):
        async def internal_require_permission(authorization: str = Header(None)):
            if not authorization:
                raise HTTPException(401, "Please provide an API key")

            test_key = get_test_key(authorization)
            if not await self.provider.authenticate(test_key, *roles):
                raise HTTPException(401, "invalid API key")

        return internal_require_permission


AuthManager = AuthProviderManager()


def get_key_permission():
    pass


check_api_key = AuthManager.require_permission(AuthPermission.api, AuthPermission.admin)

check_admin_key = AuthManager.require_permission(AuthPermission.admin)
