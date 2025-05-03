from rest_framework import serializers
from ezanimal.models import AnimalType, Breed


class AnimalTypeSerializer(serializers.ModelSerializer):
    """Serializer for the AnimalType model."""
    
    class Meta:
        model = AnimalType
        fields = ['id', 'name', 'description', 'farming_type', 'is_active']


class BreedSerializer(serializers.ModelSerializer):
    """Serializer for the Breed model."""
    animal_type_name = serializers.ReadOnlyField(source='animal_type.name')
    
    class Meta:
        model = Breed
        fields = [
            'id', 'animal_type', 'animal_type_name', 'name', 'description',
            'average_weight', 'average_height', 'average_milk_production',
            'lactation_period', 'average_meat_yield', 'growth_rate',
            'gestation_period', 'maturity_age', 'is_active'
        ]
