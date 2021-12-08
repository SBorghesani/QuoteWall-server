"""View module for handling requests about user"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.contrib.auth import get_user, get_user_model
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status


class UserView(ViewSet):
    """QuoteWall"""
    def list(self, request):
        """Handle GET requests for current user
        Returns: 
            Response -- JSON serialized user instance
        """
        try: 
            user = request.auth.user

            serializer = UserSerializer(user, many=False, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as ex:
            return Response({'message': "user not found"}, status=status.HTTP_404_NOT_FOUND)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username")