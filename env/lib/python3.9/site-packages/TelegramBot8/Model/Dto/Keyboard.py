import json

from ..Reqest import BaseRequest


class Keyboard:
    body = {}

    def __init__(self):
        self.body = {}

    def addParameter(self, key, value, not_required=False) -> {}:
        if not_required or None is value:
            return self.body
        self.body[key] = value
        return self.body

    def to_dict(self):
        return self.body

    def to_json(self):
        return json.dumps(self.body)


# TODO: Add login_url and callback_game
class InlineKeyboardButton(Keyboard):

    def __init__(self, text, url=None, callback_data=None, switch_inline_query=None,
                 switch_inline_query_current_chat=None, pay=None):
        super(InlineKeyboardButton, self).__init__()
        self.addParameter("text", text)
        self.addParameter("url", url)
        self.addParameter("callback_data", callback_data)
        self.addParameter("switch_inline_query", switch_inline_query)
        self.addParameter("switch_inline_query_current_chat", switch_inline_query_current_chat)
        self.addParameter("pay", pay)


class ReplyKeyboardButton(Keyboard):

    def __init__(self, text, request_contact=None,
                 request_location=None, request_poll=None):
        super(ReplyKeyboardButton, self).__init__()
        self.addParameter("text", text)
        self.addParameter("request_contact", request_contact)
        self.addParameter("request_location", request_location)
        if request_poll is not None:
            self.addParameter("request_poll", {"type": request_poll})


class InlineKeyboard(Keyboard):

    def __init__(self):
        super(InlineKeyboard, self).__init__()
        self.list = []

    def add(self, *keyboards):
        for k in keyboards:
            if isinstance(k, list):
                listKeyboard = list(map(lambda k: k.to_dict(), k))
                self.list.append(listKeyboard)
            else:
                self.list.append([k.to_dict()])

    def insert(self, keyboard: Keyboard, position):
        listOfKeyboard = self.list[position]
        listOfKeyboard.append(keyboard.to_dict())

    def getSize(self) -> int:
        return len(self.list)

    def to_dict(self):
        return {"inline_keyboard": self.list}

    def to_json(self):
        return json.dumps({"inline_keyboard": self.list})


class ReplyKeyboard(InlineKeyboard):
    resize_keyboard = None
    one_time_keyboard = None
    input_field_placeholder = None
    selective = None

    def __init__(self, resize_keyboard=None, one_time_keyboard=None,
                 input_field_placeholder=None, selective=None):
        super(ReplyKeyboard, self).__init__()
        self.resize_keyboard = resize_keyboard
        self.one_time_keyboard = one_time_keyboard
        self.input_field_placeholder = input_field_placeholder
        self.selective = selective

    def to_dict(self):
        self.addParameter("keyboard", self.list)
        self.addParameter("resize_keyboard", self.resize_keyboard)
        self.addParameter("one_time_keyboard", self.one_time_keyboard)
        self.addParameter("input_field_placeholder", self.input_field_placeholder)
        self.addParameter("selective", self.selective)
        return self.body

    def to_json(self):
        return json.dumps(self.to_dict())
