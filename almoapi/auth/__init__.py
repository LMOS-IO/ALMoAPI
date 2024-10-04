# TODO: convert to the generic interface

from functools import partial
import aiofiles
import io
import secrets
from ruamel.yaml import YAML
from fastapi import Header, HTTPException, Request
from pydantic import BaseModel, Field, SecretStr
from loguru import logger
from typing import Optional

from auth.interface import AuthInterface
from common.utils import coalesce
from config.config import config
from config.auth import AuthProvider

from auth.no_auth_provider import NoAuthProvider
from auth.simple_auth_provider import SimpleAuthProvider
# from auth.redis_auth_provider import RedisAuthProvider

provider_map = {
    AuthProvider.NO_AUTH: NoAuthProvider,
    AuthProvider.SIMPLE_AUTH: SimpleAuthProvider,
    # AuthProvider.REDIS_AUTH: RedisAuthProvider,
}


class AuthProviderManager():
    """Singleton class for managing auth providers"""

    provider: AuthInterface

    def __init__(self):
        """Initialize the auth provider manager"""

        provider_name = config.auth.provider
        self.provider = provider_map.get(provider_name)
        

    

Manager = AuthProviderManager()

def get_key_permission(request: Request):
    """
    Gets the key permission from a request.

    Internal only! Use the depends functions for incoming requests.
    """

    # Give full admin permissions if auth is disabled
    if config.network.disable_auth:
        return "admin"

    # Hyphens are okay here
    test_key = coalesce(
        request.headers.get("x-admin-key"),
        request.headers.get("x-api-key"),
        request.headers.get("authorization"),
    )

    if test_key is None:
        raise ValueError("The provided authentication key is missing.")

    if test_key.lower().startswith("bearer"):
        test_key = test_key.split(" ")[1]

    if AUTH_KEYS.verify_key(test_key, "admin_key"):
        return "admin"
    elif AUTH_KEYS.verify_key(test_key, "api_key"):
        return "api"
    else:
        raise ValueError("The provided authentication key is invalid.")


async def check_api_key(
    x_api_key: str = Header(None), authorization: str = Header(None)
):
    """Check if the API key is valid."""

    # Allow request if auth is disabled
    if config.network.disable_auth:
        return

    if x_api_key:
        if not AUTH_KEYS.verify_key(x_api_key, "api_key"):
            raise HTTPException(401, "Invalid API key")
        return x_api_key

    if authorization:
        split_key = authorization.split(" ")
        if len(split_key) < 2:
            raise HTTPException(401, "Invalid API key")
        if split_key[0].lower() != "bearer" or not AUTH_KEYS.verify_key(
            split_key[1], "api_key"
        ):
            raise HTTPException(401, "Invalid API key")

        return authorization

    raise HTTPException(401, "Please provide an API key")


async def check_admin_key(
    x_admin_key: str = Header(None), authorization: str = Header(None)
):
    """Check if the admin key is valid."""

    # Allow request if auth is disabled
    if config.network.disable_auth:
        return

    if x_admin_key:
        if not AUTH_KEYS.verify_key(x_admin_key, "admin_key"):
            raise HTTPException(401, "Invalid admin key")
        return x_admin_key

    if authorization:
        split_key = authorization.split(" ")
        if len(split_key) < 2:
            raise HTTPException(401, "Invalid admin key")
        if split_key[0].lower() != "bearer" or not AUTH_KEYS.verify_key(
            split_key[1], "admin_key"
        ):
            raise HTTPException(401, "Invalid admin key")
        return authorization

    raise HTTPException(401, "Please provide an admin key")
