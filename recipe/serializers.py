from core.models import (
    Recipe ,
    Tag ,
    Ingredient ,
)
from rest_framework import serializers

class TagSerializer(serializers.ModelSerializer) :

    class Meta : 
        model = Tag 
        fields = ['id' , 'name']
        read_only_fields = ['id']

class IngredientSerializer(serializers.ModelSerializer) : 

    class Meta : 
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']

class RecipeSerializer(serializers.ModelSerializer) : 
    
    """ Serializer for Recipe model """

    tags = TagSerializer(many = True , required = False ) 
    ingredients = IngredientSerializer(many = True , required = False)
    class Meta : 
        model  = Recipe
        fields = ['id' , 'title'  , 'time_minutes' , 'price' , 'link' , 'tags' , 'ingredients']
        read_only_fields = ['id']

    def create(self, validated_data):

        """ Adding custom logic to create tags while creating recipe  """

        # print(validated_data)
        tags = validated_data.pop('tags' , []) 
        ingredients = validated_data.pop('ingredients' , [])
        # print(tags)
        recipe = Recipe.objects.create(**validated_data)
        
        self._get_or_create_tags(tags  ,recipe)
        self._get_or_create_ingredients(ingredients  ,recipe)

        return recipe
    
    def _get_or_create_tags(self, tags , recipe) : 

        user = self.context['request'].user
        for tag in tags : 
            tag_obj , created = Tag.objects.get_or_create(user = user  , **tag)
            recipe.tags.add(tag_obj)

    def _get_or_create_ingredients(self, ingredients , recipe) : 

        user = self.context['request'].user
        for ingredient in ingredients : 
            ingredient_obj , created = Ingredient.objects.get_or_create(user = user  , **ingredient)
            recipe.ingredients.add(ingredient_obj)
    



class RecipeDetailSerializer(RecipeSerializer) : 

    class Meta(RecipeSerializer.Meta) : 
        fields = RecipeSerializer.Meta.fields + ['description']

 
        

    def update(self, instance, validated_data):

        """ Custom update in order to update recipe tags provided """

        tags = validated_data.pop('tags' ,[])
        ingredients = validated_data.pop('ingredients' ,[])
        if tags is not None : 
            instance.tags.clear()
            self._get_or_create_tags(tags ,instance)

        if ingredients is not None : 
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredients , instance)
        
        for attr ,val in validated_data.items() : 
            setattr(instance, attr,val)

        instance.save()
        return instance
    

    
    
        
