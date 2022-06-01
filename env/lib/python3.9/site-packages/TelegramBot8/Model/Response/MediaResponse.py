import json
from typing import Any, Optional

from . import Message, from_union, from_none, from_bool, to_class, BaseResponse


class MediaResponse(BaseResponse):
    ok: bool
    result: Message

    def __init__(self, ok: Optional[bool], result: Optional[Message]) -> None:
        self.ok = ok
        self.result = result

    @staticmethod
    def cast(obj: 'BaseResponse') -> 'MediaResponse':
        try:
            return MediaResponse.from_dict(obj.to_dict())
        except Exception:
            raise ReferenceError

    @staticmethod
    def from_dict(obj: Any) -> 'MediaResponse':
        assert isinstance(obj, dict)
        ok = from_union([from_bool, from_none], obj.get("ok"))
        result = from_union([Message.from_dict, from_none], obj.get("result"))
        return MediaResponse(ok, result)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ok"] = from_union([from_bool, from_none], self.ok)
        result["result"] = from_union([lambda x: to_class(Message, x), from_none], self.result)
        return result


def media_response_from_dict(s: Any) -> MediaResponse:
    """

    :rtype: object
    """
    data = json.loads(s)
    return MediaResponse.from_dict(data)


