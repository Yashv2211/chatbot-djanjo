from rest_framework import serializers
from .models import UserPrompt

# Define a serializer for the UserPrompt model.
class UserPromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPrompt # Specify the Django model associated with this serializer.
        fields = ('username', 'prompt')  # Specify which fields should be included in the serialized output.

# Define a custom serializer for handling user responses.
class UserResponseSerializer(serializers.Serializer):
    response = serializers.CharField()  # Define a single field 'response' which is expected to be a character string.