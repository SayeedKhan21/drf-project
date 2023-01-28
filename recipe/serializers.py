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

    tags = TagSerializer(many = True , required = False ) 
    class Meta : 
        model  = Recipe
        fields = ['id' , 'title'  , 'time_minutes' , 'price' , 'link' , 'tags']
        read_only_fields = ['id']

    def create(self, validated_data):

        """ Adding custom logic to create tags while creating recipe  """

        # print(validated_data)
        tags = validated_data.pop('tags' , []) 
        # print(tags)
        recipe = Recipe.objects.create(**validated_data)
        user = self.context['request'].user
        for tag in tags : 
            tag_obj ,created = Tag.objects.get_or_create(name = tag['name'] ,user = user)   
            recipe.tags.add(tag_obj)
        return recipe
    
    
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class RecipeDetailSerializer(RecipeSerializer) : 

    class Meta(RecipeSerializer.Meta) : 
        fields = RecipeSerializer.Meta.fields + ['description']

    def _get_or_create_tags(self, tags , recipe) : 

        user = self.context['request'].user
        for tag in tags : 
            tag_obj , created = Tag.objects.get_or_create(user = user  , **tag)
            recipe.tags.add(tag_obj)
        

    def update(self, instance, validated_data):

        """ Custom update in order to update recipe tags provided """

        tags = validated_data.pop('tags' ,[])
        if tags is not None : 
            instance.tags.clear()
            self._get_or_create_tags(tags ,instance)
        
        for attr ,val in validated_data.items() : 
            setattr(instance, attr,val)

        instance.save()
        return instance
    

    
    
        
