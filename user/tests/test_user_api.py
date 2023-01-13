from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

def create_user(**kwargs) : 
    """ Create and return user"""
    user = get_user_model().objects.create_user(**kwargs)
    return user

CREATE_USER_URL = reverse('user:create-user')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

class PublicUserApiTests(TestCase) : 

    def setUp(self) : 
        self.client = APIClient()
        

    def test_create_user_successful(self) : 
        payload = {
            'email' : 'test@example.com' , 
            'password' : '12556' ,
            'name' : 'test'
        }

        response = self.client.post(CREATE_USER_URL , payload)
        self.assertEqual(response.status_code , status.HTTP_201_CREATED )
        user = get_user_model().objects.get(email = payload['email'])
        self.assertTrue(user.check_password(payload['password']))

    def test_user_with_email_exists(self) : 
        payload = {
            'email' : 'test@example.com' , 
            'password' : '12345' ,
            'name' : 'test'
        }

        user = create_user(**payload)
        response = self.client.post(CREATE_USER_URL , payload)
        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST )
        self.assertTrue(user.check_password(payload['password']))

    def test_token_create_successfull(self) : 
        data = {
            'email' : 'test@example.com' ,
            'password' : 'goodpas' ,
            'name' : 'test' 
        }
        create_user(**data)

        payload = {'email' : data['email'] , 'password' : data['password']}
        res = self.client.post(TOKEN_URL ,  payload)
        self.assertEqual(res.status_code , status.HTTP_201_CREATED)
        self.assertIn('token' , res.data) 

    def test_token_create_failure(self) : 
        data = {
            'email' : 'test@example.com' ,
            'password' : 'goodpass' ,
            'name' : 'test' 
        }
        create_user(**data)

        payload = {'email' : data['email'] , 'password' : 'badpass' }
        res = self.client.post(TOKEN_URL ,  payload)
        self.assertEqual(res.status_code , status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token' , res.data) 


        
class PrivateApiTests(TestCase) : 

    def setUp(self) : 
        data = {
            'email' : 'test@example.com' ,
            'password' : 'test1' ,
            'name' : 'test'
        }
        user = create_user(**data)
        self.user = user
        self.client = APIClient()
        self.client.force_authenticate(user = self.user)

    def test_retrieve_profile_success(self) : 
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code ,status.HTTP_200_OK)
        self.assertEqual(res.data , {
            'name' : self.user.name ,
            'email' : self.user.email
        })
    
    def test_user_profile_update_successful(self) : 
        new_data =  {
            'name' : 'test2' ,
            'password' : 'goodpas' ,
        }

        res = self.client.patch(ME_URL , new_data)

        self.user.refresh_from_db()        
        self.assertEqual(res.status_code , status.HTTP_200_OK)
        self.assertEqual(self.user.name , new_data['name'])
        self.assertEqual(self.user.check_password(new_data['password']))
        






