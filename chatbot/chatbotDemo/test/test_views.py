from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from chatbotDemo.models import UserPrompt, PromptResponse, InternalServerException, JSONException, NetworkException
from chatbotDemo.views import process_user_prompt

class ProcessUserPromptTests(APITestCase):
    def setUp(self):
        # Use the correct URL name as defined in urls.py
        self.url = reverse('process-user-prompt')

  

    def test_invalid_json(self):
        # Simulate invalid JSON data input
        data = 'not a valid json'
        response = self.client.post(self.url, data, content_type='application/json')

        # Check for the proper handling of invalid JSON
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    @patch('chatbotDemo.generate.process_input')
    def test_internal_server_error(self, mock_process_input):
        # Simulate an error in processing the input
        mock_process_input.side_effect = InternalServerException('Mocked server error')

        data = {'username': 'admin', 'prompt': 'Tell me about the weather.'}
        response = self.client.post(self.url, data, format='json')

        # Check for the correct HTTP status when an internal server error occurs
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('error', response.data)

    # Add more tests as needed to cover all scenarios and exceptions

# This setup ensures that your Django test environment can successfully run tests that involve HTTP transactions,

