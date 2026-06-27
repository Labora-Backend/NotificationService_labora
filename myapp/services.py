from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Notification


def create_notification(
        user_id,
        notification_type,
        title,
        message,
        payload=None
):
    """
    Create notification and send real-time WebSocket event.
    """

    if payload is None:
        payload = {}

    # Save notification in database
    notification = Notification.objects.create(
        user_id=user_id,
        notification_type=notification_type,
        title=title,
        message=message,
        payload=payload
    )

    # Prepare websocket data
    notification_data = {
        "id": notification.id,
        "type": notification.notification_type,
        "title": notification.title,
        "message": notification.message,
        "payload": notification.payload,
        "is_read": notification.is_read,
        "created_at": notification.created_at.isoformat()
    }

    # Send to Redis group
    channel_layer = get_channel_layer()

    async_to_sync(
        channel_layer.group_send
    )(
        f"user_{user_id}",
        {
            "type": "send_notification",
            "notification": notification_data
        }
    )

    return notification