from fastapi import Request


def get_key(request: Request):
    test_key =request.headers.get("authorization")

    if test_key is None:
        raise ValueError("The provided authentication key is missing.")

    if test_key.lower().startswith("bearer"):
        test_key = test_key.split(" ")[1]

    return test_key