from core.models import Tag
from recipe.serializers import (
        TagSerializer ,
    )
from .test_recipe_api import create_user
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model


TAGS_URL = reverse('recipe:tag-list')

def create_tag(user ,**extra_fields) : 
    payload = {
        'name' : 'sample tag'                                  
    }
    payload.update(extra_fields)

    tag = Tag.objects.create(user = user ,**payload)
    return tag

def get_tag_detail_url(tag_id) : 
    return reverse('recipe:tag-detail' , args=[tag_id])


class PublicApiTagsTest(TestCase) :
    """ Test unauthenticated API requests  """

    def setUp(self) : 
        self.client = APIClient()

    def test_auth_required(self) : 

        """ Test auth required for retreiving tags """

        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code ,status.HTTP_401_UNAUTHORIZED)

class PrivateTagsApiTest(TestCase) : 

    def setUp(self) : 
        self.client = APIClient() 
        user_data = {
            'email' : 'test@example.com' ,
            'password' : '12345'
        }

        user = create_user(**user_data)
        self.user = user
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self) : 

        create_tag(self.user)
        create_tag(self.user , name = 'new tag')

        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code , status.HTTP_200_OK)
        self.assertEqual(len(res.data) , 2)

    def test_user_specific_tags(self) : 

        user2 = create_user(email = "test2@example.com" , password = "980fd")
        create_tag(user2)
        tag = create_tag(self.user , name = "my tag")
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code , status.HTTP_200_OK)
        self.assertEqual(len(res.data) , 1)
        self.assertEqual(res.data[0]['name'] , tag.name)

    def test_tag_partial_update(self) : 

        tag = create_tag(self.user)
        url = get_tag_detail_url(tag.id)
        payload =  {
            'name' : 'This is new custom name'
        }
        res = self.client.patch(url , payload)
        self.assertEqual(res.status_code , status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(res.data['name'] , tag.name)

    def test_delete_tag(self) : 
        tag = create_tag(self.user)
        url = get_tag_detail_url(tag.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code ,status.HTTP_204_NO_CONTENT)
        tag = Tag.objects.filter(user = self.user)
        self.assertFalse(tag.exists())

  


