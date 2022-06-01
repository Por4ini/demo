import json
from typing import Any, TypeVar
from . import from_bool, from_int, from_str, to_class

T = TypeVar("T")


class BaseResponse:
    status_code: int = 200

    @staticmethod
    def from_dict(obj: Any):
        raise NotImplemented

    def to_dict(self):
        raise NotImplemented


class Success(BaseResponse):
    ok: bool
    result: bool

    def __init__(self, ok: bool, result: bool) -> None:
        self.ok = ok
        self.result = result
        self.status_code = 200

    @staticmethod
    def from_dict(obj: Any) -> 'Success':
        assert isinstance(obj, dict)
        ok = from_bool(obj.get("ok"))
        result = from_bool(obj.get("result"))
        return Success(ok, result)

    def to_dict(self) -> dict:
        result: dict = {"ok": from_bool(self.ok), "result": from_bool(self.result)}
        return result


def success_from_dict(s: Any) -> Success:
    data = json.loads(s)
    return Success.from_dict(data)


def success_to_dict(x: Success) -> Any:
    return to_class(Success, x)


class Error(BaseResponse):
    ok: bool
    error_code: int
    description: str

    def __init__(self, ok: bool, error_code: int, description: str) -> None:
        self.ok = ok
        self.error_code = error_code
        self.description = description

    def status_code(self, status_code) -> 'Error':
        self.status_code = status_code
        return self

    @staticmethod
    def from_dict(obj: Any) -> 'Error':
        assert isinstance(obj, dict)
        ok = from_bool(obj.get("ok"))
        error_code = from_int(obj.get("error_code"))
        description = from_str(obj.get("description"))
        return Error(ok, error_code, description)

    def to_dict(self) -> dict:
        result: dict = {"ok": from_bool(self.ok), "error_code": from_int(self.error_code),
                        "description": from_str(self.description)}
        return result


def error_from_dict(s: Any) -> Error:
    data = json.loads(s)
    return Error.from_dict(data)


def error_to_dict(x: Error) -> Any:
    return to_class(Error, x)
