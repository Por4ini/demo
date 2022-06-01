from ..Model.Response import BaseResponse


class SettingCommandException(Exception):
    error_response = None

    def __init__(self, *args, **kwargs):
        super(SettingCommandException, self).__init__(*args, **kwargs)

    def __init__(self, response: BaseResponse, message):
        super(SettingCommandException, self).__init__(message)
        self.error_response = response

    def getErrorResponse(self) -> BaseResponse:
        return self.error_response


class MissingUrlOrFile(Exception):

    def __init__(self, *args, **kwargs):
        super(MissingUrlOrFile, self).__init__(*args, **kwargs)
