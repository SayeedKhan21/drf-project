from django.shortcuts import render
from rest_framework import generics
from rest_framework import authentication
from rest_framework.permissions import (
    IsAuthenticated
)
from django.contrib.auth import get_user_model
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import (
    UserSerializer , 
    AuthTokenSerializer
)
# Create your views here.

class CreateUserView(generics.CreateAPIView) : 
    """ Create a new user """
    serializer_class = UserSerializer

class ManageUserView(generics.RetrieveUpdateAPIView) : 
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes =  [IsAuthenticated]

    def get_object(self):
        return self.request.user

    

class CreateTokenView(ObtainAuthToken) : 
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        print(serializer.data)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key
        } , status=status.HTTP_201_CREATED)

 
