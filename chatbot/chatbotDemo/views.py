from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import PromptResponse, JSONException, InternalServerException, NetworkException
from .generate import process_input
from django.views.decorators.csrf import csrf_exempt
from .serializers import UserPromptSerializer, UserResponseSerializer
from rest_framework.exceptions import APIException
from json import JSONDecodeError
from rest_framework import status


@api_view(['POST'])
@csrf_exempt
def process_user_prompt(request):
    try:
        try:
            json_data = request.data
        except JSONDecodeError:
            raise JSONException(message="Invalid JSON data", status_code=400)
        
        serializer = UserPromptSerializer(data=json_data)
        if serializer.is_valid():
            serializer.save()
            # Access the validated data
            username = serializer.validated_data['username']
            prompt = serializer.validated_data['prompt']
            if username=='admin':

                raise InternalServerException()
            # Create a dummy response object
            response = process_input(prompt)
            # Serialize the dummy response
            response_serializer = UserResponseSerializer(response)
            # Return the serialized response
            return Response(response_serializer.data, status=201)
        else:
            # If serializer is not valid, return Bad Request
            return Response({'error': str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
    except JSONException as e:
        return Response({'error': str(e)}, status=e.status_code)
    except InternalServerException as e:
        return Response({'error': str(e)}, status=e.status_code)
    except NetworkException as e:
        return Response({'error': str(e)}, status=e.status_code)
    except APIException as e:
        return Response({'error': str(e)}, status=e.status_code)
    except Exception as e:
        return Response({'error': str(e)}, status=500)