from rest_framework import serializers
from ezdairy.models import DairyAnimal, MilkProduction, Lactation
from ezanimal.serializers import AnimalTypeSerializer, BreedSerializer
from django.utils.translation import gettext_lazy as _


class DairyAnimalSerializer(serializers.ModelSerializer):
    """Serializer for the DairyAnimal model."""
    animal_type_name = serializers.ReadOnlyField(source='animal_type.name')
    breed_name = serializers.ReadOnlyField(source='breed.name')
    status_display = serializers.ReadOnlyField(source='get_status_display')
    gender_display = serializers.ReadOnlyField(source='get_gender_display')
    owner_name = serializers.ReadOnlyField(source='owner.get_full_name')
    
    class Meta:
        model = DairyAnimal
        fields = [
            'id', 'tag_number', 'name', 'animal_type', 'animal_type_name', 
            'breed', 'breed_name', 'date_of_birth', 'gender', 'gender_display',
            'mother', 'father_tag', 'acquisition_date', 'acquisition_price',
            'status', 'status_display', 'notes', 'is_active', 'owner', 'owner_name',
            'created_at', 'updated_at', 'breed_avg_milk_production'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def to_representation(self, instance):
        """Add additional calculated fields to the serialized representation."""
        representation = super().to_representation(instance)
        
        # Add latest milk production data if available
        latest_milk = instance.milk_records.order_by('-date').first()
        if latest_milk:
            representation['latest_milk_date'] = latest_milk.date
            representation['latest_milk_amount'] = latest_milk.total_amount
            representation['expected_milk_amount'] = latest_milk.expected_amount
            
            # Add variance if expected amount is available
            if latest_milk.expected_amount:
                representation['milk_variance_percent'] = latest_milk.production_variance
        
        # Add current lactation data if available
        current_lactation = instance.lactations.filter(end_date__isnull=True).first()
        if current_lactation:
            representation['current_lactation_number'] = current_lactation.lactation_number
            representation['lactation_start_date'] = current_lactation.start_date
            representation['days_in_lactation'] = (latest_milk.date - current_lactation.start_date).days if latest_milk else None
        
        return representation


class MilkProductionSerializer(serializers.ModelSerializer):
    """Serializer for the MilkProduction model."""
    animal_tag = serializers.ReadOnlyField(source='animal.tag_number')
    animal_name = serializers.ReadOnlyField(source='animal.name')
    time_of_day_display = serializers.ReadOnlyField(source='get_time_of_day_display')
    recorded_by_name = serializers.ReadOnlyField(source='recorded_by.get_full_name')
    production_variance_percent = serializers.SerializerMethodField()
    
    class Meta:
        model = MilkProduction
        fields = [
            'id', 'animal', 'animal_tag', 'animal_name', 'date', 'time_of_day',
            'time_of_day_display', 'morning_amount', 'evening_amount', 'total_amount',
            'fat_content', 'protein_content', 'notes', 'recorded_by', 'recorded_by_name',
            'created_at', 'updated_at', 'expected_amount', 'expected_next_week',
            'expected_next_month', 'production_variance_percent'
        ]
        read_only_fields = ['id', 'total_amount', 'created_at', 'updated_at']
    
    def get_production_variance_percent(self, obj):
        """Get the variance between actual and expected production as a percentage."""
        return obj.production_variance
    
    def validate(self, data):
        """Validate that morning and evening amounts are non-negative."""
        if 'morning_amount' in data and data['morning_amount'] < 0:
            raise serializers.ValidationError(_("Morning amount cannot be negative."))
        if 'evening_amount' in data and data['evening_amount'] < 0:
            raise serializers.ValidationError(_("Evening amount cannot be negative."))
        return data


class LactationSerializer(serializers.ModelSerializer):
    """Serializer for the Lactation model."""
    animal_tag = serializers.ReadOnlyField(source='animal.tag_number')
    animal_name = serializers.ReadOnlyField(source='animal.name')
    duration_days = serializers.SerializerMethodField()
    production_variance_percent = serializers.SerializerMethodField()
    
    class Meta:
        model = Lactation
        fields = [
            'id', 'animal', 'animal_tag', 'animal_name', 'lactation_number',
            'start_date', 'end_date', 'total_production', 'peak_production',
            'peak_date', 'notes', 'created_at', 'updated_at', 'duration_days',
            'expected_total_production', 'expected_peak_production', 
            'expected_duration_days', 'production_variance_percent'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_duration_days(self, obj):
        """Get the duration of the lactation in days."""
        return obj.duration_days
    
    def get_production_variance_percent(self, obj):
        """Get the variance between actual and expected total production as a percentage."""
        return obj.production_variance
