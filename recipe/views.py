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
        # print("here")
        if self.action == 'list' : 
            return RecipeSerializer
        return self.serializer_class
    
    def perform_create(self, serializer):
        return serializer.save(user = self.request.user)
    
    def perform_update(self, serializer):
        instance = serializer.save()
        return instance
    

class TagViewSet(ListModelMixin  ,UpdateModelMixin, DestroyModelMixin, viewsets.GenericViewSet) : 

    queryset = Tag.objects.all() 
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return Tag.objects.filter(user = self.request.user).order_by('-name')
   


