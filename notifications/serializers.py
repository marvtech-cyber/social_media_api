from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    # Define a read-only field for the actor's username
    actor = serializers.ReadOnlyField(source='actor.username')
    # Define a serializer method field for the target object
    target = serializers.SerializerMethodField()

    class Meta:
        # Set the model for the serializer
        model = Notification
        # Set the fields to be included in the serialized representation
        fields = ['id', 'recipient', 'actor', 'verb', 'target', 'timestamp', 'unread']

    def get_target(self, obj):
        # This method returns a string representation of the target object
        return str(obj.target)