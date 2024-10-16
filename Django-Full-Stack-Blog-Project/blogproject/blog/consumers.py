import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]  # Kullanıcıyı scope'dan alıyoruz
        self.room_group_name = 'chat_room'  # Tüm kullanıcıları aynı gruba dahil edeceğimiz grup adı

        # Gruba katıl
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': f'{self.user.username} has connected.'
        }))

    def disconnect(self, close_code):
        # Gruptan ayrıl
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.user.username  # Kullanıcı adını alıyoruz

        # Gelen mesajı gruba yayınla
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': user
            }
        )

    def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Mesajı WebSocket üzerinden gönder
        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
            'username': username
        }))
