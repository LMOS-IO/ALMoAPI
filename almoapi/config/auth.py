from pathlib import Path
from typing import Union
from pydantic import BaseModel, Field, RedisDsn
from enum import Enum
from abc import ABC

from config.generics import BaseConfigModel

class AuthProvider(str, Enum):
    NO_AUTH = "none"
    SIMPLE_AUTH = "redis"
    REDIS_AUTH = "simple"


class BaseAuthConfig(BaseModel, ABC):
    """Base model for auth configs"""

    provider: AuthProvider

    class Config:
        use_enum_values = True


class NoAuthProviderConfig(BaseAuthConfig):
    """Model for no auth provider"""

    provider: AuthProvider = AuthProvider.NO_AUTH


class SimpleAuthProviderConfig(BaseAuthConfig):
    """Model for simple auth provider"""

    provider: AuthProvider = AuthProvider.SIMPLE_AUTH
    filename: Path = Field(
        "auth_file_path.yml", description="The path to the auth file"
    )


class RedisAuthProviderConfig(BaseAuthConfig):
    """Model for redis auth provider"""

    provider: AuthProvider = AuthProvider.REDIS_AUTH
    redis_url: RedisDsn = Field(description="The Redis URL for authentication purposes")


AuthProviderConfig = Union[
    NoAuthProviderConfig, SimpleAuthProviderConfig, RedisAuthProviderConfig
]
