from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .serializers import (
    RecipeSerializer ,
    RecipeDetailSerializer ,
    TagSerializer ,
    IngredientSerializer 
)
from core.models import (
    Recipe ,
    Tag ,
    Ingredient
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
        if self.action == 'list' or self.action == 'create' : 
            # print(self.request.data['tags'])
            return RecipeSerializer
        # print(self.request.data)
        return self.serializer_class
    
    def perform_create(self, serializer):
        # print(self.request.data['tags'])
        instance =  serializer.save(user = self.request.user)
        # print("instance = " , instance)
        return instance

    

class TagViewSet(ListModelMixin  ,UpdateModelMixin, DestroyModelMixin, viewsets.GenericViewSet) : 

    queryset = Tag.objects.all() 
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return self.queryset.filter(user = self.request.user).order_by('-name')
    

class IngredientViewSet(viewsets.ModelViewSet) : 

    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return self.queryset.filter(user = self.request.user).order_by('-name')
    
    def perform_create(self, serializer):
        instance = serializer.save(user = self.request.user)
        return instance
   


