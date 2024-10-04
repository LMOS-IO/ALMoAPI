"""Types for auth requests."""

from pydantic import BaseModel, Field

from auth.types import AuthPermission


class AuthPermissionResponse(BaseModel):
    permission: AuthPermission = Field(
        description="The permission level of the API key"
    )
