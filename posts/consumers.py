import json
import asyncio
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from channels.layers import get_channel_layer

from .models import Post, Comment, Reply

class CommentConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("Connected", event)
        post_id = self.scope['url_route']['kwargs']['post_id']
        self.post_room = f"post_id_{post_id}"
        # Create a channel group for the post_id
        await self.channel_layer.group_add(
            self.post_room,
            self.channel_name
        )
        await self.send({
            'type': 'websocket.accept'
        })

    async def post_edit_send(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event.get('text')
        })

    async def websocket_receive(self, event):
        received = event.get('text', None)
        if received is not None:
            loaded_data = json.loads(received)
            if loaded_data.get('desc').rfind("_delete") != -1:
                user = {}
            else:
                user = {
                    'user': await self.get_comment_user(loaded_data.get('cm_id')),
                }
            # Append to dictionary
            user['me'] = (self.scope['user']).id
            loaded_data = dict(loaded_data, **user)

            # Broadcast data to post_notif 
            await self.channel_layer.group_send(
                self.post_room,
                {
                    'type': 'post_notif',
                    'text': json.dumps(loaded_data)
                }
            )

    
    # Send event to all group members
    async def post_notif(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event.get('text')
        })
        
            
    async def websocket_disconnect(self, event):
        print("Disconnected", event)

    @database_sync_to_async
    def get_comment_user(self, id):
        comment = get_object_or_404(Comment, pk=id)
        return comment.myuser.name