import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = f"notification_{self.scope['url_route']['kwargs']['user_id']}"
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))


def notify_user(user_id, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"notification_{user_id}",
        {
            "type": "send_notification",
            "message": message,
        }
    )