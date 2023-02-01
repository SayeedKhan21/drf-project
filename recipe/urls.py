from rest_framework.routers import DefaultRouter
from .views import (
    RecipeViewSet ,
    TagViewSet ,
    IngredientViewSet
    )
from django.urls import path ,include

router = DefaultRouter()
router.register('recipes' , RecipeViewSet)
router.register('tags' , TagViewSet)
router.register('ingredients' , IngredientViewSet)

app_name = 'recipe'

urlpatterns = [
    path('' , include(router.urls))
]