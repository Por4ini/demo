from . import from_int, from_bool, from_str, to_class, from_union, from_none
from typing import Optional, Any


class Chat:
    id: int
    first_name: str
    username: str
    type: str

    def __init__(self, id: int, first_name: str, username: str, type: str) -> None:
        self.id = id
        self.first_name = first_name
        self.username = username
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> 'Chat':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        first_name = from_str(obj.get("first_name"))
        username = from_str(obj.get("username"))
        type = from_str(obj.get("type"))
        return Chat(id, first_name, username, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["first_name"] = from_str(self.first_name)
        result["username"] = from_str(self.username)
        result["type"] = from_str(self.type)
        return result


class From:
    id: int
    is_bot: bool
    first_name: str
    username: str
    language_code: Optional[str]

    def __init__(self, id: int, is_bot: bool, first_name: str, username: str, language_code: Optional[str]) -> None:
        self.id = id
        self.is_bot = is_bot
        self.first_name = first_name
        self.username = username
        self.language_code = language_code

    @staticmethod
    def from_dict(obj: Any) -> 'User':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        is_bot = from_bool(obj.get("is_bot"))
        first_name = from_str(obj.get("first_name"))
        username = from_str(obj.get("username"))
        language_code = from_union([from_str, from_none], obj.get("language_code"))
        return From(id, is_bot, first_name, username, language_code)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["is_bot"] = from_bool(self.is_bot)
        result["first_name"] = from_str(self.first_name)
        result["username"] = from_str(self.username)
        result["language_code"] = from_union([from_str, from_none], self.language_code)


