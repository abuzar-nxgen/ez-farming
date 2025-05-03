from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MeatAnimalViewSet, WeightRecordViewSet, SlaughterRecordViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'animals', MeatAnimalViewSet, basename='meat-animal')
router.register(r'weight-records', WeightRecordViewSet, basename='weight-record')
router.register(r'slaughter-records', SlaughterRecordViewSet, basename='slaughter-record')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]
