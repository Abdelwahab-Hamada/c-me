import json

from channels.generic.websocket import AsyncWebsocketConsumer

from .utils.event_types import (EventTypes,
                                EventOnline, EventOffline, 
                                EventMessageText,
                                EventIsTyping, EventTypingStopped) 

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        current_user = self.scope["user"]
        if current_user.is_authenticated:
            self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
            self.room_group_name = f"chat_{self.room_name}"

            # Join room group
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
            await self.channel_layer.group_send(
                self.room_group_name, EventOnline(user_pk=str(current_user.pk))._asdict()
            )
        else:
            raise Exception("Login")


    async def disconnect(self, close_code):
        current_user = self.scope["user"]
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
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
            elif event_type == EventTypes.event_is_typing:
                event = EventIsTyping(user_pk=current_user.pk)._asdict()
            elif event_type == EventTypes.event_typing_stopped:
                event = EventTypingStopped(user_pk=current_user.pk)._asdict()

            await self.channel_layer.group_send(
                self.room_group_name, event
            )

    async def user_state_online(self, event):
        await self.send(text_data=json.dumps(event))

    async def user_state_offline(self, event):
        await self.send(text_data=json.dumps(event))

    async def user_message_text(self, event):
        message = event["text"]

        await self.send(text_data=json.dumps(event))

    async def user_typing(self, event):
        await self.send(text_data=json.dumps(event))

    async def user_typing_stopped(self, event):
        await self.send(text_data=json.dumps(event))

