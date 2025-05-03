from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DairyAnimalViewSet, MilkProductionViewSet, LactationViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'animals', DairyAnimalViewSet, basename='dairy-animal')
router.register(r'milk-production', MilkProductionViewSet, basename='milk-production')
router.register(r'lactations', LactationViewSet, basename='lactation')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]
