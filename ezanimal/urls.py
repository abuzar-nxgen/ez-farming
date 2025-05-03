from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnimalTypeViewSet, BreedViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'animal-types', AnimalTypeViewSet, basename='animal-type')
router.register(r'breeds', BreedViewSet, basename='breed')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]
