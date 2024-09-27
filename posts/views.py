# Import the necessary modules from Django Rest Framework
from rest_framework import viewsets, permissions, filters, generics, status
# Import the DjangoFilterBackend for filtering
from django_filters.rest_framework import DjangoFilterBackend
# Import the Post, Comment, and Like models from the current app
from .models import Post, Comment, Like
# Import the PostSerializer and CommentSerializer from the current app
from .serializers import PostSerializer, CommentSerializer
# Import the custom permission class IsAuthorOrReadOnly from the current app
from .permissions import IsAuthorOrReadOnly
# Import the Response class from Django Rest Framework
from rest_framework.response import Response
# Import the action decorator from Django Rest Framework
from rest_framework.decorators import action
from notifications.models import Notification

# Define a viewset for Post objects
class PostViewSet(viewsets.ModelViewSet):
    # Specify the queryset for the viewset
    queryset = Post.objects.all()
    # Specify the serializer class for the viewset
    serializer_class = PostSerializer
    # Specify the permission classes for the viewset
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    # Specify the filter backends for the viewset
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    # Specify the search fields for the viewset
    search_fields = ['title', 'content']
    # Specify the filterset fields for the viewset
    filterset_fields = ['author']

    # Override the perform_create method to set the author of the post
    def perform_create(self, serializer):
        # Save the post with the current user as the author
        serializer.save(author=self.request.user)
    

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        # Get the post object
        post = self.get_object()
        
        # Get the user who is liking the post
        user = request.user
        
        # Check if a Like object already exists for this user and post
        like, created = Like.objects.get_or_create(user=user, post=post)
        
        if created:
            # If a Like object was created, it means the user hasn't liked the post before
            # So create a new notification for the post author
            Notification.objects.create(
                recipient=post.author,  # The post author
                actor=user,  # The user who liked the post
                verb='liked',  # The action taken
                target=post  # The post that was liked
            )
            return Response({'status': 'post liked'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'post already liked'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        # Get the post object
        post = self.get_object()
        
        # Get the user who is unliking the post
        user = request.user
        
        # Get the Like object for this user and post (if it exists)
        like = Like.objects.filter(user=user, post=post).first()
        
        if like:
            # If a Like object was found, delete it
            like.delete()
            return Response({'status': 'post unliked'}, status=status.HTTP_200_OK)
        return Response({'status': 'post not liked'}, status=status.HTTP_400_BAD_REQUEST)
  

# Define a viewset for Comment objects
class CommentViewSet(viewsets.ModelViewSet):
    # Specify the queryset for the viewset
    queryset = Comment.objects.all()
    # Specify the serializer class for the viewset
    serializer_class = CommentSerializer
    # Specify the permission classes for the viewset
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    # Override the perform_create method to set the author of the comment
    def perform_create(self, serializer):
        # Save the comment with the current user as the author
        serializer.save(author=self.request.user)
        # Get the post associated with the comment
        post = Post.objects.get(pk=self.kwargs['post_pk'])
       
class FeedView(generics.ListAPIView):
    # Specify the serializer class for the Post model
    serializer_class = PostSerializer
    
    # Only authenticated users are allowed to view the feed
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Get the current user from the request object
        user = self.request.user
        
        # Get all the users that the current user is following
        following_users = user.following.all()
        
        # Filter the Post queryset based on the authors in the following_users list
        # and order the queryset by the created_at field in descending order
        queryset = Post.objects.filter(author__in=following_users).order_by('-created_at')
        
        # Return the filtered and ordered queryset
        return queryset

class LikeViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, pk=None):
        # Get the post object with the given pk
        post = generics.get_object_or_404(Post, pk=pk)
        # Get or create a Like object for the current user and the post
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        # If a new Like object was created
        if created:
            # Create a new Notification object for the post author
            Notification.objects.create(
                recipient=post.author,  # The recipient of the notification
                actor=request.user,  # The user who liked the post
                verb='liked',  # The verb for the notification
                target=post  # The target object for the notification
            )
            # Return a response indicating that the post was liked
            return Response({'status': 'post liked'}, status=status.HTTP_201_CREATED)
        # If the Like object already existed
        return Response({'status': 'post already liked'}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        # Get the post object with the given pk
        post = generics.get_object_or_404(Post, pk=pk)
        # Get the Like object for the current user and the post
        like = Like.objects.filter(user=request.user, post=post).first()
        # If a Like object was found
        if like:
            # Delete the Like object
            like.delete()
            # Return a response indicating that the post was unliked
            return Response({'status': 'post unliked'}, status=status.HTTP_200_OK)
        # If no Like object was found
        return Response({'status': 'post not liked'}, status=status.HTTP_400_BAD_REQUEST)