from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    """Custom admin for User model."""
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_farm_owner', 'is_staff')
    list_filter = ('role', 'is_farm_owner', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'preferred_language')}),
        (_('Farm info'), {'fields': ('farm_name', 'farm_location', 'farm_size', 'is_farm_owner')}),
        (_('Role and permissions'), {
            'fields': ('role', 'employer', 'hire_date', 'job_title', 'contact_number',
                      'can_manage_animals', 'can_manage_health', 'can_manage_feeding',
                      'can_manage_inventory', 'can_manage_sales', 'can_manage_employees',
                      'can_view_reports'),
        }),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'role'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name', 'farm_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')


admin.site.register(User, UserAdmin)