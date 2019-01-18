'''

synchronous version
'''

import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.consumer import SyncConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        print(f'self.scope["path"]: {self.scope["path"]}')
        print(f'self.scope["headers"]: {self.scope["headers"]}')
        # print(f'self.scope["method"]: {self.scope["method"]}')
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        async_to_sync(self.channel_layer.send)(
            "task-test",
            {
                "type":"test_print",
                "id":123445,
                "message":message,
            }
        )
        async_to_sync(self.channel_layer.send)(
            "task-test",
            {
                "type":"test_print2",
                "id":123455,
                "message":str(self.channel_layer.__dict__),
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

class TestConsumer(SyncConsumer):

    def test_print(self, event):
        print(f'Test: {event}')

    def test_print2(self, event):
        print(f'Test2: {event}')