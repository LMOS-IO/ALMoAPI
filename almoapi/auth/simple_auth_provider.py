import io
import secrets
from typing import Optional
import aiofiles
from pydantic import SecretStr, TypeAdapter, ValidationError
from ruamel.yaml import YAML
from loguru import logger

from auth.interface import AuthInterface
from auth.types import AuthPermission

from config.config import config

_file_validator = TypeAdapter(dict[str, str])


class SimpleAuthProvider(AuthInterface):
    """Simple auth provider"""

    def __init__(self):
        self.tokens = {}
        self.YAML = YAML(typ=["rt", "safe"])
        self.load_keys()

    async def get_permission(self, token: SecretStr) -> AuthPermission:
        """Get the permission level of a token"""
        if token.get_secret_value() not in self.tokens:
            return AuthPermission.unauthenticated
        return self.tokens[token.get_secret_value()]

    async def set_token(self, token: SecretStr, permission: AuthPermission) -> None:
        """Set a token in the auth provider"""
        self.tokens[token.get_secret_value()] = permission
        await self.save_keys()

    async def add_token(
        self, permission: AuthPermission, expiration: Optional[int] = None
    ) -> SecretStr:
        """Add a token to the auth provider"""
        token = SecretStr(secrets.token_hex(16))
        self.tokens[token.get_secret_value()] = permission
        await self.save_keys()
        return token

    def load_keys(self) -> None:
        """Load the keys from a file"""
        try:
            filename = config.auth.simple.filename
            with open(filename, "r", encoding="utf8") as auth_file:
                tokens = _file_validator.validate_python(self.YAML.load(auth_file))
                self.tokens = tokens
        except ValidationError:
            logger.warning(f"Invalid file {filename}")
        except FileNotFoundError:
            logger.warning(f"{filename} not found")

    async def save_keys(self) -> None:
        """Save the keys to a file"""
        filename = config.auth.simple.filename
        async with aiofiles.open(filename, "w", encoding="utf8") as auth_file:
            string_stream = io.StringIO()
            self.YAML.dump(self.tokens, string_stream)
            await auth_file.write(string_stream.getvalue())
