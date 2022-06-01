import json
from typing import Any, Optional

from . import from_int, from_bool, from_str, to_class, From, Chat


class Result:
    message_id: int
    result_from: From
    chat: Chat
    date: int
    forward_from: From
    forward_date: int
    text: str

    def __init__(self, message_id: int, result_from: From, chat: Chat, date: int, forward_from: From, forward_date: int,
                 text: str) -> None:
        self.message_id = message_id
        self.result_from = result_from
        self.chat = chat
        self.date = date
        self.forward_from = forward_from
        self.forward_date = forward_date
        self.text = text

    @staticmethod
    def from_dict(obj: Any) -> 'SetMyCommandRequest':
        assert isinstance(obj, dict)
        message_id = from_int(obj.get("message_id"))
        result_from = From.from_dict(obj.get("from"))
        chat = Chat.from_dict(obj.get("chat"))
        date = from_int(obj.get("date"))
        forward_from = From.from_dict(obj.get("forward_from"))
        forward_date = from_int(obj.get("forward_date"))
        text = from_str(obj.get("text"))
        return Result(message_id, result_from, chat, date, forward_from, forward_date, text)

    def to_dict(self) -> dict:
        result: dict = {}
        result["message_id"] = from_int(self.message_id)
        result["from"] = to_class(From, self.result_from)
        result["chat"] = to_class(Chat, self.chat)
        result["date"] = from_int(self.date)
        result["forward_from"] = to_class(From, self.forward_from)
        result["forward_date"] = from_int(self.forward_date)
        result["text"] = from_str(self.text)
        return result


class ForwardResponse:
    ok: bool
    result: Result

    def __init__(self, ok: bool, result: Result) -> None:
        self.ok = ok
        self.result = result

    @staticmethod
    def from_dict(obj: Any) -> 'ForwardResponse':
        assert isinstance(obj, dict)
        ok = from_bool(obj.get("ok"))
        result = Result.from_dict(obj.get("result"))
        return ForwardResponse(ok, result)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ok"] = from_bool(self.ok)
        result["result"] = to_class(Result, self.result)
        return result


def forward_from_dict(s: Any) -> ForwardResponse:
    data = json.loads(s)
    return ForwardResponse.from_dict(data)


def forward_to_dict(x: ForwardResponse) -> Any:
    return to_class(ForwardResponse, x)
