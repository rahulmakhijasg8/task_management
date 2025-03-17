import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Task
from asgiref.sync import sync_to_async

class TaskUpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'task_updates'
        self.room_group_name = f"task_{self.room_name}"

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

    async def receive(self, text_data):
        # This method could handle messages from the WebSocket if needed
        pass

    # Receive message from room group
    async def task_update(self, event):
        task_data = event['task_data']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'task_data': task_data
        }))

    @sync_to_async
    def update_task_in_db(self, task_id, task_data):
        task = Task.objects.get(id=task_id)
        task.status = task_data['status']
        task.save()
        return task
