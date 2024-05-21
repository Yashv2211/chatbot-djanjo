from django.db import models

# Define a Django model to store user prompts.
class UserPrompt(models.Model):
    username = models.CharField(max_length=100)  # Field to store the username.
    prompt = models.TextField()  # Field to store the prompt text.

# Class to encapsulate the response to a prompt.
class PromptResponse:
    def __init__(self, response):
        """Initialize with the response text to be stored or handled."""
        self.response = response  # Store the response text passed to the constructor.

# Custom exception class for JSON parsing errors.
class JSONException(Exception):
    def __init__(self, message="JSON parsing error", status_code=400):
        """Initialize the JSONException with a default message and status code."""
        self.message = message  # Error message.
        self.status_code = status_code  # HTTP status code associated with JSON errors.
        super().__init__(self.message)  # Initialize the base class with the message.

# Custom exception class for internal server errors.
class InternalServerException(Exception):
    def __init__(self, message="Internal server error", status_code=500):
        """Initialize the InternalServerException with a default message and status code."""
        self.message = message  # Error message.
        self.status_code = status_code  # HTTP status code associated with server errors.
        super().__init__(self.message)  # Initialize the base class with the message.

# Custom exception class for network-related errors.
class NetworkException(Exception):
    def __init__(self, message="Network error", status_code=500):
        """Initialize the NetworkException with a default message and status code."""
        self.message = message  # Error message.
        self.status_code = status_code  # HTTP status code typically associated with network errors.
        super().__init__(self.message)  # Initialize the base class with the message.
