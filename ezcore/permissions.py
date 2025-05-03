from rest_framework import permissions


class IsOwnerOrEmployee(permissions.BasePermission):
    """
    Custom permission to only allow owners or their employees to access objects.
    """
    def has_object_permission(self, request, view, obj):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return False
        
        # Admin can do anything
        if request.user.is_staff:
            return True
        
        # Check if object has an owner field
        if hasattr(obj, 'owner'):
            # Owner can do anything with their objects
            if obj.owner == request.user:
                return True
            
            # Employee can access if they work for the owner and have appropriate permissions
            if hasattr(request.user, 'employer') and request.user.employer == obj.owner:
                # For read operations, check specific permissions based on object type
                if request.method in permissions.SAFE_METHODS:
                    # Animal-related permissions
                    if hasattr(obj, 'animal_type') and not request.user.can_manage_animals:
                        return False
                    
                    # Health-related permissions
                    if view.__class__.__name__ in ['AnimalHealthViewSet', 'VaccinationViewSet'] and not request.user.can_manage_health:
                        return False
                    
                    # Feeding-related permissions
                    if view.__class__.__name__ in ['FeedingScheduleViewSet', 'FeedingRecordViewSet'] and not request.user.can_manage_feeding:
                        return False
                    
                    # Inventory-related permissions
                    if view.__class__.__name__ in ['InventoryItemViewSet', 'InventoryTransactionViewSet'] and not request.user.can_manage_inventory:
                        return False
                    
                    # Sales-related permissions
                    if view.__class__.__name__ in ['SaleViewSet', 'ExpenseViewSet'] and not request.user.can_manage_sales:
                        return False
                    
                    # Default to allow if no specific check failed
                    return True
                
                # For write operations, check specific permissions based on object type
                else:
                    # Animal-related permissions
                    if hasattr(obj, 'animal_type') and not request.user.can_manage_animals:
                        return False
                    
                    # Health-related permissions
                    if view.__class__.__name__ in ['AnimalHealthViewSet', 'VaccinationViewSet'] and not request.user.can_manage_health:
                        return False
                    
                    # Feeding-related permissions
                    if view.__class__.__name__ in ['FeedingScheduleViewSet', 'FeedingRecordViewSet'] and not request.user.can_manage_feeding:
                        return False
                    
                    # Inventory-related permissions
                    if view.__class__.__name__ in ['InventoryItemViewSet', 'InventoryTransactionViewSet'] and not request.user.can_manage_inventory:
                        return False
                    
                    # Sales-related permissions
                    if view.__class__.__name__ in ['SaleViewSet', 'ExpenseViewSet'] and not request.user.can_manage_sales:
                        return False
                    
                    # Default to deny for write operations if no specific check passed
                    return False
        
        # If we get here, deny access
        return False


class HasFarmAccess(permissions.BasePermission):
    """
    Custom permission to check if user has access to farm data.
    """
    def has_permission(self, request, view):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return False
        
        # Admin can do anything
        if request.user.is_staff:
            return True
        
        # Farm owners can do anything with their farm
        if request.user.is_farm_owner:
            return True
        
        # Employees need to check specific permissions based on view type
        if hasattr(request.user, 'employer') and request.user.employer is not None:
            # For read operations, check specific permissions based on view type
            if request.method in permissions.SAFE_METHODS:
                # Animal-related permissions
                if view.__class__.__name__ in ['AnimalTypeViewSet', 'BreedViewSet', 'DairyAnimalViewSet', 'MeatAnimalViewSet'] and not request.user.can_manage_animals:
                    return False
                
                # Health-related permissions
                if view.__class__.__name__ in ['AnimalHealthViewSet', 'VaccinationViewSet'] and not request.user.can_manage_health:
                    return False
                
                # Feeding-related permissions
                if view.__class__.__name__ in ['FeedTypeViewSet', 'FeedingScheduleViewSet', 'FeedingRecordViewSet'] and not request.user.can_manage_feeding:
                    return False
                
                # Inventory-related permissions
                if view.__class__.__name__ in ['InventoryItemViewSet', 'InventoryTransactionViewSet'] and not request.user.can_manage_inventory:
                    return False
                
                # Sales-related permissions
                if view.__class__.__name__ in ['SaleViewSet', 'ExpenseViewSet'] and not request.user.can_manage_sales:
                    return False
                
                # Default to allow if no specific check failed
                return True
            
            # For write operations, check specific permissions based on view type
            else:
                # Animal-related permissions
                if view.__class__.__name__ in ['AnimalTypeViewSet', 'BreedViewSet', 'DairyAnimalViewSet', 'MeatAnimalViewSet'] and not request.user.can_manage_animals:
                    return False
                
                # Health-related permissions
                if view.__class__.__name__ in ['AnimalHealthViewSet', 'VaccinationViewSet'] and not request.user.can_manage_health:
                    return False
                
                # Feeding-related permissions
                if view.__class__.__name__ in ['FeedTypeViewSet', 'FeedingScheduleViewSet', 'FeedingRecordViewSet'] and not request.user.can_manage_feeding:
                    return False
                
                # Inventory-related permissions
                if view.__class__.__name__ in ['InventoryItemViewSet', 'InventoryTransactionViewSet'] and not request.user.can_manage_inventory:
                    return False
                
                # Sales-related permissions
                if view.__class__.__name__ in ['SaleViewSet', 'ExpenseViewSet'] and not request.user.can_manage_sales:
                    return False
                
                # Default to deny for write operations if no specific check passed
                return False
        
        # If we get here, deny access
        return False
