from fastapi import Request
from typing import Union

from pydantic import SecretStr


def get_test_key(request: Union[Request, str]) -> SecretStr:
    if isinstance(request, Request):
        test_key = request.headers.get("authorization")
    else:
        test_key = request

    if test_key is None:
        raise ValueError("The provided authentication key is missing.")

    if test_key.lower().startswith("bearer"):
        test_key = test_key.split(" ")[1]

    return SecretStr(test_key)
