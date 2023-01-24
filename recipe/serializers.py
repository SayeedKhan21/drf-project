from core.models import (
    Recipe ,
    Tag ,
)
from rest_framework import serializers

class TagSerializer(serializers.ModelSerializer) :

    class Meta : 
        model = Tag 
        fields = ['id' , 'name']
        read_only_fields = ['id']

class RecipeSerializer(serializers.ModelSerializer) : 
    
    """ Serializer for Recipe model """

    tags = TagSerializer(many = True)
    class Meta : 
        model  = Recipe
        fields = ['id' , 'title'  , 'time_minutes' , 'price' , 'link']
        read_only_fields = ['id']
   


class RecipeDetailSerializer(RecipeSerializer) : 

    

    class Meta(RecipeSerializer.Meta) : 
        fields = RecipeSerializer.Meta.fields + ['description']

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title' , instance.title)
        instance.time_minutes = validated_data.get('time_minutes' , instance.time_minutes)
        instance.time_minutes = validated_data.get('time_minutes' , instance.time_minutes)
        instance.description = validated_data.get('description' , instance.description)

        return instance
    

    
    
        
