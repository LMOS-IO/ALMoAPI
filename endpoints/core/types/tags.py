from enum import Enum


class Tags(str, Enum):
    """openapi endpoint groups"""

    OpenAI = "OpenAI"
    Admin = "Admin"
    List = "List"
    Tokenisation = "Tokenisation"
    Core = "Core"
    Auth = "Auth"
