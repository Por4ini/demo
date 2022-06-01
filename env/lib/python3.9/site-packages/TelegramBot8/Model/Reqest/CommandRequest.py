import json
from typing import List, Any

from ..Response import from_bool, from_str, from_list, to_class
from . import BaseRequest


class BotCommand(BaseRequest):

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def from_dict(obj: Any) -> 'BotCommand':
        assert isinstance(obj, dict)
        command = from_str(obj.get("command"))
        description = from_str(obj.get("description"))
        return BotCommand().command(command).description(description)

    def command(self, command):
        self.addParameter("command", command)
        return self

    def description(self, description):
        self.addParameter("description", description)
        return self

    def to_dict(self) -> dict:
        return self.body


class CommandRequestBase(BaseRequest):

    def language_code(self, language_code):
        self.addParameter("language_code", language_code)
        return self

    def scope(self, scope):
        self.addParameter("scope", scope)
        return self


class SetMyCommandRequest(CommandRequestBase):

    def commands(self, command: [BotCommand]):
        self.addParameter("commands", command)
        return self


class BotCommandScope:

    @staticmethod
    def BotCommandScopeDefault():
        return {"type": "default"},

    @staticmethod
    def BotCommandScopeAllPrivateChats():
        return {"type": "all_private_chats"},

    @staticmethod
    def BotCommandScopeAllGroupChats():
        return {"type": "all_group_chats"},

    @staticmethod
    def BotCommandScopeAllChatAdministrators():
        return {"type": "all_chat_administrators"},

    @staticmethod
    def BotCommandScopeChat(chat_id):
        return {"type": "chat", "chat_id": chat_id}

    @staticmethod
    def BotCommandScopeChatAdministrators(chat_id):
        return {"type": "chat_administrators", "chat_id": chat_id}

    @staticmethod
    def BotCommandScopeChatMember(chat_id, user_id):
        return {"type": "chat_member", "chat_id": chat_id, "user_id": user_id}


class BotCommands:
    ok: bool
    result: List[BotCommand]

    def __init__(self, ok: bool, result: List[BotCommand]) -> None:
        self.ok = ok
        self.result = result

    @staticmethod
    def from_dict(obj: Any) -> 'BotCommands':
        assert isinstance(obj, dict)
        ok = from_bool(obj.get("ok"))
        result = from_list(BotCommand.from_dict, obj.get("result"))
        return BotCommands(ok, result)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ok"] = from_bool(self.ok)
        result["result"] = from_list(lambda x: to_class(BotCommand, x), self.result)
        return result


def bot_commands_from_dict(s: Any) -> BotCommands:
    data = json.loads(s)
    return BotCommands.from_dict(data)


def bot_commands_to_dict(x: BotCommands) -> Any:
    return to_class(BotCommands, x)
