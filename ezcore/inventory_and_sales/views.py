from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from ezcore.inventory_and_sales.models import (
    InventoryItem, InventoryTransaction, Sale, SaleItem, Expense
)
from .serializers import (
    InventoryItemSerializer, InventoryTransactionSerializer,
    SaleSerializer, SaleItemSerializer, ExpenseSerializer
)
from ezcore.permissions import IsOwnerOrEmployee, HasFarmAccess
from django.http import HttpResponse



class InventoryItemViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing inventory items."""
    serializer_class = InventoryItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['item_type', 'is_active']
    search_fields = ['name', 'description', 'storage_location']
    ordering_fields = ['name', 'quantity', 'unit_price', 'expiry_date']
    
    def get_queryset(self):
        """
        This view should return a list of all inventory items
        for the currently authenticated user.
        """
        user = self.request.user
        if user.is_staff:
            return InventoryItem.objects.all()
        elif user.is_farm_owner:
            return InventoryItem.objects.filter(owner=user)
        elif user.employer and user.can_manage_inventory:
            # Employees can see their employer's inventory if they have permission
            return InventoryItem.objects.filter(owner=user.employer)
        return InventoryItem.objects.none()
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [permissions.IsAuthenticated, HasFarmAccess]
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes.append(IsOwnerOrEmployee)
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        # Farm owners create inventory for themselves
        if self.request.user.is_farm_owner:
            serializer.save(owner=self.request.user)
        # Employees create inventory for their employer
        elif self.request.user.employer and self.request.user.can_manage_inventory:
            serializer.save(owner=self.request.user.employer)


class InventoryTransactionViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing inventory transactions."""
    serializer_class = InventoryTransactionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['item', 'transaction_date', 'transaction_type']
    search_fields = ['item__name', 'reference', 'supplier', 'notes']
    ordering_fields = ['transaction_date', 'item__name', 'quantity']
    
    def get_queryset(self):
        """
        This view should return a list of all inventory transactions
        for the currently authenticated user's items.
        """
        user = self.request.user
        if user.is_staff:
            return InventoryTransaction.objects.all()
        elif user.is_farm_owner:
            return InventoryTransaction.objects.filter(item__owner=user)
        elif user.employer and user.can_manage_inventory:
            # Employees can see their employer's transactions if they have permission
            return InventoryTransaction.objects.filter(item__owner=user.employer)
        return InventoryTransaction.objects.none()
    
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


class SaleViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing sales."""
    serializer_class = SaleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['sale_date', 'sale_type', 'payment_status']
    search_fields = ['customer_name', 'customer_contact', 'invoice_number', 'notes']
    ordering_fields = ['sale_date', 'total_amount', 'payment_status']
    
    def get_queryset(self):
        """
        This view should return a list of all sales
        for the currently authenticated user.
        """
        user = self.request.user
        if user.is_staff:
            return Sale.objects.all()
        elif user.is_farm_owner:
            return Sale.objects.filter(owner=user)
        elif user.employer and user.can_manage_sales:
            # Employees can see their employer's sales if they have permission
            return Sale.objects.filter(owner=user.employer)
        return Sale.objects.none()
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [permissions.IsAuthenticated, HasFarmAccess]
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes.append(IsOwnerOrEmployee)
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        # Farm owners create sales for themselves
        if self.request.user.is_farm_owner:
            serializer.save(owner=self.request.user, recorded_by=self.request.user)
        # Employees create sales for their employer
        elif self.request.user.employer and self.request.user.can_manage_sales:
            serializer.save(owner=self.request.user.employer, recorded_by=self.request.user)


class SaleItemViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing sale items."""
    serializer_class = SaleItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['sale', 'item_type']
    search_fields = ['description']
    ordering_fields = ['sale__sale_date', 'quantity', 'unit_price']
    
    def get_queryset(self):
        """
        This view should return a list of all sale items
        for the currently authenticated user's sales.
        """
        user = self.request.user
        if user.is_staff:
            return SaleItem.objects.all()
        elif user.is_farm_owner:
            return SaleItem.objects.filter(sale__owner=user)
        elif user.employer and user.can_manage_sales:
            # Employees can see their employer's sale items if they have permission
            return SaleItem.objects.filter(sale__owner=user.employer)
        return SaleItem.objects.none()
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [permissions.IsAuthenticated, HasFarmAccess]
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes.append(IsOwnerOrEmployee)
        return [permission() for permission in permission_classes]


class ExpenseViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing expenses."""
    serializer_class = ExpenseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['expense_date', 'expense_type', 'payment_method']
    search_fields = ['vendor', 'receipt_number', 'description']
    ordering_fields = ['expense_date', 'amount', 'expense_type']
    
    def get_queryset(self):
        """
        This view should return a list of all expenses
        for the currently authenticated user.
        """
        user = self.request.user
        if user.is_staff:
            return Expense.objects.all()
        elif user.is_farm_owner:
            return Expense.objects.filter(owner=user)
        elif user.employer and user.can_manage_sales:
            # Employees can see their employer's expenses if they have permission
            return Expense.objects.filter(owner=user.employer)
        return Expense.objects.none()
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [permissions.IsAuthenticated, HasFarmAccess]
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes.append(IsOwnerOrEmployee)
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        # Farm owners create expenses for themselves
        if self.request.user.is_farm_owner:
            serializer.save(owner=self.request.user, recorded_by=self.request.user)
        # Employees create expenses for their employer
        elif self.request.user.employer and self.request.user.can_manage_sales:
            serializer.save(owner=self.request.user.employer, recorded_by=self.request.user)


def ias_view(request):
    return HttpResponse("Welcome to the EZ Farming App's Inventory and Sales View!")