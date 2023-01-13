"""
Test for models 
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import (
    Recipe ,
)
from decimal import Decimal


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
