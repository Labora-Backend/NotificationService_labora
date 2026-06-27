from django.db import models


class Notification(models.Model):

    user_id = models.BigIntegerField(
        db_index=True
    )

    notification_type = models.CharField(
        max_length=100
    )

    title = models.CharField(
        max_length=255
    )

    message = models.TextField()

    payload = models.JSONField(
        default=dict
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]