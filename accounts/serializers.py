from rest_framework import serializers  # Importing serializers from rest_framework
from django.contrib.auth import get_user_model  # Importing get_user_model from contrib.auth
from rest_framework.authtoken.models import Token  # Importing Token model from rest_framework.authtoken

User = get_user_model()  # Getting the User model

class UserSerializer(serializers.ModelSerializer):  # Defining a serializer for the User model
    password = serializers.CharField()  # Including password field as a CharField
    token = serializers.CharField(read_only=True)  # Including token field as a CharField, read_only set to True

    class Meta:  # Defining the Meta class for the serializer
        model = User  # Setting the User model
        fields = ('id', 'username', 'email', 'password', 'bio', 'profile_picture', 'token')  # Setting the fields to include in the serializer

    def create(self, validated_data):  # Defining the create method for the serializer
        user = get_user_model().objects.create_user(**validated_data)  # Creating a new user with the validated data
        Token.objects.create(user=user)  # Creating a new token for the user
        return user  # Returning the newly created user

    def token_represetation(self, instance):  # Defining the token_representation method for the serializer
        ret = super().token_representation(instance)  # Getting the default representation of the instance
        token, _ = Token.objects.get_or_create(user=instance)  # Getting or creating a token for the user
        ret['token'] = token.key  # Adding the token key to the representation
        return ret  # Returning the updated representation