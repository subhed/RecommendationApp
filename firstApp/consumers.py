# chat/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer
from .models import messagesModel
from asgiref.sync import async_to_sync
from .models import categoryModel
from .models import userModel

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        entries_check = categoryModel.objects.filter(category=self.scope['url_route']['kwargs']['room_name']).count()
        if entries_check > 0:
            cat_id = categoryModel.objects.filter(category=self.scope['url_route']['kwargs']['room_name'])[0].catId
            entries = messagesModel.objects.filter(catId=cat_id)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': 'Welcome to Live Chat'
                    })
        self.accept()
                
        # entries_check = categoryModel.objects.filter(category=self.scope['url_route']['kwargs']['room_name']).count()
        # if entries_check > 0:
        #     cat_id = categoryModel.objects.filter(category=self.scope['url_route']['kwargs']['room_name'])[0].catId
        #     entries = messagesModel.objects.filter(catId=cat_id)
        #     print(entries)
        #     for x in entries:
        #         async_to_sync(self.channel_layer.group_send)(
        #             self.room_group_name,
        #             {
        #                 'type': 'chat_message',
        #                 'message': x.message
        #             })

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        # self.commands[data['command']](self, data)
        message = data['message']
        user = data['user']
        user1 = userModel.objects.filter(email=user)[0]

        entries_check = categoryModel.objects.filter(category=self.scope['url_route']['kwargs']['room_name']).count()
        if entries_check > 0:
            cat_id = categoryModel.objects.filter(category=self.scope['url_route']['kwargs']['room_name'])[0]
            print('Checks')
            print(user1)
            msgInstance = messagesModel.objects.create(message=message, catId=cat_id, userId=user1)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
    
    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'message':message
        }))

