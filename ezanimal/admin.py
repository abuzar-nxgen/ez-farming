from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import AnimalType, Breed


@admin.register(AnimalType)
class AnimalTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'farming_type', 'is_active')
    list_filter = ('farming_type', 'is_active')
    search_fields = ('name', 'description')
    fieldsets = (
        (None, {
            'fields': ('name', 'farming_type', 'description', 'is_active')
        }),
    )


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ('name', 'animal_type', 'is_active')
    list_filter = ('animal_type', 'is_active')
    search_fields = ('name', 'description')
    fieldsets = (
        (None, {
            'fields': ('name', 'animal_type', 'description', 'is_active')
        }),
        (_('Characteristics'), {
            'fields': ('average_weight', 'average_lifespan', 'origin', 'characteristics')
        }),
    )
