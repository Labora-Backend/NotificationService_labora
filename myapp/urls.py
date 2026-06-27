from django.urls import path

from .views import (
    CreateNotificationView,
    NotificationListView,
    UnreadNotificationCountView,
    MarkNotificationReadView,
    MarkAllNotificationsReadView, InternalNotificationListView, InternalNotificationDetailView,
    InternalBroadcastNotificationView,
)

urlpatterns = [

    # Internal
    path(
        "internal/notifications/create/",
        CreateNotificationView.as_view()
    ),

    # User APIs
    path(
        "notifications/",
        NotificationListView.as_view()
    ),

    path(
        "notifications/unread-count/",
        UnreadNotificationCountView.as_view()
    ),

    path(
        "notifications/<int:notification_id>/read/",
        MarkNotificationReadView.as_view()
    ),

    path(
        "notifications/read-all/",
        MarkAllNotificationsReadView.as_view()
    ),
    path(
        "internal/notifications/",
        InternalNotificationListView.as_view()
    ),

    path(
        "internal/notifications/<int:notification_id>/",
        InternalNotificationDetailView.as_view()
    ),
    path(
        "internal/notifications/broadcast/",
        InternalBroadcastNotificationView.as_view()
    ),

]