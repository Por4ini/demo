import json
from typing import Any

from . import from_int, from_bool, from_str, to_class


class Result:
    id: int
    is_bot: bool
    first_name: str
    username: str
    can_join_groups: bool
    can_read_all_group_messages: bool
    supports_inline_queries: bool

    def __init__(self, id: int, is_bot: bool, first_name: str, username: str, can_join_groups: bool, can_read_all_group_messages: bool, supports_inline_queries: bool) -> None:
        self.id = id
        self.is_bot = is_bot
        self.first_name = first_name
        self.username = username
        self.can_join_groups = can_join_groups
        self.can_read_all_group_messages = can_read_all_group_messages
        self.supports_inline_queries = supports_inline_queries

    @staticmethod
    def from_dict(obj: Any) -> 'SetMyCommandRequest':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        is_bot = from_bool(obj.get("is_bot"))
        first_name = from_str(obj.get("first_name"))
        username = from_str(obj.get("username"))
        can_join_groups = from_bool(obj.get("can_join_groups"))
        can_read_all_group_messages = from_bool(obj.get("can_read_all_group_messages"))
        supports_inline_queries = from_bool(obj.get("supports_inline_queries"))
        return Result(id, is_bot, first_name, username, can_join_groups, can_read_all_group_messages, supports_inline_queries)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["is_bot"] = from_bool(self.is_bot)
        result["first_name"] = from_str(self.first_name)
        result["username"] = from_str(self.username)
        result["can_join_groups"] = from_bool(self.can_join_groups)
        result["can_read_all_group_messages"] = from_bool(self.can_read_all_group_messages)
        result["supports_inline_queries"] = from_bool(self.supports_inline_queries)
        return result


class GetMeResponse:
    ok: bool
    result: Result

    def __init__(self, ok: bool, result: Result) -> None:
        self.ok = ok
        self.result = result

    @staticmethod
    def from_dict(obj: Any) -> 'GetMeResponse':
        assert isinstance(obj, dict)
        ok = from_bool(obj.get("ok"))
        result = Result.from_dict(obj.get("result"))
        return GetMeResponse(ok, result)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ok"] = from_bool(self.ok)
        result["result"] = to_class(Result, self.result)
        return result


def get_me_response_from_dict(s: Any) -> GetMeResponse:
    data = json.loads(s)
    return GetMeResponse.from_dict(data)


def get_me_response_to_dict(x: GetMeResponse) -> Any:
    return to_class(GetMeResponse, x)
