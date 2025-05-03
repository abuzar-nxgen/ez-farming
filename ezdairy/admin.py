from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import DairyAnimal, MilkProduction, Lactation


@admin.register(DairyAnimal)
class DairyAnimalAdmin(admin.ModelAdmin):
    list_display = ('tag_number', 'name', 'animal_type', 'breed', 'gender', 'status', 'is_active', 'owner')
    list_filter = ('animal_type', 'breed', 'gender', 'status', 'is_active')
    search_fields = ('tag_number', 'name', 'notes')
    date_hierarchy = 'acquisition_date'
    fieldsets = (
        (None, {
            'fields': ('tag_number', 'name', 'animal_type', 'breed', 'is_active', 'owner')
        }),
        (_('Animal Details'), {
            'fields': ('gender', 'date_of_birth', 'mother', 'father_tag', 'status', 'notes')
        }),
        (_('Acquisition Info'), {
            'fields': ('acquisition_date', 'acquisition_price')
        }),
        (_('Production Metrics'), {
            'fields': ('breed_avg_milk_production',)
        }),
    )
    raw_id_fields = ('mother', 'owner')


@admin.register(MilkProduction)
class MilkProductionAdmin(admin.ModelAdmin):
    list_display = ('animal', 'date', 'time_of_day', 'morning_amount', 'evening_amount', 'total_amount', 'recorded_by')
    list_filter = ('date', 'time_of_day')
    search_fields = ('animal__tag_number', 'animal__name', 'notes')
    date_hierarchy = 'date'
    fieldsets = (
        (None, {
            'fields': ('animal', 'date', 'time_of_day', 'recorded_by')
        }),
        (_('Production Amounts'), {
            'fields': ('morning_amount', 'evening_amount', 'total_amount')
        }),
        (_('Quality Metrics'), {
            'fields': ('fat_content', 'protein_content')
        }),
        (_('Expected Production'), {
            'fields': ('expected_amount', 'expected_next_week', 'expected_next_month')
        }),
        (_('Additional Info'), {
            'fields': ('notes',)
        }),
    )
    readonly_fields = ('total_amount',)
    raw_id_fields = ('animal', 'recorded_by')


@admin.register(Lactation)
class LactationAdmin(admin.ModelAdmin):
    list_display = ('animal', 'lactation_number', 'start_date', 'end_date', 'total_production', 'peak_production')
    list_filter = ('start_date',)
    search_fields = ('animal__tag_number', 'animal__name', 'notes')
    date_hierarchy = 'start_date'
    fieldsets = (
        (None, {
            'fields': ('animal', 'lactation_number', 'start_date', 'end_date')
        }),
        (_('Production Metrics'), {
            'fields': ('total_production', 'peak_production', 'peak_date')
        }),
        (_('Expected Metrics'), {
            'fields': ('expected_total_production', 'expected_peak_production', 'expected_duration_days')
        }),
        (_('Additional Info'), {
            'fields': ('notes',)
        }),
    )
    raw_id_fields = ('animal',)
