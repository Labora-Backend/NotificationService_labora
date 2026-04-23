from django.db import models
class Notification(models.Model):
    user_id = models.IntegerField()
    type = models.CharField(max_length=50)
    payload = models.JSONField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)




