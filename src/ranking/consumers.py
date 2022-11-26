from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import render, get_object_or_404,redirect
import json
from .models import create_ranking,Post_coment
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.ranking_page = self.scope['url_route']['kwargs']['ranking_id']
        #最後の['ranking_id']のところをrankpagedとかにしてた。
        #これはroutingからの引数だよ。まぁ部屋名と言えば良いのかな。
        # 元のコードは→self.room_group_name = 'chat_%s' % self.ranking_page
        self.room_group_name = 'rankpaged_{}'.format(self.ranking_page)

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
        coment = text_data_json['coment']
        name = text_data_json['name']
        await self._save_coment(name,coment)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_coment',
                'name': name,
                'coment': coment
            }
        )


    # Receive message from room group
    async def chat_coment(self, event):
        coment = event['coment']
        name = event['name']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'coment': coment,
            'name' : name
        }))

    @database_sync_to_async
    def _save_coment(self,name,coment):
        ranking = get_object_or_404(create_ranking,id=int(self.ranking_page))
        Post_coment.objects.create(Post_coment_name=name,Post_coment_text=coment,article=ranking)
