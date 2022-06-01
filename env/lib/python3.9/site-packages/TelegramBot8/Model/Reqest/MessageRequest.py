from . import BaseRequest


class MessageRequest(BaseRequest):

    def chat_id(self, chat_id):
        self.addParameter("chat_id", chat_id)
        return self

    def disable_notification(self, disable_notification):
        self.addParameter("disable_notification", disable_notification)
        return self

    def protect_content(self, protect_content):
        self.addParameter("protect_content", protect_content)
        return self


class CallBackQueryRequest(BaseRequest):

    @staticmethod
    def builder():
        return CallBackQueryRequest()

    def id(self, id):
        self.addParameter("id", id)
        return self

    def from_user(self, from_user):
        self.addParameter("from", from_user)
        return self

    def message(self, message):
        self.addParameter("message", message)
        return self

    def inline_message_id(self, inline_message_id):
        self.addParameter("inline_message_id", inline_message_id)
        return self

    def chat_instance(self, chat_instance):
        self.addParameter("chat_instance", chat_instance)
        return self

    def data(self, data):
        self.addParameter("data", data)
        return self

    def game_short_name(self, game_short_name):
        self.addParameter("game_short_name", game_short_name)
        return self