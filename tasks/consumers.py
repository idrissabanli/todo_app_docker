import asyncio
import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.core.exceptions import PermissionDenied
from tasks.models import TaskReviews, Tasks
from tasks.views import check_write_comment


class CommentUser(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)
        await self.send({
            "type": "websocket.accept"
        })
        task_slug = self.scope['url_route']['kwargs']['slug']
        chat_room = "thread_{}".format(task_slug)
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )

    async def websocket_receive(self, event):
        print("receive", event)
        front_text = event.get("text", None)
        if front_text is not None:
            loaded_dict_data = json.loads(front_text)
            msg = loaded_dict_data.get("message")
            task_slug = self.scope['url_route']['kwargs']['slug']
            user = self.scope['user']
            username = 'default'
            if user.is_authenticated:
                username = user.email

            myResponse = {
                'message': msg,
                'username': username
            }

            await self.create_comment(task_slug, user, msg)

            # broadcasts the message event to be send
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    "type": "chat_message",
                    "text": json.dumps(myResponse)
                }
            )

    async def chat_message(self, event):
        # send the actual message
        print("message", event)
        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })

    async def disconnect(self, close_code):
        # Leave room group
        print('disaaasss')
        # await self.channel_layer.group_discard(
        #     self.chat_room,
        #     self.channel_name
        # )

    @database_sync_to_async
    def create_comment(self, task_slug, user, review):
        task=Tasks.objects.get(slug=task_slug)
        if not check_write_comment(task, user):
            raise PermissionError
        else:
            return TaskReviews.objects.create(task=task, user=user, review=review)
