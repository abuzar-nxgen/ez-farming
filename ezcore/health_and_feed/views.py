from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from ezcore.health_and_feed.models import (
    AnimalHealth, Vaccination, FeedType, 
    FeedingSchedule, FeedingScheduleItem, FeedingRecord
)
from .serializers import (
    AnimalHealthSerializer, VaccinationSerializer, FeedTypeSerializer,
    FeedingScheduleSerializer, FeedingScheduleItemSerializer, FeedingRecordSerializer
)
from ezcore.permissions import IsOwnerOrEmployee, HasFarmAccess
from django.http import HttpResponse



class AnimalHealthViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing animal health records."""
    serializer_class = AnimalHealthSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['dairy_animal', 'meat_animal', 'record_date', 'record_type']
    search_fields = ['diagnosis', 'symptoms', 'treatment', 'medication', 'vet_name']
    ordering_fields = ['record_date', 'dairy_animal__tag_number', 'meat_animal__tag_number']
    
    def get_queryset(self):
        """
        This view should return a list of all health records
        for the currently authenticated user's animals.
        """
        user = self.request.user
        if user.is_staff:
            return AnimalHealth.objects.all()
        elif user.is_farm_owner:
            return AnimalHealth.objects.filter(
                dairy_animal__owner=user
            ) | AnimalHealth.objects.filter(
                meat_animal__owner=user
            )
        elif user.employer and user.can_manage_health:
            # Employees can see their employer's records if they have permission
            return AnimalHealth.objects.filter(
                dairy_animal__owner=user.employer
            ) | AnimalHealth.objects.filter(
                meat_animal__owner=user.employer
            )
        return AnimalHealth.objects.none()
    
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


class VaccinationViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing vaccination records."""
    serializer_class = VaccinationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['dairy_animal', 'meat_animal', 'vaccination_date', 'vaccine_type']
    search_fields = ['vaccine_name', 'disease', 'manufacturer', 'batch_number']
    ordering_fields = ['vaccination_date', 'dairy_animal__tag_number', 'meat_animal__tag_number']
    
    def get_queryset(self):
        """
        This view should return a list of all vaccination records
        for the currently authenticated user's animals.
        """
        user = self.request.user
        if user.is_staff:
            return Vaccination.objects.all()
        elif user.is_farm_owner:
            return Vaccination.objects.filter(
                dairy_animal__owner=user
            ) | Vaccination.objects.filter(
                meat_animal__owner=user
            )
        elif user.employer and user.can_manage_health:
            # Employees can see their employer's records if they have permission
            return Vaccination.objects.filter(
                dairy_animal__owner=user.employer
            ) | Vaccination.objects.filter(
                meat_animal__owner=user.employer
            )
        return Vaccination.objects.none()
    
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


class FeedTypeViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing feed types."""
    queryset = FeedType.objects.all()
    serializer_class = FeedTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['feed_category', 'suitable_for_dairy', 'suitable_for_meat', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'feed_category']
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser | (HasFarmAccess & permissions.IsAuthenticated)]
        return [permission() for permission in permission_classes]


class FeedingScheduleViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing feeding schedules."""
    serializer_class = FeedingScheduleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['animal_type', 'breed', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'start_date', 'end_date']
    
    def get_queryset(self):
        """
        This view should return a list of all feeding schedules
        for the currently authenticated user.
        """
        user = self.request.user
        if user.is_staff:
            return FeedingSchedule.objects.all()
        elif user.is_farm_owner:
            return FeedingSchedule.objects.filter(created_by=user)
        elif user.employer and user.can_manage_feeding:
            # Employees can see their employer's schedules if they have permission
            return FeedingSchedule.objects.filter(created_by=user.employer)
        return FeedingSchedule.objects.none()
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [permissions.IsAuthenticated, HasFarmAccess]
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes.append(IsOwnerOrEmployee)
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        # Farm owners create schedules for themselves
        if self.request.user.is_farm_owner:
            serializer.save(created_by=self.request.user)
        # Employees create schedules for their employer
        elif self.request.user.employer and self.request.user.can_manage_feeding:
            serializer.save(created_by=self.request.user.employer)


class FeedingScheduleItemViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing feeding schedule items."""
    serializer_class = FeedingScheduleItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['schedule', 'feed_type', 'frequency']
    search_fields = ['feed_type__name', 'custom_frequency']
    ordering_fields = ['schedule__name', 'feed_type__name']
    
    def get_queryset(self):
        """
        This view should return a list of all feeding schedule items
        for the currently authenticated user's schedules.
        """
        user = self.request.user
        if user.is_staff:
            return FeedingScheduleItem.objects.all()
        elif user.is_farm_owner:
            return FeedingScheduleItem.objects.filter(schedule__created_by=user)
        elif user.employer and user.can_manage_feeding:
            # Employees can see their employer's schedule items if they have permission
            return FeedingScheduleItem.objects.filter(schedule__created_by=user.employer)
        return FeedingScheduleItem.objects.none()
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [permissions.IsAuthenticated, HasFarmAccess]
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes.append(IsOwnerOrEmployee)
        return [permission() for permission in permission_classes]


class FeedingRecordViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing feeding records."""
    serializer_class = FeedingRecordSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['dairy_animal', 'meat_animal', 'date', 'feed_type', 'time_of_day']
    search_fields = ['dairy_animal__tag_number', 'meat_animal__tag_number', 'feed_type__name']
    ordering_fields = ['date', 'time_of_day', 'dairy_animal__tag_number', 'meat_animal__tag_number']
    
    def get_queryset(self):
        """
        This view should return a list of all feeding records
        for the currently authenticated user's animals.
        """
        user = self.request.user
        if user.is_staff:
            return FeedingRecord.objects.all()
        elif user.is_farm_owner:
            return FeedingRecord.objects.filter(
                dairy_animal__owner=user
            ) | FeedingRecord.objects.filter(
                meat_animal__owner=user
            )
        elif user.employer and user.can_manage_feeding:
            # Employees can see their employer's records if they have permission
            return FeedingRecord.objects.filter(
                dairy_animal__owner=user.employer
            ) | FeedingRecord.objects.filter(
                meat_animal__owner=user.employer
            )
        return FeedingRecord.objects.none()
    
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


def haf_view(request):
    return HttpResponse("Welcome to the EZ Farming App's Health and Feed View!")