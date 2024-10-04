from pydantic import BaseModel, Field, SecretStr
from enum import Enum


class AuthPermission(str, Enum):
    """Enum for the permission level of an auth token"""

    admin = "admin"
    api = "api"
    unauthenticated = "unauthenticated"


class AuthToken(BaseModel):
    """Model for an individual auth token"""

    token: SecretStr = Field(description="The token string")
    permission: AuthPermission = Field(description="The permission level of the token")