from typing import NamedTuple

class EventTypes:
    event_online = "user.state.online"
    event_offline = "user.state.offline"
    event_message_text = "user.message.text"
    event_message_file = "user.message.file"
    event_is_typing = "user.typing"
    event_typing_stopped = "user.typing.stopped"
    event_message_read = "user.message.read"

class EventOnline(NamedTuple):
    user_pk: str
    type: str = EventTypes.event_online

class EventOffline(NamedTuple):
    user_pk: str
    type: str = EventTypes.event_offline

class EventMessageText(NamedTuple):
    user_pk: str
    text: str
    type: str = EventTypes.event_message_text

class EventMessageFile(NamedTuple):
    user_pk: str
    text: str
    url: str
    type: str = EventTypes.event_message_file

class EventIsTyping(NamedTuple):
    user_pk: str
    type: str = EventTypes.event_is_typing

class EventTypingStopped(NamedTuple):
    user_pk: str
    type: str = EventTypes.event_typing_stopped

class EventMessageRead(NamedTuple):
    pk: str
    user_pk: str
    type: str = EventTypes.event_message_read