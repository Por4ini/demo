from typing import List
import re
import requests
import json
import TelegramBot8.Model.Dto.Constants as const
from TelegramBot8 import SetMyCommandRequest, BotCommandScope, BotCommand, CommandRequestBase, \
    bot_commands_from_dict, ForwardRequest, error_from_dict, BaseResponse, ForwardResponse, forward_from_dict, \
    GetMeResponse, get_me_response_from_dict, success_from_dict, Update, Commands, update_list_from_dict, \
    SettingCommandException, ParseMode, MessageEntity, \
    media_response_from_dict, MissingUrlOrFile, update_from_dict, Keyboard
from TelegramBot8.Model.Reqest.MediaRequest import PhotoRequest, AudioRequest, DocumentRequest, MediaRequestBase, \
    VideoRequest, AnimationRequest, VideoNoteRequest, VoiceRequest
from TelegramBot8.Model.Reqest.UrlRequest import UpdateRequest, SendMessageRequest, AnswerCallbackRequest, \
    WebHookRequest


def _sending_media(url, file, request: MediaRequestBase, media_type: str) -> BaseResponse:
    up = None
    if file:
        poss_name = file.split("/")
        up = {media_type: (poss_name[-1], open(file, 'rb'), "multipart/form-data")}

    response = requests.post(url, files=up, data=request.build())
    if response.status_code == 200:
        return media_response_from_dict(response.text)
    else:
        return error_from_dict(response.text).status_code(response.status_code)


class TeleBot:
    _callback = {}
    _callback_regex = {}
    _text = {}
    _command = Commands()
    headers = {
        'Content-Type': 'application/json'
    }

    def __init__(self, token, limited=None):
        self.base = f"{const.BASE_URL}{token}/"
        self.limited = limited

    def _set_commands(self):

        for command in self._command.get_menu_command_list():
            commands = list(map(lambda x: BotCommand().command(x["command"])
                                .description(x["description"]).build(), command["commands"]))

            if "language_code" in command:
                self.set_my_commands(commands, command["scope"], command["language_code"])
            else:
                self.set_my_commands(commands, command["scope"], None)

    def start(self, response):
        """
        Method used to process the json structure. The method is to help with people using webhook

        :param response: The json format of the update structure
        """
        data = update_from_dict(response)
        self._process_update(data)

    def poll(self, update=None, timeout=1200, allowed_types=None):
        self._set_commands()
        lastUpdate = None
        while True:
            if lastUpdate is None:
                response = self._get_updates(offset=-1, timeout=timeout, allowed_types=allowed_types)
            else:
                response = self._get_updates(offset=lastUpdate.getNextUpdateID(), timeout=timeout,
                                             allowed_types=allowed_types)

            updates = self._generate_updates(response)

            if updates:
                for item in updates:
                    lastUpdate = item
                    self._process_update(item)
                    if update is not None:
                        update(item)

    def _generate_updates(self, response) -> List[Update]:

        if response.get('ok', False) is True:
            return update_list_from_dict(json.dumps(response)).result
        else:
            raise ValueError(response['error'])

    def add_regex_helper(self, regex):
        """Method to look at each chat and if the message matches it will triggers

        :param regex: The regex pattern you want the text to match
        """

        def decorator(func):
            if isinstance(regex, list):
                for t in regex:
                    self._text[t] = func
            else:
                self._text[regex] = func

        return decorator

    def add_command_helper(self, command):
        """This method allows you handle commands send from telegram

        :param command: Add the command you want to handle e.g. /hello_world
        """

        def decorator(func):
            if command is None: return

            if isinstance(command, list):
                for c in command:
                    self._command.add_command(c, func)
            else:
                self._command.add_command(command, func)

        return decorator

    def callback_handler(self, callback_data=None, regex=None):
        """Method yet to be implemented

        :param callback_data:
        :return:
        """

        if regex is None and callback_data is None:
            raise Exception("Both the callback_data and regex are null")

        def decorator(func):
            if callback_data is not None:
                if isinstance(callback_data, list):
                    for c in callback_data:
                        self._callback[c] = func
                else:
                    self._callback[callback_data] = func
            else:
                if isinstance(regex, list):
                    for t in regex:
                        self._callback_regex[t] = func
                else:
                    self._callback_regex[regex] = func
        return decorator


    def add_command_menu_helper(self, command, scope=BotCommandScope.BotCommandScopeDefault(), description="",
                                language=None):
        """This method allows you handle commands send from telegram and allows you to add the \
        command to telegram menu

        :param command: Add the command you want to handle e.g. /hello_world
        :param scope: Use BotCommandScope to view the different scopes. A JSON-serialized object, \
        describing scope of users for which the commands are relevant.
        :param description: Description of the command
        :param language: A two-letter ISO 639-1 language code. If empty, commands will be applied to all users from \
        the given scope, for whose language there are no dedicated commands

        :return: Error or success messages
        """

        def decorator(func):
            if command is None: return

            if isinstance(command, list):
                for c in command:
                    self._command.add_command(c, func)
                self._command.add_command_menu(command[0], func, description, scope[0], language)
            else:
                self._command.add_command(command, func)
                self._command.add_command_menu(command, func, description, scope[0], language)

        return decorator

    def _get_updates(self, offset, timeout, allowed_types) -> {}:
        if allowed_types is None:
            allowed_types = ["message", "callback_query"]

        url = f"{self.base}getUpdates"

        request_body = UpdateRequest() \
            .timeout(timeout) \
            .allowed_updates(allowed_types) \
            .offset(offset, condition=offset is not None) \
            .build()

        response = requests.request("GET", url, headers=self.headers, data=json.dumps(request_body))
        response = json.loads(response.content)

        return response

    def _process_update(self, item: Update) -> bool:
        if item.isBotCommand():
            command = item.message.text[item.message.entities[0].offset:item.message.entities[0].length].split("@")[0]
            if self._command.has_command(command):
                self._command.get_command(command)(item.message)
                return True
        elif item.hasCallBack():
            if item.callback_query.data in self._callback.keys():
                item.callback_query.set_instance_of_bot(self)
                self._callback.get(item.callback_query.data)(item.callback_query)
                return True
            else:
                for p in self._callback_regex.keys():
                    r = re.compile(p)
                    if re.fullmatch(r, item.callback_query.data.lower()):
                        item.callback_query.set_instance_of_bot(self)
                        self._callback_regex.get(p)(item.callback_query)
                        return True
                return False
        elif item.message.text:
            for p in self._text.keys():
                r = re.compile(p)
                if re.fullmatch(r, item.message.text.lower()):
                    self._text.get(p)(item.message)
                    return True
        else:
            print("DEAD ☠️")
        return False

    def get_me(self) -> GetMeResponse:
        """Get's information about the bot

        :return: Returns information about the bot using the GetMeResponse class
        """
        url = f'{self.base}getMe'
        response = requests.post(url, headers={}, data={})
        return get_me_response_from_dict(response.text)

    def send_message(self, chat_id, text, parse_mode: ParseMode = None, disable_web_page_preview=None,
                     disable_notification=None, reply_to_message_id=None,
                     allow_sending_without_reply=None, reply_markup: Keyboard = None):
        """To send message to telegram using this method

        :param chat_id: Unique identifier for the target chat or username of the target channel
        :param text: Text of the message to be sent, 1-4096 characters after entities parsing
        :param parse_mode: Mode for parsing entities in the message text allowing for bold and italic formats. \
         ParseMode enum is available to user
        :param disable_web_page_preview: Disables link previews for links in this message
        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param reply_to_message_id: If the message is a reply, ID of the original message
        :param allow_sending_without_reply: Pass True, if the message should be sent even if the specified replied-to message is not found
        :param reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        """
        url = f"{self.base}sendMessage"
        request_body = SendMessageRequest().text(text).chat_id(chat_id).parse_mode(parse_mode) \
            .disable_web_page_preview(disable_web_page_preview) \
            .disable_notification(disable_notification) \
            .reply_to_message_id(reply_to_message_id) \
            .allow_sending_without_reply(allow_sending_without_reply) \
            .reply_markup(reply_markup.to_dict() if reply_markup is not None else None).build()
        requests.request("POST", url, headers=self.headers, data=json.dumps(request_body))

    def forward_messaged(self, chat_id, from_chat_id, message_id: int,
                         disable_notification: bool = None, protect_content: bool = None) -> ForwardResponse:
        """Use this method to forward messages of any kind. Service messages can't be forwarded.
         On success, the sent Message is returned.


         :param chat_id: Unique identifier for the target chat or username of the target channel
         :param from_chat_id: Unique identifier for the chat group where the original message was sent
         :param message_id: Message id in the chat group specified in from_chat_id
         :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
         :param protect_content: Protects the contents of the forwarded message from forwarding and saving

         :return: ForwardResponse containing the message
        """
        url = f'{self.base}forwardMessage'
        request_body = ForwardRequest()
        request_body = request_body.chat_id(chat_id).from_chat_id(from_chat_id).message_id(message_id). \
            disable_notification(disable_notification).protect_content(protect_content).build()

        response = requests.post(url, headers=self.headers, data=json.dumps(request_body))
        return forward_from_dict(response.text)

    def set_my_commands(self, commands: [BotCommand], scope: {} = None, language_code: str = None) -> BaseResponse:
        """This allows you to set a list of commands in the page where your bot will exist

        :param commands: Is an array of CommandDto. At most 100 commands can be specified.
        :param scope: A JSON-serialized object, describing scope of users for which the commands are relevant.Defaults \
        to BotCommandScopeDefault. You can use the BotCommandScope to get values in
        :param language_code: A two-letter ISO 639-1 language code. If empty, commands will be applied to all users \
        from the given scope, for whose language there are no dedicated commands.

        :return: Error or success messages
        """

        url = f'{self.base}setMyCommands'
        request_body = SetMyCommandRequest().commands(commands).scope(scope) \
            .language_code(language_code).build()

        payload = json.dumps(request_body)
        response = requests.post(url, headers=self.headers, data=payload)
        if response.status_code != 200:
            err = error_from_dict(response.text).status_code(response.status_code)
            raise SettingCommandException(err, f"Error when setting the commands due to {err.to_dict()}")
        else:
            return success_from_dict(response.text)

    def get_my_commands(self, scope: {} = None, language_code: str = None):
        """Use this method to get the current list of the bot's commands for the given scope and user language.

        :param scope: A JSON-serialized object, describing scope of users. Defaults to BotCommandScopeDefault.
        :param language_code: A two-letter ISO 639-1 language code or an empty string

        :return: Array of BotCommand on success. If commands aren't set, an empty list is returned.
        """

        url = f'{self.base}getMyCommands'
        request_body = CommandRequestBase().scope(scope) \
            .language_code(language_code).build()

        payload = json.dumps(request_body)
        response = requests.post(url, headers=self.headers, data=payload)

        if response.status_code != 200:
            return error_from_dict(response.text).status_code(response.status_code)
        else:
            return bot_commands_from_dict(response.text)

    def delete_my_commands(self, scope: {} = None, language_code: str = None) -> BaseResponse:
        """Use this method to delete the list of the bot's commands for the given scope and user language. \
        After deletion, higher level commands will be shown to affected users.

        :param scope: A JSON-serialized object, describing scope of users. Defaults to BotCommandScopeDefault.
        :param language_code: A two-letter ISO 639-1 language code or an empty string

        :return: True on success
        """

        url = f'{self.base}deleteMyCommands'
        request_body = CommandRequestBase().scope(scope) \
            .language_code(language_code).build()

        payload = json.dumps(request_body)
        response = requests.post(url, headers=self.headers, data=payload)

        if response.status_code != 200:
            return error_from_dict(response.text).status_code(response.status_code)
        else:
            return success_from_dict(response.text)

    def send_photo(self, chat_id, file=None, image_url=None, caption: str = None, parse_mode: ParseMode = None,
                   caption_entities: List[MessageEntity] = None, disable_notification: bool = None,
                   protect_content: bool = None, reply_to_message_id: int = None,
                   allow_sending_without_reply: bool = None, reply_markup=None) -> BaseResponse:
        """ Method send image to a specific chat

        :param chat_id: Unique identifier for the target chat or username of the target channel
        :param file: The file to which the image file is located at
        :param image_url: The image that you wish to send
        :param reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, \
        custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        :param allow_sending_without_reply: Pass True, if the message should be sent even if the specified replied-to \
        message is not found
        :param reply_to_message_id: If the message is a reply, ID of the original message
        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding and saving
        :param caption: Photo caption (may also be used when resending photos by file_id), 0-1024 characters after \
        entities parsing
        :param parse_mode: Mode for parsing entities in the photo caption. See formatting options for more details.
        :param caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be\
         specified instead of parse_mode
        :return: BaseResponse which can be casted into either MediaResponse or Error
        """
        url = self.base + f"sendPhoto"

        request = PhotoRequest().chat_id(chat_id).caption(caption).parse_mode(parse_mode) \
            .caption_entities(caption_entities).disable_notification(disable_notification). \
            protect_content(protect_content).reply_to_message_id(reply_to_message_id) \
            .allow_sending_without_reply(allow_sending_without_reply).reply_markup(reply_markup)

        if url is None and file is None:
            raise MissingUrlOrFile

        if url:
            request.photo(image_url)

        return _sending_media(url, file, request, "photo")

    def send_audio(self, chat_id, file=None, audio_url=None, caption: str = None, parse_mode: ParseMode = None,
                   caption_entities: List[MessageEntity] = None, disable_notification: bool = None,
                   protect_content: bool = None, reply_to_message_id: int = None,
                   allow_sending_without_reply: bool = None, reply_markup=None, duration: int = None,
                   performer: str = None, title: str = None, thumb: str = None) -> BaseResponse:

        """Use this method to send audio files, if you want Telegram clients to display them in the music player. \
        Your audio must be in the .MP3 or .M4A format. Bots can currently \
        send audio files of up to 50 MB in size, this limit may be changed in the future.
        
        :param chat_id: Unique identifier for the target chat or username of the target channel
        :param file: The file to which the image file is located at
        :param audio_url: The audio that you wish to send
        :param caption: Photo caption (may also be used when resending photos by file_id), 0-1024 characters after \
        entities parsing
        :param parse_mode: Mode for parsing entities in the photo caption. See formatting options for more details.
        :param caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be\
         specified instead of parse_mode
        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding and saving
        :param reply_to_message_id: If the message is a reply, ID of the original message
        :param allow_sending_without_reply: Pass True, if the message should be sent even if the specified replied-to \
        message is not found
        :param reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, \
        custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        :param duration: Duration of the audio in seconds
        :param performer: Performer
        :param title: Track name
        :param thumb: humbnail of the file sent; can be ignored if thumbnail generation for the file is supported \
        server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and \
        height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails \
        can't be reused and can be only uploaded as a new file, so you can pass “attach://<file_attach_name>” if the \
        thumbnail was uploaded using multipart/form-data under <file_attach_name>.
        :return: BaseResponse which can be casted into either MediaResponse or Error
        """

        url = self.base + f"sendAudio"

        request = AudioRequest().chat_id(chat_id).caption(caption).parse_mode(parse_mode) \
            .caption_entities(caption_entities).disable_notification(disable_notification). \
            protect_content(protect_content).reply_to_message_id(reply_to_message_id) \
            .allow_sending_without_reply(allow_sending_without_reply).reply_markup(reply_markup).duration(duration) \
            .performer(performer).title(title).thumb(thumb)

        if url is None and file is None:
            raise MissingUrlOrFile

        if url:
            request.audio(audio_url)

        return _sending_media(url, file, request, "audio")

    def send_document(self, chat_id, file=None, document_url=None, caption: str = None, parse_mode: ParseMode = None,
                      caption_entities: List[MessageEntity] = None, disable_notification: bool = None,
                      protect_content: bool = None, reply_to_message_id: int = None,
                      allow_sending_without_reply: bool = None, reply_markup=None, thumb: str = None) -> BaseResponse:

        """Use this method to send general files. Bots can currently send files of any type of up to 50 MB in size, \
        this limit may be changed in the future.

        :param chat_id: Unique identifier for the target chat or username of the target channel
        :param file: The file to which the image file is located at
        :param document_url: The document that you wish to send
        :param caption: Photo caption (may also be used when resending photos by file_id), 0-1024 characters after \
        entities parsing
        :param parse_mode: Mode for parsing entities in the photo caption. See formatting options for more details.
        :param caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be\
         specified instead of parse_mode
        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding and saving
        :param reply_to_message_id: If the message is a reply, ID of the original message
        :param allow_sending_without_reply: Pass True, if the message should be sent even if the specified replied-to \
        message is not found
        :param reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, \
        custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        :param thumb: humbnail of the file sent; can be ignored if thumbnail generation for the file is supported \
        server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and \
        height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails \
        can't be reused and can be only uploaded as a new file, so you can pass “attach://<file_attach_name>” if the \
        thumbnail was uploaded using multipart/form-data under <file_attach_name>.
        :return: BaseResponse which can be casted into either MediaResponse or Error
        """

        url = self.base + f"sendDocument"

        request: DocumentRequest = DocumentRequest().chat_id(chat_id).caption(caption).parse_mode(parse_mode) \
            .caption_entities(caption_entities).disable_notification(disable_notification). \
            protect_content(protect_content).reply_to_message_id(reply_to_message_id) \
            .allow_sending_without_reply(allow_sending_without_reply).reply_markup(reply_markup).thumb(thumb)

        if url is None and file is None:
            raise MissingUrlOrFile

        if url:
            request.document(document_url)

        return _sending_media(url, file, request, "document")

    def send_video(self, chat_id, file=None, video_url=None, caption: str = None, parse_mode: ParseMode = None,
                   caption_entities: List[MessageEntity] = None, disable_notification: bool = None,
                   protect_content: bool = None, reply_to_message_id: int = None,
                   allow_sending_without_reply: bool = None, reply_markup=None, thumb: str = None,
                   supports_streaming: bool = None, duration: int = None, width: int = None,
                   height: int = None) -> BaseResponse:

        """Use this method to send video files, Telegram clients support mp4 videos \
        (other formats may be sent as Document). Bots can currently send video files of up to 50 MB in size, \
        this limit may be changed in the future.

        :param chat_id: Unique identifier for the target chat or username of the target channel
        :param file: The file to which the image file is located at
        :param video_url: The video that you wish to send
        :param caption: Photo caption (may also be used when resending photos by file_id), 0-1024 characters after \
        entities parsing
        :param parse_mode: Mode for parsing entities in the photo caption. See formatting options for more details.
        :param caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be\
         specified instead of parse_mode
        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding and saving
        :param reply_to_message_id: If the message is a reply, ID of the original message
        :param allow_sending_without_reply: Pass True, if the message should be sent even if the specified replied-to \
        message is not found
        :param reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, \
        custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        :param thumb: humbnail of the file sent; can be ignored if thumbnail generation for the file is supported \
        server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and \
        height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails \
        can't be reused and can be only uploaded as a new file, so you can pass “attach://<file_attach_name>” if the \
        thumbnail was uploaded using multipart/form-data under <file_attach_name>.
        :param duration: Duration of sent video in seconds
        :param supports_streaming: Pass True, if the uploaded video is suitable for streaming
        :param width: Video width
        :param height: Video height
        :return: BaseResponse which can be casted into either MediaResponse or Error
        """

        url = self.base + f"sendVideo"

        request: VideoRequest = VideoRequest().chat_id(chat_id).caption(caption).parse_mode(parse_mode) \
            .caption_entities(caption_entities).disable_notification(disable_notification). \
            protect_content(protect_content).reply_to_message_id(reply_to_message_id) \
            .allow_sending_without_reply(allow_sending_without_reply).reply_markup(reply_markup).thumb(thumb) \
            .duration(duration).supports_streaming(supports_streaming).width(width).height(height)

        if url is None and file is None:
            raise MissingUrlOrFile

        if url:
            request.video(video_url)

        return _sending_media(url, file, request, "video")

    def send_animation(self, chat_id, file=None, animation_url=None, caption: str = None, parse_mode: ParseMode = None,
                       caption_entities: List[MessageEntity] = None, disable_notification: bool = None,
                       protect_content: bool = None, reply_to_message_id: int = None,
                       allow_sending_without_reply: bool = None, reply_markup=None, thumb: str = None,
                       duration: int = None, width: int = None, height: int = None) -> BaseResponse:

        """Use this method to send animation files (GIF or H.264/MPEG-4 AVC video without sound). On success, \
        the sent Message is returned. Bots can currently send animation files of up to 50 MB in size, \
        this limit may be changed in the future.

        :param chat_id: Unique identifier for the target chat or username of the target channel
        :param file: The file to which the image file is located at
        :param animation_url: The animation that you wish to send
        :param caption: Photo caption (may also be used when resending photos by file_id), 0-1024 characters after \
        entities parsing
        :param parse_mode: Mode for parsing entities in the photo caption. See formatting options for more details.
        :param caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be\
         specified instead of parse_mode
        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding and saving
        :param reply_to_message_id: If the message is a reply, ID of the original message
        :param allow_sending_without_reply: Pass True, if the message should be sent even if the specified replied-to \
        message is not found
        :param reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, \
        custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        :param thumb: humbnail of the file sent; can be ignored if thumbnail generation for the file is supported \
        server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and \
        height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails \
        can't be reused and can be only uploaded as a new file, so you can pass “attach://<file_attach_name>” if the \
        thumbnail was uploaded using multipart/form-data under <file_attach_name>.
        :param duration: Duration of sent video in seconds
        :param width: Video width
        :param height: Video height
        :return: BaseResponse which can be casted into either MediaResponse or Error
        """

        url = self.base + f"sendAnimation"

        request: AnimationRequest = AnimationRequest().chat_id(chat_id).caption(caption).parse_mode(parse_mode) \
            .caption_entities(caption_entities).disable_notification(disable_notification). \
            protect_content(protect_content).reply_to_message_id(reply_to_message_id) \
            .allow_sending_without_reply(allow_sending_without_reply).reply_markup(reply_markup).thumb(thumb) \
            .duration(duration).width(width).height(height)

        if url is None and file is None:
            raise MissingUrlOrFile

        if url:
            request.animation(animation_url)

        return _sending_media(url, file, request, "animation")

    def send_voice(self, chat_id, file=None, voice_url=None, caption: str = None, parse_mode: ParseMode = None,
                   caption_entities: List[MessageEntity] = None, disable_notification: bool = None,
                   protect_content: bool = None, reply_to_message_id: int = None,
                   allow_sending_without_reply: bool = None, reply_markup=None) -> BaseResponse:

        """Use this method to send audio files, if you want Telegram clients to display the file as a playable voice \
        message. For this to work, your audio must be in an .OGG file encoded with OPUS (other formats may be sent as \
        Audio or Document). On success, the sent Message is returned. Bots can currently send voice messages of up \
        to 50 MB in size, this limit may be changed in the future.

        :param chat_id: Unique identifier for the target chat or username of the target channel
        :param file: The file to which the image file is located at
        :param voice_url: The animation that you wish to send
        :param caption: Photo caption (may also be used when resending photos by file_id), 0-1024 characters after \
        entities parsing
        :param parse_mode: Mode for parsing entities in the photo caption. See formatting options for more details.
        :param caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be\
         specified instead of parse_mode
        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding and saving
        :param reply_to_message_id: If the message is a reply, ID of the original message
        :param allow_sending_without_reply: Pass True, if the message should be sent even if the specified replied-to \
        message is not found
        :param reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, \
        custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        :return: BaseResponse which can be casted into either MediaResponse or Error
        """

        url = self.base + f"sendVoice"

        request: VoiceRequest = VoiceRequest().chat_id(chat_id).caption(caption).parse_mode(parse_mode) \
            .caption_entities(caption_entities).disable_notification(disable_notification). \
            protect_content(protect_content).reply_to_message_id(reply_to_message_id) \
            .allow_sending_without_reply(allow_sending_without_reply).reply_markup(reply_markup)

        if url is None and file is None:
            raise MissingUrlOrFile

        if url:
            request.voice(voice_url)

        return _sending_media(url, file, request, "voice")

    def send_video_note(self, chat_id, file=None, video_note_url=None, disable_notification: bool = None,
                        protect_content: bool = None, reply_to_message_id: int = None,
                        allow_sending_without_reply: bool = None, reply_markup=None, thumb: str = None,
                        length: int = None, duration: int = None) -> BaseResponse:

        """Rounded square mp4 videos of up to 1 minute long. Use this method to send video messages.\
         On success, the sent Message is returned.

        :param length:	Video width and height, i.e. diameter of the video message
        :param chat_id: Unique identifier for the target chat or username of the target channel
        :param file: The file to which the image file is located at
        :param video_note_url: The video that you wish to send
         specified instead of parse_mode
        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding and saving
        :param reply_to_message_id: If the message is a reply, ID of the original message
        :param allow_sending_without_reply: Pass True, if the message should be sent even if the specified replied-to \
        message is not found
        :param reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, \
        custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        :param thumb: humbnail of the file sent; can be ignored if thumbnail generation for the file is supported \
        server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and \
        height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails \
        can't be reused and can be only uploaded as a new file, so you can pass “attach://<file_attach_name>” if the \
        thumbnail was uploaded using multipart/form-data under <file_attach_name>.
        :param duration: Duration of sent video in seconds
        :return: BaseResponse which can be casted into either MediaResponse or Error
        """

        url = self.base + f"sendVideoNote"

        request: VideoNoteRequest = VideoNoteRequest().chat_id(chat_id).disable_notification(disable_notification). \
            protect_content(protect_content).reply_to_message_id(reply_to_message_id) \
            .allow_sending_without_reply(allow_sending_without_reply).reply_markup(reply_markup).thumb(thumb) \
            .duration(duration).length(length)

        if url is None and file is None:
            raise MissingUrlOrFile

        if url:
            request.video_note(video_note_url)

        return _sending_media(url, file, request, "video_note")

    def answer_call_back(self, callback_query_id: str, text: str = None, show_alert: bool = None,
                         url_request: str = None, cache_time: int = None) -> BaseResponse:
        """
        Use this method to send answers to callback queries sent from inline keyboards. The answer will be displayed \
         to the user as a notification at the top of the chat screen or as an alert.
        :param callback_query_id: Unique identifier for the query to be answered
        :param text: Text of the notification. If not specified, nothing will be shown to the user, 0-200 characters
        :param show_alert: If True, an alert will be shown by the client instead of a notification at the top \
         of the chat screen. Defaults to false.
        :param url_request: URL that will be opened by the user's client. If you have created a Game and accepted the \
         conditions via @Botfather, specify the URL that opens your game — note that this will only work if the query \
          comes from a callback_game button.
        :param cache_time: 	The maximum amount of time in seconds that the result of the callback query may be cached \
         client-side. Telegram apps will support caching starting in version 3.14. Defaults to 0.
        :return: On success, True is returned as a BaseResponse model
        """
        url = self.base + f"answerCallbackQuery"
        request: AnswerCallbackRequest = AnswerCallbackRequest.builder().callback_query_id(callback_query_id) \
            .text(text).show_alert(show_alert).url(url_request).cache_time(cache_time)

        response = requests.post(url, headers=self.headers, data=request.to_json())

        if response.status_code != 200:
            return error_from_dict(response.text).status_code(response.status_code)
        else:
            return success_from_dict(response.text)

    def set_webhook(self, url_webhook: str, ip_address: str = None, max_connections: str = None,
                    allowed_updates: [str] = None, drop_pending_updates: bool = None) -> BaseResponse:

        """
        Use this method to specify a url and receive incoming updates via an outgoing webhook. Whenever there \
        is an update for the bot, we will send an HTTPS POST request to the specified url, containing a JSON-serialized \
        Update. In case of an unsuccessful request, we will give up after a reasonable amount of attempts

        :param url_webhook: HTTPS url to send updates to. Use an empty string to remove webhook integration
        :param ip_address: The fixed IP address which will be used to send webhook requests instead of the IP address \
        resolved through DNS
        :param max_connections: Maximum allowed number of simultaneous HTTPS connections to the webhook for update\
         delivery, 1-100. Defaults to 40. Use lower values to limit the load on your bot's server, and higher values to increase your bot's throughput.
        :param allowed_updates: A JSON-serialized list of the update types you want your bot to receive. For example,\
         specify [“message”, “edited_channel_post”, “callback_query”] to only receive updates of these types. \
         See Update for a complete list of available update types. Specify an empty list to receive all update \
         types except chat_member (default). If not specified, the previous setting will be used. Please note that this\
         parameter doesn't affect updates created before the call to the setWebhook, so unwanted updates may be \
        received for a short period of time.
        :param drop_pending_updates: Pass True to drop all pending updates
        :return: True on success
        """

        self._set_commands()

        url = self.base + f"setWebhook"
        request: WebHookRequest = WebHookRequest.builder().url(url_webhook) \
            .ip_address(ip_address).max_connections(max_connections).drop_pending_updates(drop_pending_updates) \
            .allowed_updates(allowed_updates)

        response = requests.post(url, headers=self.headers, data=request.to_json())

        if response.status_code != 200:
            return error_from_dict(response.text).status_code(response.status_code)
        else:
            return success_from_dict(response.text)
