from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from user.serializers import UserSerializer, EmployeeSerializer
from django.http import HttpResponse

User = get_user_model()


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner or admin
        return obj == request.user or request.user.is_staff


class CanManageEmployees(permissions.BasePermission):
    """
    Custom permission to only allow users with employee management permission.
    """
    def has_permission(self, request, view):
        return request.user.can_manage_employees


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing user information."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'is_farm_owner', 'role']
    search_fields = ['email', 'first_name', 'last_name', 'farm_name']
    ordering_fields = ['email', 'date_joined', 'last_name']
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """
        Return appropriate serializer class based on the action.
        """
        if self.action == 'employees':
            return EmployeeSerializer
        elif hasattr(self, 'action') and self.action == 'me':
            # For the 'me' endpoint, use the standard UserSerializer
            return UserSerializer
        return super().get_serializer_class()
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Return the currently authenticated user.
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get', 'post'])
    def employees(self, request):
        """
        List all employees for the current user or create a new employee.
        """
        if not request.user.can_manage_employees:
            return Response(
                {"detail": "You do not have permission to manage employees."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if request.method == 'GET':
            employees = User.objects.filter(employer=request.user)
            serializer = self.get_serializer(employees, many=True)
            return Response(serializer.data)
        
        elif request.method == 'POST':
            # Set the employer to the current user
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(employer=request.user, is_farm_owner=False)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get', 'put', 'patch', 'delete'])
    def employee(self, request, pk=None):
        """
        Retrieve, update or delete an employee.
        """
        if not request.user.can_manage_employees:
            return Response(
                {"detail": "You do not have permission to manage employees."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            employee = User.objects.get(pk=pk, employer=request.user)
        except User.DoesNotExist:
            return Response(
                {"detail": "Employee not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if request.method == 'GET':
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data)
        
        elif request.method in ['PUT', 'PATCH']:
            partial = request.method == 'PATCH'
            serializer = EmployeeSerializer(employee, data=request.data, partial=partial)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            employee.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

def user_view(request):
    """
    A simple view to return a message indicating that the user view is working.
    """
    return HttpResponse("User view is working!")