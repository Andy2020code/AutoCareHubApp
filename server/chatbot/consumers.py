from channels.generic.websocket import AsyncWebsocketConsumer

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("Connected")

    async def disconnect(self, close_code):
        print("Disconnected")
        pass

    async def receive(self, text_data):
        await self.send(text_data)
