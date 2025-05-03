from rest_framework import serializers
from ezmeat.models import MeatAnimal, WeightRecord, SlaughterRecord
from ezanimal.serializers import AnimalTypeSerializer, BreedSerializer
from django.utils.translation import gettext_lazy as _


class MeatAnimalSerializer(serializers.ModelSerializer):
    """Serializer for the MeatAnimal model."""
    animal_type_name = serializers.ReadOnlyField(source='animal_type.name')
    breed_name = serializers.ReadOnlyField(source='breed.name')
    status_display = serializers.ReadOnlyField(source='get_status_display')
    gender_display = serializers.ReadOnlyField(source='get_gender_display')
    owner_name = serializers.ReadOnlyField(source='owner.get_full_name')
    age_in_days = serializers.SerializerMethodField()
    weight_gain_progress_percent = serializers.SerializerMethodField()
    
    class Meta:
        model = MeatAnimal
        fields = [
            'id', 'tag_number', 'name', 'animal_type', 'animal_type_name', 
            'breed', 'breed_name', 'date_of_birth', 'gender', 'gender_display',
            'mother', 'father_tag', 'acquisition_date', 'acquisition_price',
            'acquisition_weight', 'current_weight', 'target_weight',
            'status', 'status_display', 'notes', 'is_active', 'owner', 'owner_name',
            'created_at', 'updated_at', 'age_in_days', 'weight_gain_progress_percent',
            'breed_avg_daily_gain', 'breed_avg_finishing_weight', 'breed_avg_days_to_finish'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'current_weight']
    
    def get_age_in_days(self, obj):
        """Get the age of the animal in days."""
        return obj.age_in_days
    
    def get_weight_gain_progress_percent(self, obj):
        """Get the progress towards target weight as a percentage."""
        return obj.weight_gain_progress
    
    def to_representation(self, instance):
        """Add additional calculated fields to the serialized representation."""
        representation = super().to_representation(instance)
        
        # Add latest weight record data if available
        latest_weight = instance.weight_records.order_by('-date').first()
        if latest_weight:
            representation['latest_weight_date'] = latest_weight.date
            representation['latest_weight'] = latest_weight.weight
            representation['expected_weight'] = latest_weight.expected_weight
            
            # Add variance if expected weight is available
            if latest_weight.expected_weight:
                representation['weight_variance_percent'] = latest_weight.weight_variance
            
            # Add daily gain information if available
            if latest_weight.actual_daily_gain:
                representation['actual_daily_gain'] = latest_weight.actual_daily_gain
                representation['expected_daily_gain'] = latest_weight.expected_daily_gain
                
                if latest_weight.expected_daily_gain:
                    representation['daily_gain_variance_percent'] = latest_weight.daily_gain_variance
        
        # Calculate days to target weight based on current daily gain
        if instance.current_weight and instance.target_weight and latest_weight and latest_weight.actual_daily_gain and latest_weight.actual_daily_gain > 0:
            weight_to_gain = instance.target_weight - instance.current_weight
            if weight_to_gain > 0:
                representation['estimated_days_to_target'] = round(weight_to_gain / latest_weight.actual_daily_gain)
        
        return representation


class WeightRecordSerializer(serializers.ModelSerializer):
    """Serializer for the WeightRecord model."""
    animal_tag = serializers.ReadOnlyField(source='animal.tag_number')
    animal_name = serializers.ReadOnlyField(source='animal.name')
    recorded_by_name = serializers.ReadOnlyField(source='recorded_by.get_full_name')
    weight_variance_percent = serializers.SerializerMethodField()
    actual_daily_gain = serializers.SerializerMethodField()
    daily_gain_variance_percent = serializers.SerializerMethodField()
    
    class Meta:
        model = WeightRecord
        fields = [
            'id', 'animal', 'animal_tag', 'animal_name', 'date', 'weight',
            'notes', 'recorded_by', 'recorded_by_name', 'created_at', 'updated_at',
            'expected_weight', 'expected_next_week', 'expected_next_month',
            'expected_daily_gain', 'weight_variance_percent', 'actual_daily_gain',
            'daily_gain_variance_percent'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_weight_variance_percent(self, obj):
        """Get the variance between actual and expected weight as a percentage."""
        return obj.weight_variance
    
    def get_actual_daily_gain(self, obj):
        """Get the actual daily gain since the previous record."""
        return obj.actual_daily_gain
    
    def get_daily_gain_variance_percent(self, obj):
        """Get the variance between actual and expected daily gain as a percentage."""
        return obj.daily_gain_variance
    
    def validate(self, data):
        """Validate that weight is positive."""
        if 'weight' in data and data['weight'] <= 0:
            raise serializers.ValidationError(_("Weight must be positive."))
        return data


class SlaughterRecordSerializer(serializers.ModelSerializer):
    """Serializer for the SlaughterRecord model."""
    animal_tag = serializers.ReadOnlyField(source='animal.tag_number')
    animal_name = serializers.ReadOnlyField(source='animal.name')
    quality_grade_display = serializers.ReadOnlyField(source='get_quality_grade_display')
    recorded_by_name = serializers.ReadOnlyField(source='recorded_by.get_full_name')
    live_weight_variance_percent = serializers.SerializerMethodField()
    carcass_weight_variance_percent = serializers.SerializerMethodField()
    dressing_percentage_variance_percent = serializers.SerializerMethodField()
    
    class Meta:
        model = SlaughterRecord
        fields = [
            'id', 'animal', 'animal_tag', 'animal_name', 'slaughter_date',
            'slaughter_location', 'processor', 'live_weight', 'carcass_weight',
            'dressing_percentage', 'quality_grade', 'quality_grade_display',
            'yield_grade', 'notes', 'recorded_by', 'recorded_by_name',
            'created_at', 'updated_at', 'expected_live_weight',
            'expected_carcass_weight', 'expected_dressing_percentage',
            'live_weight_variance_percent', 'carcass_weight_variance_percent',
            'dressing_percentage_variance_percent'
        ]
        read_only_fields = ['id', 'dressing_percentage', 'created_at', 'updated_at']
    
    def get_live_weight_variance_percent(self, obj):
        """Get the variance between actual and expected live weight as a percentage."""
        return obj.live_weight_variance
    
    def get_carcass_weight_variance_percent(self, obj):
        """Get the variance between actual and expected carcass weight as a percentage."""
        return obj.carcass_weight_variance
    
    def get_dressing_percentage_variance_percent(self, obj):
        """Get the variance between actual and expected dressing percentage as a percentage."""
        return obj.dressing_percentage_variance
    
    def validate(self, data):
        """Validate that weights are positive and carcass weight is less than live weight."""
        if 'live_weight' in data and data['live_weight'] <= 0:
            raise serializers.ValidationError(_("Live weight must be positive."))
        if 'carcass_weight' in data and data['carcass_weight'] <= 0:
            raise serializers.ValidationError(_("Carcass weight must be positive."))
        if 'live_weight' in data and 'carcass_weight' in data and data['carcass_weight'] > data['live_weight']:
            raise serializers.ValidationError(_("Carcass weight cannot be greater than live weight."))
        return data
