from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .serializers import (
    RecipeSerializer ,
    RecipeDetailSerializer ,
    TagSerializer
)
from core.models import (
    Recipe ,
    Tag    
)
from rest_framework.mixins import (
    ListModelMixin ,
    UpdateModelMixin ,
    DestroyModelMixin ,
)
from rest_framework.response import Response
from rest_framework import status
from . import serializers

class RecipeViewSet(viewsets.ModelViewSet) : 
    
    serializer_class = RecipeDetailSerializer
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


    def get_queryset(self):
        return self.queryset.filter(user = self.request.user).order_by('-id')
    
    def get_serializer_class(self):
        # print("here = " , self.action)
        if self.action == 'list' or self.action == 'create' : 
            # print("here")
            # print("tag = " , (self.request.data['tags']))
            # print(self.request.data['tags'])
            return RecipeSerializer
        # print(self.request.data)
        return self.serializer_class
    
    def perform_create(self, serializer):
        # print('here')
        # print("here")
        # print(self.request.data['tags'])
        instance =  serializer.save(user = self.request.user)
        # print("instance = " , instance)
        return instance
    
    def perform_update(self, serializer):
        # print(serializer.validated_data)
        return super().perform_update(serializer)
    

class TagViewSet(ListModelMixin  ,UpdateModelMixin, DestroyModelMixin, viewsets.GenericViewSet) : 

    queryset = Tag.objects.all() 
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return Tag.objects.filter(user = self.request.user).order_by('-name')
   


