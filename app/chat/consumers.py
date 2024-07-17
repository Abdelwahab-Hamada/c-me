import json

from channels.generic.websocket import AsyncWebsocketConsumer

from .utils.event_types import (EventTypes,
                                EventOnline, EventOffline, 
                                EventMessageText, EventMessageFile,
                                EventIsTyping, EventTypingStopped,
                                EventMessageRead) 

from .utils.db import save_text_message, mark_message_as_read

class ChatConsumer(AsyncWebsocketConsumer):
    online_list = []

    async def connect(self):
        current_user = self.scope["user"]
        if current_user.is_authenticated:
            self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
            self.room_group_name = f"chat_{self.room_name}"

            # Join room group
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
            self.online_list.append(current_user.pk)
            await self.channel_layer.group_send(
                self.room_group_name, EventOnline(user_pk=str(current_user.pk))._asdict()
            )
        else:
            raise Exception("Login")


    async def disconnect(self, close_code):
        current_user = self.scope["user"]
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        self.online_list.remove(current_user.pk)
        await self.channel_layer.group_send(
            self.room_group_name, EventOffline(user_pk=str(current_user.pk))._asdict()
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        current_user = self.scope["user"]
        if current_user.is_authenticated:
            remote_event = json.loads(text_data)
            event_type = remote_event["type"]
            event = EventMessageText(user_pk=current_user.pk, text="Unformatted message.")._asdict()

            if event_type == EventTypes.event_message_text:
                event["text"] = remote_event["text"]
                msg_object = await save_text_message(current_user.pk, self.room_name, event["text"])
                event["pk"] = msg_object.pk
            elif event_type == EventTypes.event_message_file:
                text = remote_event["text"]
                url = remote_event["url"]
                event = EventMessageFile(user_pk=current_user.pk, text=text, url=url)._asdict()
                event["pk"] = remote_event["message_id"]
            elif event_type == EventTypes.event_is_typing:
                event = EventIsTyping(user_pk=current_user.pk)._asdict()
            elif event_type == EventTypes.event_typing_stopped:
                event = EventTypingStopped(user_pk=current_user.pk)._asdict()
            elif event_type == EventTypes.event_message_read:
                await mark_message_as_read(remote_event["pk"])
                event = EventMessageRead(user_pk=current_user.pk, pk=remote_event["pk"])._asdict()

            await self.channel_layer.group_send(
                self.room_group_name, event
            )

    async def user_state_online(self, event):
        event["list"] = self.online_list
        await self.send(text_data=json.dumps(event))

    async def user_state_offline(self, event):
        await self.send(text_data=json.dumps(event))

    async def user_message_text(self, event):
        await self.send(text_data=json.dumps(event))

    async def user_message_file(self, event):
        await self.send(text_data=json.dumps(event))

    async def user_typing(self, event):
        await self.send(text_data=json.dumps(event))

    async def user_typing_stopped(self, event):
        await self.send(text_data=json.dumps(event))

    async def user_message_read(self, event):
        await self.send(text_data=json.dumps(event))
