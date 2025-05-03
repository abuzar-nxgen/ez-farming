from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from ezmeat.models import MeatAnimal, WeightRecord, SlaughterRecord
from .serializers import MeatAnimalSerializer, WeightRecordSerializer, SlaughterRecordSerializer
from ezcore.permissions import IsOwnerOrEmployee, HasFarmAccess
from django.http import HttpResponse



class MeatAnimalViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing meat animals."""
    serializer_class = MeatAnimalSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['animal_type', 'breed', 'status', 'is_active', 'gender']
    search_fields = ['tag_number', 'name']
    ordering_fields = ['tag_number', 'name', 'date_of_birth', 'acquisition_date', 'current_weight']
    
    def get_queryset(self):
        """
        This view should return a list of all meat animals
        for the currently authenticated user.
        """
        user = self.request.user
        if user.is_staff:
            return MeatAnimal.objects.all()
        elif user.is_farm_owner:
            return MeatAnimal.objects.filter(owner=user)
        elif user.employer:
            # Employees can see their employer's animals if they have permission
            if user.can_manage_animals:
                return MeatAnimal.objects.filter(owner=user.employer)
            return MeatAnimal.objects.none()
        return MeatAnimal.objects.none()
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [permissions.IsAuthenticated, HasFarmAccess]
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes.append(IsOwnerOrEmployee)
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        # Farm owners create animals for themselves
        if self.request.user.is_farm_owner:
            serializer.save(owner=self.request.user)
        # Employees create animals for their employer
        elif self.request.user.employer and self.request.user.can_manage_animals:
            serializer.save(owner=self.request.user.employer)


class WeightRecordViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing weight records."""
    serializer_class = WeightRecordSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['animal', 'date']
    search_fields = ['animal__tag_number', 'animal__name']
    ordering_fields = ['date', 'animal__tag_number', 'weight']
    
    def get_queryset(self):
        """
        This view should return a list of all weight records
        for the currently authenticated user's animals.
        """
        user = self.request.user
        if user.is_staff:
            return WeightRecord.objects.all()
        elif user.is_farm_owner:
            return WeightRecord.objects.filter(animal__owner=user)
        elif user.employer:
            # Employees can see their employer's records if they have permission
            if user.can_manage_animals:
                return WeightRecord.objects.filter(animal__owner=user.employer)
            return WeightRecord.objects.none()
        return WeightRecord.objects.none()
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [permissions.IsAuthenticated, HasFarmAccess]
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes.append(IsOwnerOrEmployee)
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(recorded_by=self.request.user)


class SlaughterRecordViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing slaughter records."""
    serializer_class = SlaughterRecordSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['animal', 'slaughter_date', 'quality_grade']
    search_fields = ['animal__tag_number', 'animal__name', 'slaughter_location', 'processor']
    ordering_fields = ['slaughter_date', 'animal__tag_number', 'live_weight', 'carcass_weight']
    
    def get_queryset(self):
        """
        This view should return a list of all slaughter records
        for the currently authenticated user's animals.
        """
        user = self.request.user
        if user.is_staff:
            return SlaughterRecord.objects.all()
        elif user.is_farm_owner:
            return SlaughterRecord.objects.filter(animal__owner=user)
        elif user.employer:
            # Employees can see their employer's records if they have permission
            if user.can_manage_animals:
                return SlaughterRecord.objects.filter(animal__owner=user.employer)
            return SlaughterRecord.objects.none()
        return SlaughterRecord.objects.none()
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [permissions.IsAuthenticated, HasFarmAccess]
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes.append(IsOwnerOrEmployee)
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(recorded_by=self.request.user)

def meat_view(request):
    return HttpResponse("Welcome to the EZ Farming App's Meat View!")