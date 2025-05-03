from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from ezcore.health_and_feed.models import (
    AnimalHealth, Vaccination, FeedType, 
    FeedingSchedule, FeedingScheduleItem, FeedingRecord
)
from ezcore.inventory_and_sales.models import (
    InventoryItem, InventoryTransaction, Sale, SaleItem, Expense
)


@admin.register(AnimalHealth)
class AnimalHealthAdmin(admin.ModelAdmin):
    list_display = ('get_animal_tag', 'record_date', 'record_type', 'diagnosis', 'get_recorded_by')
    list_filter = ('record_date', 'record_type')
    search_fields = ('dairy_animal__tag_number', 'meat_animal__tag_number', 'diagnosis', 'symptoms', 'treatment')
    date_hierarchy = 'record_date'
    
    def get_animal_tag(self, obj):
        return obj.dairy_animal.tag_number if obj.dairy_animal else obj.meat_animal.tag_number
    get_animal_tag.short_description = _('Animal Tag')
    
    def get_recorded_by(self, obj):
        return obj.recorded_by.get_full_name() if obj.recorded_by else '-'
    get_recorded_by.short_description = _('Recorded By')


@admin.register(Vaccination)
class VaccinationAdmin(admin.ModelAdmin):
    list_display = ('get_animal_tag', 'vaccination_date', 'vaccine_name', 'disease', 'get_recorded_by')
    list_filter = ('vaccination_date', 'vaccine_type')
    search_fields = ('dairy_animal__tag_number', 'meat_animal__tag_number', 'vaccine_name', 'disease')
    date_hierarchy = 'vaccination_date'
    
    def get_animal_tag(self, obj):
        return obj.dairy_animal.tag_number if obj.dairy_animal else obj.meat_animal.tag_number
    get_animal_tag.short_description = _('Animal Tag')
    
    def get_recorded_by(self, obj):
        return obj.recorded_by.get_full_name() if obj.recorded_by else '-'
    get_recorded_by.short_description = _('Recorded By')


@admin.register(FeedType)
class FeedTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'feed_category', 'suitable_for_dairy', 'suitable_for_meat', 'is_active')
    list_filter = ('feed_category', 'suitable_for_dairy', 'suitable_for_meat', 'is_active')
    search_fields = ('name', 'description')


@admin.register(FeedingSchedule)
class FeedingScheduleAdmin(admin.ModelAdmin):
    list_display = ('name', 'animal_type', 'breed', 'start_date', 'end_date', 'is_active')
    list_filter = ('animal_type', 'breed', 'is_active')
    search_fields = ('name', 'description')
    date_hierarchy = 'start_date'


@admin.register(FeedingScheduleItem)
class FeedingScheduleItemAdmin(admin.ModelAdmin):
    list_display = ('schedule', 'feed_type', 'amount', 'frequency', 'time_of_day')
    list_filter = ('frequency', 'time_of_day')
    search_fields = ('schedule__name', 'feed_type__name')


@admin.register(FeedingRecord)
class FeedingRecordAdmin(admin.ModelAdmin):
    list_display = ('get_animal_tag', 'date', 'feed_type', 'amount', 'time_of_day', 'get_recorded_by')
    list_filter = ('date', 'time_of_day')
    search_fields = ('dairy_animal__tag_number', 'meat_animal__tag_number', 'feed_type__name')
    date_hierarchy = 'date'
    
    def get_animal_tag(self, obj):
        return obj.dairy_animal.tag_number if obj.dairy_animal else obj.meat_animal.tag_number
    get_animal_tag.short_description = _('Animal Tag')
    
    def get_recorded_by(self, obj):
        return obj.recorded_by.get_full_name() if obj.recorded_by else '-'
    get_recorded_by.short_description = _('Recorded By')


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'item_type', 'quantity', 'unit', 'unit_price', 'storage_location', 'is_active')
    list_filter = ('item_type', 'is_active')
    search_fields = ('name', 'description', 'storage_location')
    fieldsets = (
        (None, {
            'fields': ('name', 'item_type', 'description', 'is_active', 'owner')
        }),
        (_('Inventory Details'), {
            'fields': ('quantity', 'unit', 'unit_price', 'storage_location', 'expiry_date')
        }),
        (_('Thresholds'), {
            'fields': ('reorder_level', 'reorder_quantity')
        }),
    )


@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ('item', 'transaction_date', 'transaction_type', 'quantity', 'unit_price', 'get_recorded_by')
    list_filter = ('transaction_date', 'transaction_type')
    search_fields = ('item__name', 'reference', 'supplier', 'notes')
    date_hierarchy = 'transaction_date'
    
    def get_recorded_by(self, obj):
        return obj.recorded_by.get_full_name() if obj.recorded_by else '-'
    get_recorded_by.short_description = _('Recorded By')


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'sale_date', 'customer_name', 'sale_type', 'total_amount', 'payment_status')
    list_filter = ('sale_date', 'sale_type', 'payment_status')
    search_fields = ('invoice_number', 'customer_name', 'customer_contact', 'notes')
    date_hierarchy = 'sale_date'


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('sale', 'item_type', 'description', 'quantity', 'unit_price', 'total_price')
    list_filter = ('item_type',)
    search_fields = ('sale__invoice_number', 'description')


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('expense_date', 'expense_type', 'vendor', 'amount', 'payment_method', 'get_recorded_by')
    list_filter = ('expense_date', 'expense_type', 'payment_method')
    search_fields = ('vendor', 'receipt_number', 'description')
    date_hierarchy = 'expense_date'
    
    def get_recorded_by(self, obj):
        return obj.recorded_by.get_full_name() if obj.recorded_by else '-'
    get_recorded_by.short_description = _('Recorded By')
