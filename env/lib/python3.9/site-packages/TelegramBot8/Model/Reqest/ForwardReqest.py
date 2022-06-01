from ..Reqest.MessageRequest import MessageRequest


class ForwardRequest(MessageRequest):

    def from_chat_id(self, from_chat_id):
        self.addParameter("from_chat_id", from_chat_id)
        return self

    def message_id(self, message_id):
        self.addParameter("message_id", message_id)
        return self
