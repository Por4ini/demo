import json


class BaseRequest(object):
    body = {}

    def __init__(self):
        self.body = {}

    @staticmethod
    def builder():
        return BaseRequest()

    def addParameter(self, key, value, not_required=False) -> {}:
        if not_required or None is value:
            return self.body
        self.body[key] = value
        return self.body

    def build(self) -> {}:
        return self.body

    def to_json(self):
        return json.dumps(self.body)