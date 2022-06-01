from . import BaseRequest
from ... import ParseMode


class MediaRequestBase(BaseRequest):

    def chat_id(self, chat_id):
        self.addParameter("chat_id", chat_id)
        return self

    def caption(self, caption):
        self.addParameter("caption", caption)
        return self

    def parse_mode(self, parse_mode: ParseMode):
        if parse_mode is not None:
            parse_mode = parse_mode.value

        self.addParameter("parse_mode", parse_mode)
        return self

    def caption_entities(self, caption_entities):
        self.addParameter("caption_entities", caption_entities)
        return self

    def disable_notification(self, disable_notification):
        self.addParameter("disable_notification", disable_notification)
        return self

    def protect_content(self, protect_content):
        self.addParameter("protect_content", protect_content)
        return self

    def reply_to_message_id(self, reply_to_message_id):
        self.addParameter("reply_to_message_id", reply_to_message_id)
        return self

    def allow_sending_without_reply(self, allow_sending_without_reply):
        self.addParameter("allow_sending_without_reply", allow_sending_without_reply)
        return self

    def reply_markup(self, reply_markup):
        self.addParameter("reply_markup", reply_markup)
        return self


class PhotoRequest(MediaRequestBase):
    def photo(self, photo):
        self.addParameter("photo", photo)
        return self


class AudioRequest(MediaRequestBase):
    def audio(self, audio):
        self.addParameter("audio", audio)
        return self

    def duration(self, duration):
        self.addParameter("duration", duration)
        return self

    def performer(self, performer):
        self.addParameter("performer", performer)
        return self

    def title(self, title):
        self.addParameter("title", title)
        return self

    def thumb(self, thumb):
        self.addParameter("thumb", thumb)
        return self


class DocumentRequest(MediaRequestBase):
    def document(self, document):
        self.addParameter("document", document)
        return self

    def thumb(self, thumb):
        self.addParameter("thumb", thumb)
        return self


class VideoRequest(MediaRequestBase):
    def video(self, video):
        self.addParameter("video", video)
        return self

    def duration(self, duration):
        self.addParameter("duration", duration)
        return self

    def width(self, width):
        self.addParameter("width", width)
        return self

    def height(self, height):
        self.addParameter("height", height)
        return self

    def thumb(self, thumb):
        self.addParameter("thumb", thumb)
        return self

    def supports_streaming(self, supports_streaming):
        self.addParameter("supports_streaming", supports_streaming)
        return self


class AnimationRequest(MediaRequestBase):
    def animation(self, animation):
        self.addParameter("animation", animation)
        return self

    def duration(self, duration):
        self.addParameter("duration", duration)
        return self

    def width(self, width):
        self.addParameter("width", width)
        return self

    def height(self, height):
        self.addParameter("height", height)
        return self

    def thumb(self, thumb):
        self.addParameter("thumb", thumb)
        return self


class VoiceRequest(MediaRequestBase):
    def voice(self, voice):
        self.addParameter("voice", voice)
        return self


class VideoNoteRequest(MediaRequestBase):
    def video_note(self, video_note):
        self.addParameter("video_note", video_note)
        return self

    def length(self, length):
        self.addParameter("length", length)
        return self

    def duration(self, duration):
        self.addParameter("duration", duration)
        return self

    def thumb(self, thumb):
        self.addParameter("thumb", thumb)
        return self
