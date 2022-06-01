import json
from enum import Enum
from typing import Any, Optional, List

from . import from_int, from_str, from_list, from_bool, from_union, from_none, to_class


class User:
    id: int
    is_bot: bool
    first_name: str
    username: Optional[str]
    language_code: Optional[str]
    _ori_dict = {}

    def __init__(self, id: int, is_bot: bool, first_name: str, username: Optional[str],
                 language_code: Optional[str], original: {}) -> None:
        self.id = id
        self.is_bot = is_bot
        self.first_name = first_name
        self.username = username
        self.language_code = language_code
        self._ori_dict = original

    @staticmethod
    def from_dict(obj: Any) -> 'User':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        is_bot = from_bool(obj.get("is_bot"))
        first_name = from_str(obj.get("first_name"))
        username = from_union([from_str, from_none], obj.get("username"))
        language_code = from_union([from_str, from_none], obj.get("language_code"))
        return User(id, is_bot, first_name, username, language_code, obj)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_union([from_int, from_none], self.id)
        result["is_bot"] = from_union([from_bool, from_none], self.is_bot)
        result["first_name"] = from_union([from_str, from_none], self.first_name)
        result["username"] = from_union([from_str, from_none], self.username)
        result["language_code"] = from_union([from_str, from_none], self.language_code)
        result.update(self._ori_dict)
        return result


class Chat:
    id: int
    type: str
    title: Optional[str]
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    all_members_are_administrators: Optional[bool]
    _ori_dict = {}

    def __init__(self, id: int, type: Optional[str], original: {}, first_name: Optional[str] = None,
                 username: Optional[str] = None,
                 title: Optional[str] = None, all_members_are_administrators: Optional[bool] = None) -> None:
        self.id = id
        self.first_name = first_name
        self.username = username
        self.type = type
        self.title = title
        self.all_members_are_administrators = all_members_are_administrators
        self._ori_dict = original

    @staticmethod
    def from_dict(obj: Any) -> 'Chat':
        assert isinstance(obj, dict)
        id = obj.get("id")
        type = from_str(obj.get("type"))
        first_name = from_union([from_str, from_none], obj.get("first_name"))
        username = from_union([from_str, from_none], obj.get("username"))
        title = from_union([from_str, from_none], obj.get("title"))
        all_members_are_administrators = from_union([from_bool, from_none], obj.get("all_members_are_administrators"))
        return Chat(id, type, obj, first_name, username, title, all_members_are_administrators)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["first_name"] = from_union([from_str, from_none], self.first_name)
        result["username"] = from_union([from_str, from_none], self.username)
        result["type"] = from_str(self.type)
        result["title"] = from_union([from_str, from_none], self.title)
        result["all_members_are_administrators"] = from_union([from_bool, from_none],
                                                              self.all_members_are_administrators)
        result.update(self._ori_dict)
        return result


class MessageEntity:
    offset: int
    length: int
    type: str
    url: Optional[str]
    user: Optional[User]
    language: Optional[str]
    _ori_dict = {}

    def __init__(self, offset: int, length: int, type: str, original: {}, url: Optional[str], user: Optional[User],
                 language: Optional[str]) -> None:
        self.offset = offset
        self.length = length
        self.type = type
        self.url = url
        self.language = language
        self.user = user
        self._ori_dict = original

    @staticmethod
    def from_dict(obj: Any) -> 'MessageEntity':
        assert isinstance(obj, dict)
        offset = from_int(obj.get("offset"))
        length = from_int(obj.get("length"))
        type = from_str(obj.get("type"))
        url = from_union([from_str, from_none], obj.get("url"))
        user = from_union([User.from_dict, from_none], obj.get("user"))
        language = from_union([from_str, from_none], obj.get("language"))
        return MessageEntity(offset, length, type, obj, url, user, language)

    def to_dict(self) -> dict:
        result: dict = {"offset": from_int(self.offset),
                        "length": from_int(self.length),
                        "type": from_str(self.type),
                        "url": from_union([from_str, from_none], self.url),
                        "user": from_union([lambda x: to_class(User, x), from_none], self.user),
                        "language": from_union([from_str, from_none], self.language)
                        }
        result.update(self._ori_dict)
        return result


class Photo:
    file_id: Optional[str]
    file_unique_id: Optional[str]
    file_size: Optional[int]
    width: Optional[int]
    height: Optional[int]
    _ori_dict = {}

    def __init__(self, file_id: Optional[str], file_unique_id: Optional[str], file_size: Optional[int],
                 width: Optional[int], height: Optional[int], original: {}) -> None:
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.file_size = file_size
        self.width = width
        self.height = height
        self._ori_dict = original

    @staticmethod
    def from_dict(obj: Any) -> 'Photo':
        assert isinstance(obj, dict)
        file_id = from_union([from_str, from_none], obj.get("file_id"))
        file_unique_id = from_union([from_str, from_none], obj.get("file_unique_id"))
        file_size = from_union([from_int, from_none], obj.get("file_size"))
        width = from_union([from_int, from_none], obj.get("width"))
        height = from_union([from_int, from_none], obj.get("height"))
        return Photo(file_id, file_unique_id, file_size, width, height, obj)

    def to_dict(self) -> dict:
        result: dict = {}
        result["file_id"] = from_union([from_str, from_none], self.file_id)
        result["file_unique_id"] = from_union([from_str, from_none], self.file_unique_id)
        result["file_size"] = from_union([from_int, from_none], self.file_size)
        result["width"] = from_union([from_int, from_none], self.width)
        result["height"] = from_union([from_int, from_none], self.height)
        result.update(self._ori_dict)
        return result


class Audio:
    file_id: str
    file_unique_id: str
    duration: int
    file_name: Optional[str]
    mime_type: Optional[str]
    performer: Optional[str]
    file_size: Optional[int]
    _ori_dict = {}

    def __init__(self, duration: int, file_name: Optional[str], mime_type: Optional[str],
                 performer: Optional[str], file_id: str, file_unique_id: str, file_size: Optional[int],
                 original: {}) -> None:
        self.duration = duration
        self.file_name = file_name
        self.mime_type = mime_type
        self.performer = performer
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.file_size = file_size
        self._ori_dict = original

    @staticmethod
    def from_dict(obj: Any) -> 'Audio':
        assert isinstance(obj, dict)
        duration = from_int(obj.get("duration"))
        file_name = from_union([from_str, from_none], obj.get("file_name"))
        mime_type = from_union([from_str, from_none], obj.get("mime_type"))
        performer = from_union([from_str, from_none], obj.get("performer"))
        file_id = from_str(obj.get("file_id"))
        file_unique_id = from_str(obj.get("file_unique_id"))
        file_size = from_union([from_int, from_none], obj.get("file_size"))
        return Audio(duration, file_name, mime_type, performer, file_id, file_unique_id, file_size, obj)

    def to_dict(self) -> dict:
        result: dict = {}
        result["duration"] = from_int(self.duration)
        result["file_name"] = from_union([from_str, from_none], self.file_name)
        result["mime_type"] = from_union([from_str, from_none], self.mime_type)
        result["performer"] = from_union([from_str, from_none], self.performer)
        result["file_id"] = from_str(self.file_id)
        result["file_unique_id"] = from_str(self.file_unique_id)
        result["file_size"] = from_union([from_int, from_none], self.file_size)
        result.update(self._ori_dict)
        return result


class Document:
    file_name: Optional[str]
    mime_type: Optional[str]
    thumb: Optional[Photo]
    file_id: str
    file_unique_id: str
    file_size: Optional[int]
    _ori_dict = {}

    def __init__(self, file_name: Optional[str], mime_type: Optional[str], thumb: Optional[Photo],
                 file_id: str, file_unique_id: str, file_size: Optional[int], original: {}) -> None:
        self.file_name = file_name
        self.mime_type = mime_type
        self.thumb = thumb
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.file_size = file_size
        self._ori_dict = original

    @staticmethod
    def from_dict(obj: Any) -> 'Document':
        assert isinstance(obj, dict)
        file_name = from_union([from_str, from_none], obj.get("file_name"))
        mime_type = from_union([from_str, from_none], obj.get("mime_type"))
        thumb = from_union([Photo.from_dict, from_none], obj.get("thumb"))
        file_id = from_str(obj.get("file_id"))
        file_unique_id = from_str(obj.get("file_unique_id"))
        file_size = from_union([from_int, from_none], obj.get("file_size"))
        return Document(file_name, mime_type, thumb, file_id, file_unique_id, file_size, obj)

    def to_dict(self) -> dict:
        result: dict = {}
        result["file_name"] = from_union([from_str, from_none], self.file_name)
        result["mime_type"] = from_union([from_str, from_none], self.mime_type)
        result["thumb"] = from_union([lambda x: to_class(Photo, x), from_none], self.thumb)
        result["file_id"] = from_str(self.file_id)
        result["file_unique_id"] = from_str(self.file_unique_id)
        result["file_size"] = from_union([from_int, from_none], self.file_size)
        result.update(self._ori_dict)
        return result


class Video:
    duration: Optional[int]
    width: Optional[int]
    height: Optional[int]
    file_name: Optional[str]
    mime_type: Optional[str]
    thumb: Optional[Photo]
    file_id: str
    file_unique_id: str
    file_size: Optional[int]
    _ori_dict = {}

    def __init__(self, duration: Optional[int], width: Optional[int], height: Optional[int], file_name: Optional[str],
                 mime_type: Optional[str], thumb: Optional[Photo], file_id: str,
                 file_unique_id: str, file_size: Optional[int], original: {}) -> None:
        self.duration = duration
        self.width = width
        self.height = height
        self.file_name = file_name
        self.mime_type = mime_type
        self.thumb = thumb
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.file_size = file_size
        self._ori_dict = original

    @staticmethod
    def from_dict(obj: Any) -> 'Video':
        assert isinstance(obj, dict)
        duration = from_union([from_int, from_none], obj.get("duration"))
        width = from_union([from_int, from_none], obj.get("width"))
        height = from_union([from_int, from_none], obj.get("height"))
        file_name = from_union([from_str, from_none], obj.get("file_name"))
        mime_type = from_union([from_str, from_none], obj.get("mime_type"))
        thumb = from_union([Photo.from_dict, from_none], obj.get("thumb"))
        file_id = from_str(obj.get("file_id"))
        file_unique_id = from_str(obj.get("file_unique_id"))
        file_size = from_union([from_int, from_none], obj.get("file_size"))
        return Video(duration, width, height, file_name, mime_type, thumb, file_id, file_unique_id, file_size, obj)

    def to_dict(self) -> dict:
        result: dict = {}
        result["duration"] = from_union([from_int, from_none], self.duration)
        result["width"] = from_union([from_int, from_none], self.width)
        result["height"] = from_union([from_int, from_none], self.height)
        result["file_name"] = from_union([from_str, from_none], self.file_name)
        result["mime_type"] = from_union([from_str, from_none], self.mime_type)
        result["thumb"] = from_union([lambda x: to_class(Photo, x), from_none], self.thumb)
        result["file_id"] = from_str(self.file_id)
        result["file_unique_id"] = from_str(self.file_unique_id)
        result["file_size"] = from_union([from_int, from_none], self.file_size)
        result.update(self._ori_dict)
        return result


class Message:
    message_id: int
    message_from: Optional[User]
    chat: Optional[Chat]
    date: int
    text: Optional[str]
    entities: Optional[List[MessageEntity]]
    new_chat_participant: Optional[User]
    new_chat_member: Optional[User]
    new_chat_members: Optional[List[User]]
    photo: Optional[List[Photo]]
    audio: Optional[Audio]
    document: Optional[Document]
    video: Optional[Video]
    _ori_dict = {}

    def __init__(self, message_id: int, message_from: Optional[User], chat: Optional[Chat],
                 date: Optional[int], text: Optional[str], entities: Optional[List[MessageEntity]],
                 new_chat_participant: Optional[User], new_chat_member: Optional[User],
                 new_chat_members: Optional[List[User]], original: {}, photo: Optional[List[Photo]],
                 audio: Optional[Audio], document: Optional[Document], video: Optional[Video]) -> None:
        self.message_id = message_id
        self.message_from = message_from
        self.chat = chat
        self.date = date
        self.text = text
        self.entities = entities
        self.new_chat_participant = new_chat_participant
        self.new_chat_member = new_chat_member
        self.new_chat_members = new_chat_members
        self._ori_dict = original
        self.photo = photo
        self.audio = audio
        self.document = document
        self.video = video

    @staticmethod
    def from_dict(obj: Any) -> 'Message':
        assert isinstance(obj, dict)
        message_id = from_int(obj.get("message_id"))
        message_from = from_union([User.from_dict, from_none], obj.get("from"))
        chat = from_union([Chat.from_dict, from_none], obj.get("chat"))
        date = from_int(obj.get("date"))
        text = from_union([from_str, from_none], obj.get("text"))
        entities = from_union([lambda x: from_list(MessageEntity.from_dict, x), from_none], obj.get("entities"))
        new_chat_participant = from_union([User.from_dict, from_none], obj.get("new_chat_participant"))
        new_chat_member = from_union([User.from_dict, from_none], obj.get("new_chat_member"))
        new_chat_members = from_union([lambda x: from_list(User.from_dict, x), from_none], obj.get("new_chat_members"))
        photo = from_union([lambda x: from_list(Photo.from_dict, x), from_none], obj.get("photo"))
        audio = from_union([Audio.from_dict, from_none], obj.get("audio"))
        document = from_union([Document.from_dict, from_none], obj.get("document"))
        video = from_union([Video.from_dict, from_none], obj.get("video"))
        return Message(message_id, message_from, chat, date, text, entities, new_chat_participant, new_chat_member,
                       new_chat_members, obj, photo, audio, document, video)

    def to_dict(self) -> dict:
        result: dict = {}
        result["message_id"] = from_int(self.message_id)
        result["from"] = from_union([lambda x: to_class(User, x), from_none], self.message_from)
        result["chat"] = from_union([lambda x: to_class(Chat, x), from_none], self.chat)
        result["date"] = from_int(self.date)
        result["text"] = from_union([from_str, from_none], self.text)
        result["entities"] = from_union([lambda x: from_list(lambda x: to_class(MessageEntity, x), x), from_none],
                                        self.entities)
        result["new_chat_participant"] = from_union([lambda x: to_class(User, x), from_none], self.new_chat_participant)
        result["new_chat_member"] = from_union([lambda x: to_class(User, x), from_none], self.new_chat_member)
        result["new_chat_members"] = from_union([lambda x: from_list(lambda x: to_class(User, x), x), from_none],
                                                self.new_chat_members)
        result["photo"] = from_union([lambda x: from_list(lambda x: to_class(Photo, x), x), from_none], self.photo)
        result["audio"] = from_union([lambda x: to_class(Audio, x), from_none], self.audio)
        result["document"] = from_union([lambda x: to_class(Document, x), from_none], self.document)
        result["video"] = from_union([lambda x: to_class(Video, x), from_none], self.video)
        result.update(self._ori_dict)
        return result


class CallBackQuery:
    id: str
    from_user: User
    message: Optional[Message]
    inline_message_id: Optional[str]
    chat_instance: Optional[str]
    data: Optional[str]
    game_short_name: Optional[str]
    _ori_dict = {}
    bot = None

    def set_instance_of_bot(self, bot):
        self.bot = bot

    def answer(self, text: str = None, show_alert: bool = None, url_request: str = None, cache_time: int = None):
        if self.bot is None:
            raise Exception("Bot instance is not created")
        else:
            self.bot.answer_call_back(self.id, text, show_alert, url_request, cache_time)

    def __init__(self, id: str, from_user: User, message: Optional[Message], inline_message_id: Optional[str],
                 chat_instance: Optional[str], data: Optional[str], game_short_name: Optional[str],
                 original: {}) -> None:
        self.id = id
        self.from_user = from_user
        self.message = message
        self.inline_message_id = inline_message_id
        self.chat_instance = chat_instance
        self.data = data
        self.game_short_name = game_short_name
        self._ori_dict = original

    @staticmethod
    def from_dict(obj: Any) -> 'CallBackQuery':
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        from_user = User.from_dict(obj.get("from"))
        message = from_union([Message.from_dict, from_none], obj.get("message"))
        inline_message_id = from_union([from_str, from_none], obj.get("inline_message_id"))
        chat_instance = from_union([from_str, from_none], obj.get("chat_instance"))
        data = from_union([from_str, from_none], obj.get("data"))
        game_short_name = from_union([from_str, from_none], obj.get("game_short_name"))
        return CallBackQuery(id, from_user, message, inline_message_id, chat_instance, data, game_short_name, obj)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["from"] = from_union([lambda x: to_class(User, x), from_none], self.from_user)
        result["message"] = from_union([lambda x: to_class(Message, x), from_none], self.message)
        result["inline_message_id"] = from_union([from_str, from_none], self.inline_message_id)
        result["chat_instance"] = from_union([from_str, from_none], self.chat_instance)
        result["data"] = from_union([from_str, from_none], self.data)
        result["game_short_name"] = from_union([from_str, from_none], self.game_short_name)
        result.update(self._ori_dict)
        return result


class Update:
    update_id: int
    message: Optional[Message]
    callback_query: Optional[CallBackQuery]
    _ori_dict = {}

    def __init__(self, update_id: int, message: Optional[Message], original: {},
                 callback_query: Optional[CallBackQuery]) -> None:
        self.update_id = update_id
        self.message = message
        self._ori_dict = original
        self.callback_query = callback_query

    def getNextUpdateID(self) -> int:
        return self.update_id + 1

    def hasMessage(self) -> bool:
        return self.message is not None

    def hasCallBack(self) -> bool:
        return self.callback_query is not None

    def isBotCommand(self) -> bool:
        return self.hasMessage() and \
               self.message.entities is not None and \
               self.message.entities[0].type == "bot_command" and \
               self.message is not None and self.message.entities is not None

    @staticmethod
    def from_dict(obj: Any) -> 'Update':
        assert isinstance(obj, dict)
        update_id = from_int(obj.get("update_id"))
        message = from_union([Message.from_dict, from_none], obj.get("message"))
        callback_query = from_union([CallBackQuery.from_dict, from_none], obj.get("callback_query"))
        return Update(update_id, message, obj, callback_query)

    def to_dict(self) -> dict:
        result: dict = {}
        result["update_id"] = from_int(self.update_id)
        result["message"] = from_union([lambda x: to_class(Message, x), from_none], self.message)
        result["callback_query"] = from_union([lambda x: to_class(CallBackQuery, x), from_none], self.callback_query)
        result.update(self._ori_dict)
        return result


def update_from_dict(s: Any) -> Update:
    data = json.loads(s)
    return Update.from_dict(data)


class UpdateList:
    ok: bool
    result: List[Update]
    _ori_dict = {}

    def __init__(self, ok: bool, result: List[Update], original: {}) -> None:
        self.ok = ok
        self.result = result
        self._ori_dict = original

    @staticmethod
    def from_dict(obj: Any) -> 'UpdateList':
        assert isinstance(obj, dict)
        ok = from_bool(obj.get("ok"))
        result = from_list(Update.from_dict, obj.get("result"))
        return UpdateList(ok, result, obj)

    def to_dict(self) -> dict:
        result: dict = {
            "ok": from_bool(self.ok),
            "result": from_list(lambda x: to_class(Update, x), self.result)
        }
        result.update(self._ori_dict)
        return result


def update_list_from_dict(s: Any) -> UpdateList:
    data = json.loads(s)
    return UpdateList.from_dict(data)


def update_list_to_dict(x: UpdateList) -> Any:
    return to_class(UpdateList, x)


class ParseMode(Enum):
    MarkdownV2 = "MarkdownV2"
    Markdown = "MarkdownV2"
    HTML = "html"
