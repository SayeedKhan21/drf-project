from core.models import (
    Recipe ,
    Tag ,
    Ingredient ,
)
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

def create_user(**payload) : 
    return get_user_model().objects.create(**payload)

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

        user2 = create_user( email = "test2@example.com" ,password = "42334")
        create_recipe(user2)
        create_recipe(self.user)
        # recipe  = create_recipe(self.user)
        recipe = Recipe.objects.filter(user = self.user)        
        serializer = RecipeSerializer(recipe, many = True )
        res = self.client.get(RECIPE_URL) 
        # print("res = " , res.data)
        # print("serailizer = " , serializer.data)
        self.assertEqual(res.status_code , status.HTTP_200_OK)
        self.assertEqual(res.data ,serializer.data)

    def test_recipe_detail_retrieve(self) : 
        
        recipe =create_recipe(self.user)
        url = get_recipe_detail_url(recipe.id)
        # print(url)
        res = self.client.get(url)
        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.status_code , status.HTTP_200_OK)
        self.assertEqual(res.data , serializer.data)

    def test_create_recipe(self) : 
       payload = {
            'title' : 'sample' ,
            'time_minutes' : 15 ,
            'price' : 10.5 ,
            'link' : 'http://example.com/recipe.pdf'                                     
        }

       res = self.client.post(RECIPE_URL , data = payload)
       self.assertEqual(res.status_code , status.HTTP_201_CREATED)

    def test_recipe_partial_update_successfull(self) : 

        recipe = create_recipe(self.user)
        changedData = {
            'title' : 'New title' ,
            'description' : 'this is new recipe'
        }        
        url = get_recipe_detail_url(recipe.id)
        res = self.client.patch(url ,changedData)
        self.assertEqual(res.status_code ,status.HTTP_200_OK)
        recipe.refresh_from_db()
        
        self.assertEqual(recipe.title, changedData['title'])

    def test_recipe_full_update_successfull(self) : 

        """ Test full recipe update """

        recipe = create_recipe(self.user)
        changedData = {
            'title' : 'sample' ,
            'description' : 'This is new sample recipe' ,
            'time_minutes' : 25 ,
            'price' : Decimal('10.2') ,
            'link' : 'http://example.com/newrecipe.pdf'             
        }        
        url = get_recipe_detail_url(recipe.id)
        res = self.client.put(url ,changedData)
        self.assertEqual(res.status_code ,status.HTTP_200_OK)
        recipe.refresh_from_db()
        for key ,val in changedData.items() : 
            self.assertEqual(getattr(recipe , key) , val)

    def test_create_recipe_with_tag(self) : 

        """ Test creating a recipe with tags """

        payload = { 
            "title" : "sample" ,
            "description" : "This is sample recipe" ,
            "time_minutes" : 15 ,
            "price" : 200 ,
            "link" : "http://example.com/recipe.pdf" ,
            "tags" : [{"name" : "good" } ,{ "name" : "average" }]
        }
        print(RECIPE_URL)
        res = self.client.post(RECIPE_URL , payload ,format = "json")
        self.assertEqual(res.status_code , status.HTTP_201_CREATED)
        recipes = Recipe.objects.filter(user = self.user)
        recipe = recipes[0]
        self.assertEqual(recipes.count() , 1) ;
        self.assertEqual(recipe.tags.count() , 2)
        # print(vars(recipe))
        for tag in payload['tags'] : 
            exists = recipe.tags.filter(name = tag['name'] , user =self.user).exists()
            self.assertTrue(exists)

    def test_create_tag_on_update(self) : 

        recipe = create_recipe(self.user) 
        url = get_recipe_detail_url(recipe.id)
        payload =  {
            'tags' : [
                {'name' : 'amazing'}
            ]
        }
        res = self.client.patch(url  , payload , format = "json")
        self.assertEqual(res.status_code , status.HTTP_200_OK)
        tag = Tag.objects.get(user = self.user , name = 'amazing')
        self.assertIn(tag , recipe.tags.all())

    def test_recipe_reassign_tag(self) : 

        """ Test to check whether recipes tags are updated  """

        tag1 = Tag.objects.create(user =  self.user , name = 'dinner')
        recipe = create_recipe(self.user)
        url = get_recipe_detail_url(recipe.id)
        recipe.tags.add(tag1)

        payload = {
            'tags' :[
                {'name' : 'lunch'}
            ]
        }

        res = self.client.patch(url ,payload ,format = "json")
        self.assertEqual(res.status_code , status.HTTP_200_OK)
        tag2 = Tag.objects.get(user = self.user , name = 'lunch')
        self.assertIn(tag2 , recipe.tags.all())
        self.assertNotIn(tag1 ,recipe.tags.all())


    def create_recipe_with_ingredients(self) : 

        """ Create new ingredients while creating recipe """

        payload = { 
            "title" : "sample" ,
            "description" : "This is sample recipe" ,
            "time_minutes" : 15 ,
            "price" : 200 ,
            "link" : "http://example.com/recipe.pdf" ,
            "tags" : [{"name" : "good" } ,{ "name" : "average" }] ,
            "ingredients" : [{"name" : "abc"} , {"name" : "xyz"}]            
        }

        res = self.client.post(RECIPE_URL , payload , format = "json")
        self.assertEqual(res.status_code , status.HTTP_201_CREATED)
        recipe = Recipe.objects.filter(user = self.user)[0]
        self.assertEqual(recipe.ingredients.count() , 2)
        for ingredient in payload['ingredients'] : 
            exists = Ingredient.objects.filter(user = self.user , name = ingredient['name']).exists()
            self.assertTrue(exists)


    def test_create_ingredient_on_update(self) : 

        recipe = create_recipe(self.user)
        payload = {
            'ingredients' : [
                {'name' : 'abc'} ,
                {'name' : 'xyz'}
            ]
        }
        url = get_recipe_detail_url(recipe.id)
        res = self.client.patch(url ,payload ,format = "json")
        self.assertEqual(res.status_code ,status.HTTP_200_OK)
        for ingredient in payload['ingredients'] : 
            exists = Ingredient.objects.filter(user = self.user , name = ingredient['name']).exists()
            self.assertTrue(exists)

    def test_reassign_ingreidient_on_update(self) : 

        recipe = create_recipe(self.user)
        ingredient = Ingredient.objects.create(user = self.user , name = 'abc')
        recipe.ingredients.add(ingredient)

        payload = {
            'ingredients' : [
                {'name' : 'xyz'}
            ]
        }
        url = get_recipe_detail_url(recipe.id)
        res = self.client.patch(url , payload , format = "json")
        self.assertEqual(res.status_code ,status.HTTP_200_OK)
        recipe.refresh_from_db()
        ingredient2 = Ingredient.objects.get(user = self.user , name = 'xyz')
        self.assertIn(ingredient2 ,recipe.ingredients.all())
        self.assertNotIn(ingredient ,recipe.ingredients.all())


        
        
        
        



        

        





