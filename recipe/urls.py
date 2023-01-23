from rest_framework.routers import DefaultRouter
from .views import RecipeViewSet
from django.urls import path ,include

router = DefaultRouter()
router.register('recipes' , RecipeViewSet)

app_name = 'recipe'

urlpatterns = [
    path('' , include(router.urls))
]