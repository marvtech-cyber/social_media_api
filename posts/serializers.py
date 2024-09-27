# Import the necessary modules from Django Rest Framework
from rest_framework import serializers
# Import the Post, Comment, and Like models from the current app
from .models import Post, Comment, Like

# Define a serializer for Comment objects
class CommentSerializer(serializers.ModelSerializer):
    # Serialize the author field as a read-only field, displaying the author's username
    author = serializers.ReadOnlyField(source='author.username')

    # Define the metadata for the CommentSerializer
    class Meta:
        # Specify the model that this serializer is used to serialize
        model = Comment
        # Specify the fields that should be included in the serialized Comment object
        fields = ['id', 'author', 'content', 'created_at', 'updated_at']

# Define a serializer for Post objects
class PostSerializer(serializers.ModelSerializer):
    # Serialize the author field as a read-only field, displaying the author's username
    author = serializers.ReadOnlyField(source='author.username')
    # Serialize a list of Comment objects associated with the post, using the CommentSerializer
    comments = CommentSerializer(many=True, read_only=True)
    
    # Define the metadata for the PostSerializer
    class Meta:
        # Specify the model that this serializer is used to serialize
        model = Post
        # Specify the fields that should be included in the serialized Post object
        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at']