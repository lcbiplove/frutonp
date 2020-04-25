import json
import asyncio
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import Notif, NotifClick

class NotifConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.send({
            'type': 'websocket.accept'
        })
        user = self.scope['user']
        self.notif_room = f"notif_user_{user.id}"
        # Create a channel group for the post_id
        await self.channel_layer.group_add(
            self.notif_room,
            self.channel_name
        )

    async def notif_send(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event.get('text')
        })

    async def websocket_receive(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': "Hi",
        })
            
    async def websocket_disconnect(self, event):
        print("Notif disconnected", event)
        await self.channel_layer.group_discard(
            self.notif_room,
            self.channel_name
        )
