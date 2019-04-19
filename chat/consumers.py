from channels.generic.websocket import AsyncWebsocketConsumer
import json

from chat.models import ChatRoom, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # 문자, 숫자, 하이픈 및 마침표만 포함할 수 있음
        self.current_room, self.chat_room_created = ChatRoom.objects.get_or_create(name=self.room_name)

        # Join room group
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, **kwargs):
        text_data_json = json.loads(kwargs['text_data'])
        message = text_data_json['message']
        Message.objects.create(room=self.current_room, message=message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):  # event => {'type': 'chat_message', 'message': message}
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
