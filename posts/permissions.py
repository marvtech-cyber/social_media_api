# Import the necessary modules
from rest_framework import permissions

# Define a custom permission class to check if the user is the author of an object
class IsAuthorOrReadOnly(permissions.BasePermission):
    # Override the has_object_permission method to check if the user has permission to access the object
    def has_object_permission(self, request, view, obj):
        # If the request method is a safe method, allow access
        if request.method in permissions.SAFE_METHODS:
            return True
        # If the request method is not a safe method, only allow access if the user is the author of the object
        return obj.author == request.user