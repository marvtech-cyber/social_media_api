from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    # Set the serializer class for the view set
    serializer_class = NotificationSerializer
    # Set the permission classes for the view set
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return a queryset of notifications for the current user, ordered by timestamp
        return Notification.objects.filter(recipient=self.request.user).order_by('-timestamp')

    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        # Get a queryset of all notifications for the current user
        notifications = self.get_queryset()
        # Update the unread field of all notifications to False
        notifications.update(unread=False)
        # Return a response indicating that all notifications have been marked as read
        return Response({'status': 'all notifications marked as read'})

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        # Get the notification object with the given pk
        notification = self.get_object()
        # Set the unread field of the notification to False
        notification.unread = False
        # Save the updated notification object
        notification.save()
        # Return a response indicating that the notification has been marked as read
        return Response({'status': 'notification marked as read'})