from core.models import Recipe
from recipe.serializers import (
    RecipeSerializer ,
    RecipeDetailSerializer
    )
from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

RECIPE_URL = reverse('recipe:recipe-list')

def create_recipe(user ,**extra_fields) : 
    payload = {
        'title' : 'sample' ,
        'description' : 'This is sample recipe' ,
        'time_minutes' : 15 ,
        'price' : Decimal('20.2') ,
        'link' : 'http://example.com/recipe.pdf'                                     
    }
    payload.update(extra_fields)

    recipe = Recipe.objects.create(user = user ,**payload)
    return recipe

def get_recipe_detail_url(recipe_id) : 
    return reverse('recipe:recipe-detail' , args=[recipe_id])


class PublicRecipeApiTest(TestCase) : 

    def setUp(self) : 
        client = APIClient()

    def test_auth_required(self) : 

        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code , status.HTTP_401_UNAUTHORIZED)

class PrivateRecipeApiTests(TestCase) : 

    def setUp(self) : 
        user_data = {
            'email' : 'test@example.com' ,
            'password' : '12345'
        }

        user = get_user_model().objects.create_user(**user_data)  
        self.client = APIClient() 
        self.user = user
        self.client.force_authenticate(self.user )

    def test_recipe_retrieve(self) : 

        create_recipe(self.user)
        create_recipe(self.user)
        res =self.client.get(RECIPE_URL) 
        self.assertEqual(res.status_code , status.HTTP_200_OK)

    def test_user_specific_recipes(self) : 

        user2 = get_user_model().objects.create_user(
            email = "test2@example.com" ,
            password = "42334"
        )
        create_recipe(user2)
        create_recipe(self.user)
        # recipe  = create_recipe(self.user)
        recipe = Recipe.objects.filter(user = self.user)        
        serializer = RecipeSerializer(recipe )
        res = self.client.get(RECIPE_URL) 
        # print("res = " , res.data)
        # print("serailizer = " , serializer.data)
        self.assertEqual(res.status_code , status.HTTP_200_OK)
        self.assertEqual(res.data ,serializer.data)

    def test_recipe_detail_retrieve(self) : 
        
        recipe =create_recipe(self.user)
        url = get_recipe_detail_url(recipe.id)
        print(url)
        res = self.client.get(url)
        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.status_code , status.HTTP_200_OK)
        # print(serializer.data)
        self.assertEqual(res.data , serializer.data)

    def test_create_recipe(self) : 
       payload = {
            'title' : 'sample' ,
            'time_minutes' : 15 ,
            'price' : Decimal('20.2') ,
            'link' : 'http://example.com/recipe.pdf'                                     
        }

       res = self.client.post(RECIPE_URL , data = payload)
       self.assertEqual(res.status_code , status.HTTP_201_CREATED)





