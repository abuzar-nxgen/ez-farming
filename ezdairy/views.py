from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from ezdairy.models import DairyAnimal, MilkProduction, Lactation
from .serializers import DairyAnimalSerializer, MilkProductionSerializer, LactationSerializer
from ezcore.permissions import IsOwnerOrEmployee, HasFarmAccess
from django.http import HttpResponse




class DairyAnimalViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing dairy animals."""
    serializer_class = DairyAnimalSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['animal_type', 'breed', 'status', 'is_active', 'gender']
    search_fields = ['tag_number', 'name']
    ordering_fields = ['tag_number', 'name', 'date_of_birth', 'acquisition_date']
    
    def get_queryset(self):
        """
        This view should return a list of all dairy animals
        for the currently authenticated user.
        """
        user = self.request.user
        if user.is_staff:
            return DairyAnimal.objects.all()
        elif user.is_farm_owner:
            return DairyAnimal.objects.filter(owner=user)
        elif user.employer:
            # Employees can see their employer's animals if they have permission
            if user.can_manage_animals:
                return DairyAnimal.objects.filter(owner=user.employer)
            return DairyAnimal.objects.none()
        return DairyAnimal.objects.none()
    
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


class MilkProductionViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing milk production records."""
    serializer_class = MilkProductionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['animal', 'date']
    search_fields = ['animal__tag_number', 'animal__name']
    ordering_fields = ['date', 'animal__tag_number', 'morning_amount', 'evening_amount', 'total_amount']
    
    def get_queryset(self):
        """
        This view should return a list of all milk production records
        for the currently authenticated user's animals.
        """
        user = self.request.user
        if user.is_staff:
            return MilkProduction.objects.all()
        elif user.is_farm_owner:
            return MilkProduction.objects.filter(animal__owner=user)
        elif user.employer:
            # Employees can see their employer's records if they have permission
            if user.can_manage_animals:
                return MilkProduction.objects.filter(animal__owner=user.employer)
            return MilkProduction.objects.none()
        return MilkProduction.objects.none()
    
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


class LactationViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing lactation records."""
    serializer_class = LactationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['animal', 'lactation_number']
    search_fields = ['animal__tag_number', 'animal__name']
    ordering_fields = ['animal__tag_number', 'lactation_number', 'start_date', 'end_date']
    
    def get_queryset(self):
        """
        This view should return a list of all lactation records
        for the currently authenticated user's animals.
        """
        user = self.request.user
        if user.is_staff:
            return Lactation.objects.all()
        elif user.is_farm_owner:
            return Lactation.objects.filter(animal__owner=user)
        elif user.employer:
            # Employees can see their employer's records if they have permission
            if user.can_manage_animals:
                return Lactation.objects.filter(animal__owner=user.employer)
            return Lactation.objects.none()
        return Lactation.objects.none()
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [permissions.IsAuthenticated, HasFarmAccess]
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes.append(IsOwnerOrEmployee)
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save()
        
    
def dairy_view(request):
    return HttpResponse("Welcome to the EZ Farming App's Dairy View!")
