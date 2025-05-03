from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import MeatAnimal, WeightRecord, SlaughterRecord


@admin.register(MeatAnimal)
class MeatAnimalAdmin(admin.ModelAdmin):
    list_display = ('tag_number', 'name', 'animal_type', 'breed', 'gender', 'status', 'current_weight', 'target_weight', 'is_active', 'owner')
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
        (_('Weight Information'), {
            'fields': ('acquisition_weight', 'current_weight', 'target_weight')
        }),
        (_('Acquisition Info'), {
            'fields': ('acquisition_date', 'acquisition_price')
        }),
        (_('Breed Metrics'), {
            'fields': ('breed_avg_daily_gain', 'breed_avg_finishing_weight', 'breed_avg_days_to_finish')
        }),
    )
    readonly_fields = ('current_weight',)
    raw_id_fields = ('mother', 'owner')


@admin.register(WeightRecord)
class WeightRecordAdmin(admin.ModelAdmin):
    list_display = ('animal', 'date', 'weight', 'expected_weight', 'weight_variance', 'recorded_by')
    list_filter = ('date',)
    search_fields = ('animal__tag_number', 'animal__name', 'notes')
    date_hierarchy = 'date'
    fieldsets = (
        (None, {
            'fields': ('animal', 'date', 'weight', 'recorded_by')
        }),
        (_('Expected Values'), {
            'fields': ('expected_weight', 'expected_next_week', 'expected_next_month', 'expected_daily_gain')
        }),
        (_('Additional Info'), {
            'fields': ('notes',)
        }),
    )
    raw_id_fields = ('animal', 'recorded_by')
    
    def weight_variance(self, obj):
        if obj.weight_variance is not None:
            return f"{obj.weight_variance:.2f}%"
        return "-"
    weight_variance.short_description = _('Weight Variance')


@admin.register(SlaughterRecord)
class SlaughterRecordAdmin(admin.ModelAdmin):
    list_display = ('animal', 'slaughter_date', 'live_weight', 'carcass_weight', 'dressing_percentage', 'quality_grade', 'recorded_by')
    list_filter = ('slaughter_date', 'quality_grade')
    search_fields = ('animal__tag_number', 'animal__name', 'processor', 'slaughter_location', 'notes')
    date_hierarchy = 'slaughter_date'
    fieldsets = (
        (None, {
            'fields': ('animal', 'slaughter_date', 'slaughter_location', 'processor', 'recorded_by')
        }),
        (_('Weight Information'), {
            'fields': ('live_weight', 'carcass_weight', 'dressing_percentage')
        }),
        (_('Expected Values'), {
            'fields': ('expected_live_weight', 'expected_carcass_weight', 'expected_dressing_percentage')
        }),
        (_('Quality Information'), {
            'fields': ('quality_grade', 'yield_grade')
        }),
        (_('Additional Info'), {
            'fields': ('notes',)
        }),
    )
    readonly_fields = ('dressing_percentage',)
    raw_id_fields = ('animal', 'recorded_by')
