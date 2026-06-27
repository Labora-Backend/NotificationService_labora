from channels.generic.websocket import AsyncJsonWebsocketConsumer


class NotificationConsumer(
    AsyncJsonWebsocketConsumer
):

    async def connect(self):

        user_id = self.scope.get(
            "user_id"
        )
        if not user_id:
            await self.close()
            return

        self.group_name = (
            f"user_{user_id}"
        )

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    group_name = None

    async def disconnect(self, close_code):

        if self.group_name:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name )

    async def send_notification(
        self,
        event
    ):
        await self.send_json(
            event["notification"]
        )