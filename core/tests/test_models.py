"""
Test for models 
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import (
    Recipe ,
    Tag , 
    Ingredient ,
)
from decimal import Decimal


def create_user(email = "test@example.com" , password =  "12345") : 
    return get_user_model().objects.create(email = email , password = password)

class ModelTests(TestCase) : 

    """ Test Models """

    def test_create_user_with_email_successful(self) : 
        email = "test@example.com"
        password = "test123"

        user = get_user_model().objects.create_user(
            email = email ,
            password = password
        )

        self.assertEqual(user.email ,email)
        self.assertTrue(user.check_password(password))
        

    def test_new_user_with_normalized_email(self) : 
        sample_emails = [
            ['test1@EXAMPLE.COM' , 'test1@example.com'] ,
            ['test2@Example.com' , 'test2@example.com'] ,
            ['TEST3@example.COM' , 'TEST3@example.com'] ,
        ]

        for email , expected in sample_emails : 
            user = get_user_model().objects.create_user(email , 'sample')
            self.assertEqual(user.email ,expected)

    def test_create_superuser(self) : 
        user = get_user_model().objects.create_superuser('test@example.com' , '123')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_recipe_create_successfull(self) : 
        data = {
            'email' : 'user3@example.com' ,
            'password' : '12345' ,
            'name' : 'User 3'
        }
        user = get_user_model().objects.create_user(**data)
        recipe = Recipe.objects.create(
            user = user ,
            title = 'First Recipe' ,
            description = 'This is my first recipe' ,
            time_minutes = 20 ,
            price = Decimal('5.50')            
        )
        self.assertEqual(recipe.title , str(recipe))

    def test_create_tag(self) : 

        """ Check creation of tag """
        tag = Tag.objects.create(name = "sample" , user = create_user())
        self.assertEqual(tag.name , str(tag))

    def test_create_ingredient(self) : 

        """ Check creation of ingredient """

        ingredient = Ingredient.objects.create(name = "sample" , user = create_user() )
        self.assertEqual(str(ingredient) , "sample")



