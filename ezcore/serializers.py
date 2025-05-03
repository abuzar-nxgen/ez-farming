from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the custom User model."""
    
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'farm_name', 
                  'farm_location', 'farm_size', 'preferred_language', 'date_joined')
        read_only_fields = ('id', 'date_joined')


class UserRegistrationSerializer(serializers.Serializer):
    """Serializer for user registration."""
    
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    farm_name = serializers.CharField(required=False)
    farm_location = serializers.CharField(required=False)
    farm_size = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    preferred_language = serializers.ChoiceField(choices=[('en', 'English'), ('ur', 'Urdu')], default='en')
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    
    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(_("A user is already registered with this email address."))
        return email
    
    def validate_password1(self, password):
        return get_adapter().clean_password(password)
    
    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data
    
    def get_cleaned_data(self):
        return {
            'email': self.validated_data.get('email', ''),
            'password1': self.validated_data.get('password1', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'farm_name': self.validated_data.get('farm_name', ''),
            'farm_location': self.validated_data.get('farm_location', ''),
            'farm_size': self.validated_data.get('farm_size', None),
            'preferred_language': self.validated_data.get('preferred_language', 'en'),
        }
    
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        
        # Set user fields
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        user.farm_name = self.cleaned_data.get('farm_name', '')
        user.farm_location = self.cleaned_data.get('farm_location', '')
        user.farm_size = self.cleaned_data.get('farm_size', None)
        user.preferred_language = self.cleaned_data.get('preferred_language', 'en')
        
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        return user
