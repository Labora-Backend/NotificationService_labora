from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Notification

@api_view(["POST"])
def create_notification(request):
    n = Notification.objects.create(
        user_id=request.data["user_id"],
        payload=request.data["payload"]
    )

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{n.user_id}",
        {
            "type": "send_notification",
            "message": n.payload
        }
    )

    return Response({"status": "sent"})
