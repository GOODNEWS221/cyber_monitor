import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import UserProfile


class LogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]

        # Only allow authenticated users
        if not user.is_authenticated:
            await self.close()
            return
        
        # Each company has its own group 

        self.company_group_name = f"logs_company_{await self.get_company_id(user)}"

        await self.channel_layer.group_add(self.company_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.company_group_name, self.channel_name)

    async def disconnect(self, event):
        await self.send(text_data=json.dumps(event["data"]))

    
    @database_sync_to_async
    def get_company_id(self, user):
        return user.userprofile.company.id