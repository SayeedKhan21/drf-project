from core.models import (User)
from rest_framework import serializers
from django.contrib.auth import(
 get_user_model ,
 authenticate
)

class UserSerializer(serializers.ModelSerializer) : 
    """ Serializer for the user model """
    class Meta : 
        model = get_user_model()
        fields = ['email' , 'password' , 'name']
        extra_kwargs = {'password' : {'write_only' : True , 'min_length' : 5}}

    def create(self ,validated_data) :  
        """ Create and return a user """
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email' , instance.email)
        instance.name = validated_data.get('name' , instance.name)
        instance.password = validated_data.get('passoword' , instance.password)

        return instance


class AuthTokenSerializer(serializers.Serializer) : 
    email = serializers.EmailField()
    password = serializers.CharField(
        min_length = 5 ,
        style = {
            'input_type' : 'password'
        } ,
    )

    def validate(self, attrs):
        
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        user = authenticate(
            request=request ,
            username = email ,
            password = password
        )
        # print(user)

        if user is None : 
            raise serializers.ValidationError('Invalid credentials provided' ,code = 'authorization')

        attrs['user'] = user
        return attrs

        

    