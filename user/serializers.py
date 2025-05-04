from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""
    password = serializers.CharField(write_only=True, required=False)
    employer_email = serializers.ReadOnlyField(source='employer.email', allow_null=True)
    role_display = serializers.ReadOnlyField(source='get_role_display')
    employees_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'password', 'first_name', 'last_name', 
            'farm_name', 'farm_location', 'farm_size', 'preferred_language',
            'is_farm_owner', 'role', 'role_display', 'employer', 'employer_email',
            'hire_date', 'job_title', 'contact_number', 'employees_count',
            'can_manage_animals', 'can_manage_health', 'can_manage_feeding',
            'can_manage_inventory', 'can_manage_sales', 'can_manage_employees',
            'can_view_reports', 'is_active', 'date_joined'
        ]
        read_only_fields = ['id', 'is_active', 'date_joined']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def get_employees_count(self, obj):
        """Get the count of employees for this user."""
        return obj.employees.count() if hasattr(obj, 'employees') else 0
    
    def create(self, validated_data):
        """Create a new user with encrypted password."""
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
    
    def update(self, instance, validated_data):
        """Update user, setting password correctly if present."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class EmployeeSerializer(UserSerializer):
    """Serializer for employees (used when farm owners manage their employees)."""
    
    class Meta(UserSerializer.Meta):
        # Exclude farm-specific fields for employees
        exclude = ['farm_name', 'farm_location', 'farm_size', 'is_farm_owner']
    
    def validate(self, data):
        """Validate that employees have an employer."""
        if not data.get('employer') and not self.instance:
            raise serializers.ValidationError(_("Employees must have an employer."))
        
        # Ensure employees are not farm owners
        if data.get('is_farm_owner'):
            raise serializers.ValidationError(_("Employees cannot be farm owners."))
        
        return data


class EmployerSerializer(UserSerializer):
    """Serializer for employers with their employees."""
    employees = EmployeeSerializer(many=True, read_only=True)
    
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['employees']
    
    def validate(self, data):
        """Validate that employers don't have an employer themselves."""
        if data.get('employer'):
            raise serializers.ValidationError(_("Farm owners cannot have employers."))
        
        return data
