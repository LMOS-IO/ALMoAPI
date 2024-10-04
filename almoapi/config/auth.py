from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from enum import Enum
from abc import ABC

from config.generics import BaseConfigModel


class AuthProvider(str, Enum):
    NO_AUTH = "no_auth"
    SIMPLE_AUTH = "simple"
    REDIS_AUTH = "redis"


class BaseAuthConfig(BaseModel, ABC):
    """Base model for auth configs"""

    enable: bool = False

    model_config = ConfigDict(use_enum_values=True, validate_default=True)


class NoAuthProviderConfig(BaseAuthConfig):
    """Model for no auth provider"""


class SimpleAuthProviderConfig(BaseAuthConfig):
    """Model for simple auth provider"""

    filename: str = Field("api_tokens.yml", description="The path to the auth file")


class RedisAuthProviderConfig(BaseAuthConfig):
    """Model for redis auth provider"""

    host: str = Field("localhost", description="The Redis host")
    port: int = Field(6379, description="The Redis port")
    username: Optional[str] = Field(None, description="The Redis username")
    password: Optional[str] = Field(None, description="The Redis password")
    ssl: bool = Field(False, description="Enable SSL for Redis")
    ssl_certfile: Optional[str] = Field(
        None,
        description="Path to SSL certificate file for Redis",
    )
    ssl_keyfile: Optional[str] = Field(
        None,
        description="Path to SSL key file for Redis",
    )
    ssl_ca_certs: Optional[str] = Field(
        None,
        description="Path to SSL CA certificates file for Redis",
    )
    prefix: str = Field("AlmoAPI-", description="Redis key prefix")


class AuthProviderConfig(BaseConfigModel):
    """Authentication Provider Config
    All auth providers are not enabled from the config by default.
    to override the default (simple), set enabled true"""

    redis: RedisAuthProviderConfig = Field(
        default_factory=RedisAuthProviderConfig,
        description="Redis authentication provider config",
    )
    simple: SimpleAuthProviderConfig = Field(
        default_factory=SimpleAuthProviderConfig,
        description="Simple authentication provider config",
    )
    no_auth: NoAuthProviderConfig = Field(
        default_factory=NoAuthProviderConfig,
        description="No authentication provider config",
    )
