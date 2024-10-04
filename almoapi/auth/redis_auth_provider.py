import secrets
from typing import Optional
from pydantic import SecretStr
from loguru import logger

from auth.interface import AuthInterface
from auth.types import AuthPermission

from config.config import config
from common.utils import filter_none_values
from common.optional_dependencies import dependencies

if dependencies.redis:
    import redis.asyncio as redis


class RedisAuthProvider(AuthInterface):
    """Reids Backed auth provider"""

    def __init__(self):
        if not dependencies.redis:
            logger.error(
                (
                    "Redis is not installed.",
                    "Please install it via `pip install .[redis]`.",
                )
            )
            exit(1)

        redis_args = filter_none_values(
            {
                "host": config.auth.redis.host,
                "port": config.auth.redis.port,
                "username": config.auth.redis.username,
                "password": config.auth.redis.password,
                "ssl": config.auth.redis.ssl,
                "ssl_cert_reqs": config.auth.redis.ssl_certfile,
                "ssl_keyfile": config.auth.redis.ssl_keyfile,
                "ssl_ca_certs": config.auth.redis.ssl_ca_certs,
            }
        )

        self.Redis = redis.Redis(**redis_args, decode_responses=True)

    async def get_permission(self, token: SecretStr) -> AuthPermission:
        """Get the permission level of a token"""
        if not token.get_secret_value():
            return AuthPermission.unauthenticated

        redis_token = await self.Redis.get(
            f"{config.auth.redis.prefix}key-{token.get_secret_value()}"
        )

        if not redis_token:
            return AuthPermission.unauthenticated

        return redis_token

    async def set_token(
        self,
        token: SecretStr,
        permission: AuthPermission,
        expiration: Optional[int] = None,
    ) -> None:
        """Set a token in the auth provider"""
        args = filter_none_values(
            {
                "name": f"{config.auth.redis.prefix}key-{token.get_secret_value()}",
                "value": permission,
                "ex": expiration,
            }
        )
        await self.Redis.set(**args)

    async def add_token(
        self, permission: AuthPermission, expiration: Optional[int] = None
    ) -> SecretStr:
        """Add a token to the auth provider"""
        token = SecretStr(secrets.token_hex(16))
        await self.set_token(token, permission, expiration)
        return token
