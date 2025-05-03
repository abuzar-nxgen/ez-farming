from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from ezanimal.models import AnimalType, Breed
from ezdairy.models import DairyAnimal
from ezmeat.models import MeatAnimal

class AnimalHealth(models.Model):
    """
    Model for tracking health records of animals.
    This model can be linked to either dairy or meat animals.
    """
    # Polymorphic relationship to either dairy or meat animal
    dairy_animal = models.ForeignKey(
        DairyAnimal,
        on_delete=models.CASCADE,
        related_name='health_records',
        verbose_name=_('dairy animal'),
        null=True,
        blank=True
    )
    meat_animal = models.ForeignKey(
        MeatAnimal,
        on_delete=models.CASCADE,
        related_name='health_records',
        verbose_name=_('meat animal'),
        null=True,
        blank=True
    )
    
    # Health record details
    record_date = models.DateField(_('record date'))
    record_type = models.CharField(
        _('record type'),
        max_length=20,
        choices=[
            ('routine_check', _('Routine Check')),
            ('illness', _('Illness')),
            ('injury', _('Injury')),
            ('vaccination', _('Vaccination')),
            ('treatment', _('Treatment')),
            ('surgery', _('Surgery')),
            ('other', _('Other'))
        ]
    )
    
    # Health status
    temperature = models.DecimalField(
        _('temperature (°C)'),
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True
    )
    weight = models.DecimalField(
        _('weight (kg)'),
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    # Diagnosis and treatment
    diagnosis = models.CharField(_('diagnosis'), max_length=255, blank=True)
    symptoms = models.TextField(_('symptoms'), blank=True)
    treatment = models.TextField(_('treatment'), blank=True)
    medication = models.CharField(_('medication'), max_length=255, blank=True)
    dosage = models.CharField(_('dosage'), max_length=100, blank=True)
    
    # Follow-up
    follow_up_date = models.DateField(_('follow-up date'), null=True, blank=True)
    recovery_date = models.DateField(_('recovery date'), null=True, blank=True)
    
    # Veterinarian information
    vet_name = models.CharField(_('veterinarian name'), max_length=255, blank=True)
    vet_contact = models.CharField(_('veterinarian contact'), max_length=255, blank=True)
    
    cost = models.DecimalField(
        _('cost'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    notes = models.TextField(_('notes'), blank=True)
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='recorded_health_records',
        verbose_name=_('recorded by')
    )
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('animal health record')
        verbose_name_plural = _('animal health records')
        ordering = ['-record_date']
    
    def __str__(self):
        animal = self.dairy_animal or self.meat_animal
        return f"{animal.tag_number} - {self.record_date} - {self.get_record_type_display()}"
    
    def clean(self):
        """Ensure that either dairy_animal or meat_animal is set, but not both."""
        from django.core.exceptions import ValidationError
        
        if self.dairy_animal and self.meat_animal:
            raise ValidationError(_('A health record cannot be associated with both dairy and meat animals.'))
        if not self.dairy_animal and not self.meat_animal:
            raise ValidationError(_('A health record must be associated with either a dairy or meat animal.'))


class Vaccination(models.Model):
    """
    Model for tracking vaccinations of animals.
    """
    # Polymorphic relationship to either dairy or meat animal
    dairy_animal = models.ForeignKey(
        DairyAnimal,
        on_delete=models.CASCADE,
        related_name='vaccinations',
        verbose_name=_('dairy animal'),
        null=True,
        blank=True
    )
    meat_animal = models.ForeignKey(
        MeatAnimal,
        on_delete=models.CASCADE,
        related_name='vaccinations',
        verbose_name=_('meat animal'),
        null=True,
        blank=True
    )
    
    # Vaccination details
    vaccine_name = models.CharField(_('vaccine name'), max_length=255)
    vaccination_date = models.DateField(_('vaccination date'))
    
    # Vaccine information
    vaccine_type = models.CharField(
        _('vaccine type'),
        max_length=20,
        choices=[
            ('preventive', _('Preventive')),
            ('therapeutic', _('Therapeutic')),
            ('other', _('Other'))
        ],
        default='preventive'
    )
    disease = models.CharField(_('disease'), max_length=255, blank=True)
    manufacturer = models.CharField(_('manufacturer'), max_length=255, blank=True)
    batch_number = models.CharField(_('batch number'), max_length=100, blank=True)
    
    # Administration details
    dosage = models.CharField(_('dosage'), max_length=100, blank=True)
    administration_method = models.CharField(
        _('administration method'),
        max_length=20,
        choices=[
            ('injection', _('Injection')),
            ('oral', _('Oral')),
            ('nasal', _('Nasal')),
            ('other', _('Other'))
        ],
        default='injection'
    )
    
    # Follow-up
    next_due_date = models.DateField(_('next due date'), null=True, blank=True)
    
    # Veterinarian information
    administered_by = models.CharField(_('administered by'), max_length=255, blank=True)
    
    cost = models.DecimalField(
        _('cost'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    notes = models.TextField(_('notes'), blank=True)
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='recorded_vaccinations',
        verbose_name=_('recorded by')
    )
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('vaccination')
        verbose_name_plural = _('vaccinations')
        ordering = ['-vaccination_date']
    
    def __str__(self):
        animal = self.dairy_animal or self.meat_animal
        return f"{animal.tag_number} - {self.vaccination_date} - {self.vaccine_name}"
    
    def clean(self):
        """Ensure that either dairy_animal or meat_animal is set, but not both."""
        from django.core.exceptions import ValidationError
        
        if self.dairy_animal and self.meat_animal:
            raise ValidationError(_('A vaccination cannot be associated with both dairy and meat animals.'))
        if not self.dairy_animal and not self.meat_animal:
            raise ValidationError(_('A vaccination must be associated with either a dairy or meat animal.'))


class FeedType(models.Model):
    """
    Model for different types of feed.
    This is a system-generated model that supports multilingual fields.
    """
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    
    # Feed characteristics
    feed_category = models.CharField(
        _('feed category'),
        max_length=20,
        choices=[
            ('forage', _('Forage')),
            ('concentrate', _('Concentrate')),
            ('supplement', _('Supplement')),
            ('mineral', _('Mineral')),
            ('other', _('Other'))
        ]
    )
    
    # Nutritional information
    protein_percentage = models.DecimalField(
        _('protein percentage'),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    energy_content = models.DecimalField(
        _('energy content (MJ/kg)'),
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )
    fiber_percentage = models.DecimalField(
        _('fiber percentage'),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    # Suitability
    suitable_for_dairy = models.BooleanField(_('suitable for dairy'), default=True)
    suitable_for_meat = models.BooleanField(_('suitable for meat'), default=True)
    
    # Status
    is_active = models.BooleanField(_('active'), default=True)
    
    class Meta:
        verbose_name = _('feed type')
        verbose_name_plural = _('feed types')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class FeedingSchedule(models.Model):
    """
    Model for feeding schedules.
    Can be associated with animal types, breeds, or specific animals.
    """
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    
    # Schedule can be associated with animal type, breed, or specific animals
    animal_type = models.ForeignKey(
        AnimalType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='feeding_schedules',
        verbose_name=_('animal type')
    )
    breed = models.ForeignKey(
        Breed,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='feeding_schedules',
        verbose_name=_('breed')
    )
    
    # Schedule details
    start_date = models.DateField(_('start date'))
    end_date = models.DateField(_('end date'), null=True, blank=True)
    
    # Status
    is_active = models.BooleanField(_('active'), default=True)
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_feeding_schedules',
        verbose_name=_('created by')
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('feeding schedule')
        verbose_name_plural = _('feeding schedules')
        ordering = ['-start_date', 'name']
    
    def __str__(self):
        return self.name


class FeedingScheduleItem(models.Model):
    """
    Model for individual items in a feeding schedule.
    """
    schedule = models.ForeignKey(
        FeedingSchedule,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('schedule')
    )
    feed_type = models.ForeignKey(
        FeedType,
        on_delete=models.CASCADE,
        related_name='schedule_items',
        verbose_name=_('feed type')
    )
    
    # Feeding details
    amount = models.DecimalField(
        _('amount (kg)'),
        max_digits=8,
        decimal_places=2
    )
    frequency = models.CharField(
        _('frequency'),
        max_length=20,
        choices=[
            ('daily', _('Daily')),
            ('twice_daily', _('Twice Daily')),
            ('weekly', _('Weekly')),
            ('custom', _('Custom'))
        ],
        default='daily'
    )
    custom_frequency = models.CharField(_('custom frequency'), max_length=255, blank=True)
    
    # Time of day
    time_of_day = models.CharField(
        _('time of day'),
        max_length=20,
        choices=[
            ('morning', _('Morning')),
            ('afternoon', _('Afternoon')),
            ('evening', _('Evening')),
            ('other', _('Other'))
        ],
        default='morning'
    )
    
    class Meta:
        verbose_name = _('feeding schedule item')
        verbose_name_plural = _('feeding schedule items')
        ordering = ['schedule', 'feed_type']
    
    def __str__(self):
        return f"{self.schedule.name} - {self.feed_type.name} - {self.amount}kg"


class FeedingRecord(models.Model):
    """
    Model for recording actual feeding events.
    """
    # Polymorphic relationship to either dairy or meat animal
    dairy_animal = models.ForeignKey(
        DairyAnimal,
        on_delete=models.CASCADE,
        related_name='feeding_records',
        verbose_name=_('dairy animal'),
        null=True,
        blank=True
    )
    meat_animal = models.ForeignKey(
        MeatAnimal,
        on_delete=models.CASCADE,
        related_name='feeding_records',
        verbose_name=_('meat animal'),
        null=True,
        blank=True
    )
    
    # Feeding details
    date = models.DateField(_('date'))
    feed_type = models.ForeignKey(
        FeedType,
        on_delete=models.PROTECT,
        related_name='feeding_records',
        verbose_name=_('feed type')
    )
    
    # Amount and time
    amount = models.DecimalField(_('amount (kg)'), max_digits=8, decimal_places=2)
    time_of_day = models.CharField(
        _('time of day'),
        max_length=20,
        choices=[
            ('morning', _('Morning')),
            ('afternoon', _('Afternoon')),
            ('evening', _('Evening')),
            ('other', _('Other'))
        ]
    )
    
    # Optional schedule reference
    schedule_item = models.ForeignKey(
        FeedingScheduleItem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='feeding_records',
        verbose_name=_('schedule item')
    )
    
    notes = models.TextField(_('notes'), blank=True)
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='recorded_feedings',
        verbose_name=_('recorded by')
    )
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('feeding record')
        verbose_name_plural = _('feeding records')
        ordering = ['-date', 'time_of_day']
    
    def __str__(self):
        animal = self.dairy_animal or self.meat_animal
        return f"{animal.tag_number} - {self.date} - {self.feed_type.name}"
    
    def clean(self):
        """Ensure that either dairy_animal or meat_animal is set, but not both."""
        from django.core.exceptions import ValidationError
        
        if self.dairy_animal and self.meat_animal:
            raise ValidationError(_('A feeding record cannot be associated with both dairy and meat animals.'))
        if not self.dairy_animal and not self.meat_animal:
            raise ValidationError(_('A feeding record must be associated with either a dairy or meat animal.'))
