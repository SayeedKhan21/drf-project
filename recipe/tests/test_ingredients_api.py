from core.models import (
    Ingredient ,
)
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from .test_recipe_api import create_user
from recipe.serializers import(
    IngredientSerializer ,
)

INGREDIENTS_URL = reverse('recipe:ingredient-list')

def create_ingredient(user, **data) : 

    payload = {
        'name' : 'sample ingredient'
    }
    payload.update(data)

    return Ingredient.objects.create(user = user , **payload)

def get_detail_ingredient_url(ingredient_id) : 

    return reverse('recipe:ingredient-detail' ,args=[ingredient_id])

class PublicIngredientApiTest(TestCase) : 

    def setUp(self) : 
        self.client = APIClient()

    def auth_required(self) : 

        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code  , status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTest(TestCase) : 

    def setUp(self) : 

        user_data = {
            'email' : 'test@example.com' ,
            'password' : '12345'
        }
        self.user = create_user(**user_data)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient(self) : 

        """  Test ingredient retrieval """

        ingredient = create_ingredient(self.user)
        ingredient = create_ingredient(self.user,  name = 'abc')
        res = self.client.get(INGREDIENTS_URL)
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients , many = True)
        self.assertEqual(res.status_code ,status.HTTP_200_OK)
        self.assertEqual(res.data , serializer.data)

    def test_retrieve_user_specific_ingredient(self) : 

        """  Test ingredient retrieval """
        newUser_data = {
            'email' : 'test2@example.com', 
            'password' : '342897'
        }
        user2 = create_user(**newUser_data)
        create_ingredient(self.user)
        create_ingredient(user2,  name = 'abc')
        res = self.client.get(INGREDIENTS_URL)
        ingredients = Ingredient.objects.filter(user = self.user)
        serializer = IngredientSerializer(ingredients , many = True)
        self.assertEqual(res.status_code ,status.HTTP_200_OK)
        self.assertEqual(res.data , serializer.data)
        self.assertEqual(len(res.data) , 1)


    def test_ingredient_update(self) :


        ingredient = create_ingredient(self.user)
        payload = {
            'name' : 'New ingredient'
        }

        url = get_detail_ingredient_url(ingredient.id)
        res = self.client.patch(url , payload ,format = "json")
        self.assertEqual(res.status_code , status.HTTP_200_OK)
        ingredient.refresh_from_db()
        # print(ingredient.name)
        self.assertEqual(ingredient.name , payload['name'])

    def test_ingredient_delete(self) : 

        """ Test delete functionality """

        ingredient = create_ingredient(self.user)
        url = get_detail_ingredient_url(ingredient.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code , status.HTTP_204_NO_CONTENT)
        ingredients = Ingredient.objects.all()
        self.assertEqual(len(ingredients) , 0)

    

