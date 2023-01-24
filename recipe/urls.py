from rest_framework.routers import DefaultRouter
from .views import (
    RecipeViewSet ,
    TagViewSet ,
    )
from django.urls import path ,include

router = DefaultRouter()
router.register('recipes' , RecipeViewSet)
router.register('tags' , TagViewSet)

app_name = 'recipe'

urlpatterns = [
    path('' , include(router.urls))
]