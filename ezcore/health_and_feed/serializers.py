from rest_framework import serializers
from ezcore.health_and_feed.models import (
    AnimalHealth, Vaccination, FeedType, 
    FeedingSchedule, FeedingScheduleItem, FeedingRecord
)


class AnimalHealthSerializer(serializers.ModelSerializer):
    """Serializer for the AnimalHealth model."""
    dairy_animal_tag = serializers.ReadOnlyField(source='dairy_animal.tag_number', allow_null=True)
    meat_animal_tag = serializers.ReadOnlyField(source='meat_animal.tag_number', allow_null=True)
    record_type_display = serializers.ReadOnlyField(source='get_record_type_display')
    
    class Meta:
        model = AnimalHealth
        fields = [
            'id', 'dairy_animal', 'dairy_animal_tag', 'meat_animal', 'meat_animal_tag',
            'record_date', 'record_type', 'record_type_display', 'temperature', 'weight',
            'diagnosis', 'symptoms', 'treatment', 'medication', 'dosage',
            'follow_up_date', 'recovery_date', 'vet_name', 'vet_contact',
            'cost', 'notes', 'recorded_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class VaccinationSerializer(serializers.ModelSerializer):
    """Serializer for the Vaccination model."""
    dairy_animal_tag = serializers.ReadOnlyField(source='dairy_animal.tag_number', allow_null=True)
    meat_animal_tag = serializers.ReadOnlyField(source='meat_animal.tag_number', allow_null=True)
    vaccine_type_display = serializers.ReadOnlyField(source='get_vaccine_type_display')
    administration_method_display = serializers.ReadOnlyField(source='get_administration_method_display')
    
    class Meta:
        model = Vaccination
        fields = [
            'id', 'dairy_animal', 'dairy_animal_tag', 'meat_animal', 'meat_animal_tag',
            'vaccine_name', 'vaccination_date', 'vaccine_type', 'vaccine_type_display',
            'disease', 'manufacturer', 'batch_number', 'dosage',
            'administration_method', 'administration_method_display',
            'next_due_date', 'administered_by', 'cost', 'notes',
            'recorded_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class FeedTypeSerializer(serializers.ModelSerializer):
    """Serializer for the FeedType model."""
    feed_category_display = serializers.ReadOnlyField(source='get_feed_category_display')
    
    class Meta:
        model = FeedType
        fields = [
            'id', 'name', 'description', 'feed_category', 'feed_category_display',
            'protein_percentage', 'energy_content', 'fiber_percentage',
            'suitable_for_dairy', 'suitable_for_meat', 'is_active'
        ]
        read_only_fields = ['id']


class FeedingScheduleItemSerializer(serializers.ModelSerializer):
    """Serializer for the FeedingScheduleItem model."""
    feed_type_name = serializers.ReadOnlyField(source='feed_type.name')
    frequency_display = serializers.ReadOnlyField(source='get_frequency_display')
    
    class Meta:
        model = FeedingScheduleItem
        fields = [
            'id', 'schedule', 'feed_type', 'feed_type_name', 'amount',
            'frequency', 'frequency_display', 'custom_frequency',
            'morning', 'afternoon', 'evening', 'notes'
        ]
        read_only_fields = ['id']


class FeedingScheduleSerializer(serializers.ModelSerializer):
    """Serializer for the FeedingSchedule model."""
    items = FeedingScheduleItemSerializer(many=True, read_only=True)
    animal_type_name = serializers.ReadOnlyField(source='animal_type.name', allow_null=True)
    breed_name = serializers.ReadOnlyField(source='breed.name', allow_null=True)
    
    class Meta:
        model = FeedingSchedule
        fields = [
            'id', 'name', 'description', 'animal_type', 'animal_type_name',
            'breed', 'breed_name', 'start_date', 'end_date',
            'is_active', 'created_by', 'created_at', 'updated_at', 'items'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class FeedingRecordSerializer(serializers.ModelSerializer):
    """Serializer for the FeedingRecord model."""
    dairy_animal_tag = serializers.ReadOnlyField(source='dairy_animal.tag_number', allow_null=True)
    meat_animal_tag = serializers.ReadOnlyField(source='meat_animal.tag_number', allow_null=True)
    feed_type_name = serializers.ReadOnlyField(source='feed_type.name')
    time_of_day_display = serializers.ReadOnlyField(source='get_time_of_day_display')
    
    class Meta:
        model = FeedingRecord
        fields = [
            'id', 'dairy_animal', 'dairy_animal_tag', 'meat_animal', 'meat_animal_tag',
            'date', 'feed_type', 'feed_type_name', 'amount',
            'time_of_day', 'time_of_day_display', 'schedule_item',
            'notes', 'recorded_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
