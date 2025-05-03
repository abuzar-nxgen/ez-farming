from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ezcore.health_and_feed.views import (
    AnimalHealthViewSet, VaccinationViewSet, FeedTypeViewSet,
    FeedingScheduleViewSet, FeedingScheduleItemViewSet, FeedingRecordViewSet
)
from ezcore.inventory_and_sales.views import (
    InventoryItemViewSet, InventoryTransactionViewSet,
    SaleViewSet, SaleItemViewSet, ExpenseViewSet
)

# Create a router and register our health and feeding viewsets
health_feeding_router = DefaultRouter()
health_feeding_router.register(r'health-records', AnimalHealthViewSet, basename='animal-health')
health_feeding_router.register(r'vaccinations', VaccinationViewSet, basename='vaccination')
health_feeding_router.register(r'feed-types', FeedTypeViewSet, basename='feed-type')
health_feeding_router.register(r'feeding-schedules', FeedingScheduleViewSet, basename='feeding-schedule')
health_feeding_router.register(r'feeding-schedule-items', FeedingScheduleItemViewSet, basename='feeding-schedule-item')
health_feeding_router.register(r'feeding-records', FeedingRecordViewSet, basename='feeding-record')

# Create a router and register our inventory and sales viewsets
inventory_sales_router = DefaultRouter()
inventory_sales_router.register(r'inventory-items', InventoryItemViewSet, basename='inventory-item')
inventory_sales_router.register(r'inventory-transactions', InventoryTransactionViewSet, basename='inventory-transaction')
inventory_sales_router.register(r'sales', SaleViewSet, basename='sale')
inventory_sales_router.register(r'sale-items', SaleItemViewSet, basename='sale-item')
inventory_sales_router.register(r'expenses', ExpenseViewSet, basename='expense')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('health-feeding/', include(health_feeding_router.urls)),
    path('inventory-sales/', include(inventory_sales_router.urls)),
]
