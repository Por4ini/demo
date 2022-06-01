from ..Model import BotCommand, SetMyCommandRequest


class Commands:
    _commands = {}
    _command_menu = {}

    @staticmethod
    def generate_key(scope, language):
        if language is None:
            language = ""
        ' '.join(scope.values()) + language

    def add_command(self, name: str, func):
        self._commands[name] = func

    def get_command(self, name: str):
        return self._commands[name]

    def has_command(self, name):
        return name in self._commands.keys()

    def get_menu_command_list(self):
        return self._command_menu.values()

    def add_command_menu(self, name: str, func, description, scope, language=None):
        key = self.generate_key(scope, language)
        data = self._command_menu.get(key)
        if data is None:
            data = {"commands": [], "scope": scope, "language_code": language}
        command_list = data["commands"]
        command_list.append(BotCommand().command(name).description(description).build())
        data = SetMyCommandRequest().commands(command_list).scope(data["scope"]) \
            .language_code(None if language is None else data["language_code"]).build()
        self._command_menu[key] = data
