from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from ezanimal.models import AnimalType, Breed
from .serializers import AnimalTypeSerializer, BreedSerializer
from ezcore.permissions import HasFarmAccess
from django.http import HttpResponse



class AnimalTypeViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing animal types."""
    queryset = AnimalType.objects.all()
    serializer_class = AnimalTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['farming_type', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name']
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser | HasFarmAccess]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save()


class BreedViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing breeds."""
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['animal_type', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'animal_type__name']
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser | HasFarmAccess]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save()

def animal_view(request):
    return HttpResponse("Welcome to the EZ Farming App's Animal View!")