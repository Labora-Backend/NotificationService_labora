from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response

from .permissions.internal_service import (
    IsInternalService
)

from .services import create_notification

from .authentication import CustomJWTAuthentication
from .models import Notification
from .serializers import NotificationSerializer, InternalNotificationListSerializer


class CreateNotificationView(
    APIView
):
    authentication_classes = []

    permission_classes = [
        IsInternalService
    ]

    def post(
            self,
            request
    ):
        notification = create_notification(
            user_id=request.data["user_id"],
            notification_type=request.data["type"],
            title=request.data["title"],
            message=request.data["message"],
            payload=request.data.get(
                "payload",
                {}
            )
        )

        return Response(
            {
                "notification_id":
                    notification.id
            }
        )

class NotificationListView(
        generics.ListAPIView
    ):
        serializer_class = NotificationSerializer

        authentication_classes = [
            CustomJWTAuthentication
        ]

        def get_queryset(self):
            return (
                Notification.objects
                .filter(
                    user_id=self.request.user.id
                )
                .order_by(
                    "-created_at"
                )
            )

class UnreadNotificationCountView(
    APIView
):

    authentication_classes = [
        CustomJWTAuthentication
    ]

    def get(
            self,
            request
    ):

        count = Notification.objects.filter(
            user_id=request.user.id,
            is_read=False
        ).count()

        return Response(
            {
                "unread_count": count
            }
        )

    # Mark Single Notification Read
class MarkNotificationReadView(
    APIView
):

    authentication_classes = [
        CustomJWTAuthentication
    ]

    def patch(
            self,
            request,
            notification_id
    ):

        try:

            notification = Notification.objects.get(
                id=notification_id,
                user_id=request.user.id
            )

        except Notification.DoesNotExist:

            return Response(
                {
                    "error":
                        "Notification not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        notification.is_read = True

        notification.save()

        return Response(
            {
                "message":
                    "Notification marked as read"
            }
        )


class MarkAllNotificationsReadView(
    APIView
):

    authentication_classes = [
        CustomJWTAuthentication
    ]

    def patch(
            self,
            request
    ):

        Notification.objects.filter(
            user_id=request.user.id,
            is_read=False
        ).update(
            is_read=True
        )

        return Response(
            {
                "message":
                    "All notifications marked as read"
            }
        )

class InternalNotificationListView(APIView):
    authentication_classes = []

    permission_classes = [IsInternalService]

    def get(self, request):

        notifications = Notification.objects.all()

        paginator = PageNumberPagination()
        paginator.page_size = 20

        page = paginator.paginate_queryset(
            notifications,
            request
        )

        serializer = InternalNotificationListSerializer(
            page,
            many=True
        )

        return paginator.get_paginated_response(
            serializer.data
        )


class InternalNotificationDetailView(APIView):
    authentication_classes = []

    permission_classes = [IsInternalService]

    def get(self, request, notification_id):

        try:

            notification = Notification.objects.get(
                pk=notification_id
            )

        except Notification.DoesNotExist:

            return Response(
                {
                    "error": "Notification not found"
                },
                status=404
            )

        serializer = InternalNotificationListSerializer(
            notification
        )

        return Response(
            serializer.data
        )
class InternalBroadcastNotificationView(APIView):
    authentication_classes = []

    permission_classes = [IsInternalService]

    def post(self, request):

        title = request.data.get("title")
        message = request.data.get("message")
        notification_type = request.data.get("notification_type")
        payload = request.data.get("payload", {})

        user_ids = request.data.get("user_ids")

        if not title or not message or not notification_type:

            return Response(
                {
                    "error": "title, message and notification_type are required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user_ids:

            return Response(
                {
                    "error": "user_ids is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        for user_id in user_ids:

            create_notification(

                user_id=user_id,

                notification_type=notification_type,

                title=title,

                message=message,

                payload=payload,

            )

        return Response(

            {
                "message": "Notifications sent successfully",
                "total_users": len(user_ids)
            },

            status=status.HTTP_201_CREATED

        )