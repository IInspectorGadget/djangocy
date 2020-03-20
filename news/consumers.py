from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json
from asgiref.sync import async_to_sync
from news.models import Chat, Message, User
from channels.db import database_sync_to_async

# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['id']
#         self.username = self.scope['url_route']['kwargs']['username']
#         self.room_group_name = 'chat_%s' % self.room_name


#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )
#         self.accept()

#     def disconnect(self, close_code):
#         # Leave room group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )

#     # Receive message from WebSocket
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
        
#         # Send message to room group
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )

#     # Receive message from room group
#     def chat_message(self, event):
#         message = event['message']

#         # Send message to WebSocket
#         self.send(text_data=json.dumps({
#             'message': message
#         }))


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['id']
        self.room_group_name = 'chat_%s' % self.room_name
        # self.email = await database_sync_to_async(self.get_email)(self.username)
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        userId = text_data_json['userId']

        await database_sync_to_async(self.create_row)(userId, int(self.room_name), message)
        await database_sync_to_async(self.chatPubDateSet)(int(self.room_name))

        username = await database_sync_to_async(self.get_username)(userId)
        img = await database_sync_to_async(self.get_img)(userId)
        pub_date = str(await database_sync_to_async(self.get_pubDate)(int(self.room_name)))
        

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'img': img,
                'pub_date': pub_date
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        img = event['img']
        pub_date = event['pub_date']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'img': img,
            'pub_date': pub_date,

        }))


    def get_username(self, userId):
        user = User.objects.get(id = userId)
        return user.username

    def get_img(self, userId):
        user = User.objects.get(id = userId)
        return user.image.url

    def get_pubDate(self, chatId):
        chat = Chat.objects.get(id = chatId)
        return chat.message_set.last().pub_date


    def create_row(self, userId, chatId, mes):
        message = Message()
        user = User.objects.get(id = userId)
        message.author = user
        message.message = mes
        message.chat_id = chatId
        message.save()

    def chatPubDateSet(self, chatId):
        chat = Chat.objects.get(id = chatId)
        chat.last_message_date = chat.message_set.last().pub_date
        chat.save()