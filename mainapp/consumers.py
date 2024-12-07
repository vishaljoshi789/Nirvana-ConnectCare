from channels.generic.websocket import AsyncWebsocketConsumer
import json

class LogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_authenticated:
            self.user = self.scope["user"]
            self.group_name = f"user_{self.user.id}"

            # Join the user's WebSocket group
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.scope["user"].is_authenticated:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def send_log_update(self, event):
        data = event["data"]
        # Send the data to the WebSocket
        await self.send(text_data=json.dumps(data))

class PatientEventConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_authenticated:
            self.user = self.scope["user"]
            self.group_name = f"user_{self.user.id}"

            # Join the user's WebSocket group
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.scope["user"].is_authenticated:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def send_patient_event(self, event):
        data = event["data"]
        # Send the data to the WebSocket
        await self.send(text_data=json.dumps(data))