from django.db import models
from django.utils.translation import gettext_lazy as _
from ezanimal.models import AnimalType, Breed
from ezcore.models import User


class MeatAnimal(models.Model):
    """Model for meat animals."""
    
    STATUS_CHOICES = [
        ('growing', _('Growing')),
        ('finishing', _('Finishing')),
        ('ready', _('Ready for Slaughter')),
        ('sold', _('Sold')),
        ('slaughtered', _('Slaughtered')),
        ('deceased', _('Deceased')),
    ]
    
    GENDER_CHOICES = [
        ('female', _('Female')),
        ('male', _('Male')),
        ('castrated', _('Castrated Male')),
    ]
    
    tag_number = models.CharField(_('tag number'), max_length=50, unique=True)
    name = models.CharField(_('name'), max_length=100, blank=True, null=True)
    animal_type = models.ForeignKey(AnimalType, on_delete=models.PROTECT, related_name='meat_animals', verbose_name=_('animal type'))
    breed = models.ForeignKey(Breed, on_delete=models.PROTECT, related_name='meat_animals', verbose_name=_('breed'))
    date_of_birth = models.DateField(_('date of birth'), blank=True, null=True)
    gender = models.CharField(_('gender'), max_length=10, choices=GENDER_CHOICES)
    mother = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='offspring', verbose_name=_('mother'))
    father_tag = models.CharField(_('father tag'), max_length=50, blank=True, null=True)
    acquisition_date = models.DateField(_('acquisition date'), blank=True, null=True)
    acquisition_price = models.DecimalField(_('acquisition price'), max_digits=10, decimal_places=2, blank=True, null=True)
    acquisition_weight = models.DecimalField(_('acquisition weight (kg)'), max_digits=6, decimal_places=2, blank=True, null=True)
    current_weight = models.DecimalField(_('current weight (kg)'), max_digits=6, decimal_places=2, blank=True, null=True)
    target_weight = models.DecimalField(_('target weight (kg)'), max_digits=6, decimal_places=2, blank=True, null=True)
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='growing')
    notes = models.TextField(_('notes'), blank=True, null=True)
    is_active = models.BooleanField(_('is active'), default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meat_animals', verbose_name=_('owner'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    # New fields for breed-based defaults
    breed_avg_daily_gain = models.DecimalField(_('breed average daily gain (kg/day)'), max_digits=4, decimal_places=2, blank=True, null=True)
    breed_avg_finishing_weight = models.DecimalField(_('breed average finishing weight (kg)'), max_digits=6, decimal_places=2, blank=True, null=True)
    breed_avg_days_to_finish = models.PositiveIntegerField(_('breed average days to finish'), blank=True, null=True)
    
    class Meta:
        verbose_name = _('meat animal')
        verbose_name_plural = _('meat animals')
        ordering = ['tag_number']
    
    def __str__(self):
        return f"{self.tag_number} - {self.name or 'Unnamed'}"
    
    @property
    def age_in_days(self):
        """Calculate the age of the animal in days."""
        if not self.date_of_birth:
            return None
        from django.utils import timezone
        return (timezone.now().date() - self.date_of_birth).days
    
    @property
    def weight_gain_progress(self):
        """Calculate progress towards target weight as percentage."""
        if not self.acquisition_weight or not self.current_weight or not self.target_weight:
            return None
        total_gain_needed = self.target_weight - self.acquisition_weight
        actual_gain = self.current_weight - self.acquisition_weight
        if total_gain_needed <= 0:
            return 100
        return min(100, (actual_gain / total_gain_needed) * 100)


class WeightRecord(models.Model):
    """Model for weight records."""
    
    animal = models.ForeignKey(MeatAnimal, on_delete=models.CASCADE, related_name='weight_records', verbose_name=_('animal'))
    date = models.DateField(_('date'))
    weight = models.DecimalField(_('weight (kg)'), max_digits=6, decimal_places=2)
    notes = models.TextField(_('notes'), blank=True, null=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='recorded_weights', verbose_name=_('recorded by'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    # New fields for expected production
    expected_weight = models.DecimalField(_('expected weight (kg)'), max_digits=6, decimal_places=2, blank=True, null=True)
    expected_next_week = models.DecimalField(_('expected weight next week (kg)'), max_digits=6, decimal_places=2, blank=True, null=True)
    expected_next_month = models.DecimalField(_('expected weight next month (kg)'), max_digits=6, decimal_places=2, blank=True, null=True)
    expected_daily_gain = models.DecimalField(_('expected daily gain (kg/day)'), max_digits=4, decimal_places=2, blank=True, null=True)
    
    class Meta:
        verbose_name = _('weight record')
        verbose_name_plural = _('weight records')
        ordering = ['-date']
        unique_together = ['animal', 'date']
    
    def __str__(self):
        return f"{self.animal.tag_number} - {self.date} - {self.weight}kg"
    
    def save(self, *args, **kwargs):
        # Update the current weight of the animal
        super().save(*args, **kwargs)
        self.animal.current_weight = self.weight
        self.animal.save(update_fields=['current_weight'])
    
    @property
    def weight_variance(self):
        """Calculate variance between actual and expected weight."""
        if not self.expected_weight or self.expected_weight == 0:
            return None
        return ((self.weight - self.expected_weight) / self.expected_weight) * 100
    
    @property
    def previous_record(self):
        """Get the previous weight record for this animal."""
        return WeightRecord.objects.filter(
            animal=self.animal, 
            date__lt=self.date
        ).order_by('-date').first()
    
    @property
    def actual_daily_gain(self):
        """Calculate the actual daily gain since the previous record."""
        prev = self.previous_record
        if not prev:
            return None
        days_difference = (self.date - prev.date).days
        if days_difference <= 0:
            return None
        return (self.weight - prev.weight) / days_difference
    
    @property
    def daily_gain_variance(self):
        """Calculate variance between actual and expected daily gain."""
        actual = self.actual_daily_gain
        if not actual or not self.expected_daily_gain or self.expected_daily_gain == 0:
            return None
        return ((actual - self.expected_daily_gain) / self.expected_daily_gain) * 100


class SlaughterRecord(models.Model):
    """Model for slaughter records."""
    
    QUALITY_CHOICES = [
        ('prime', _('Prime')),
        ('choice', _('Choice')),
        ('select', _('Select')),
        ('standard', _('Standard')),
        ('commercial', _('Commercial')),
        ('utility', _('Utility')),
    ]
    
    animal = models.OneToOneField(MeatAnimal, on_delete=models.CASCADE, related_name='slaughter_record', verbose_name=_('animal'))
    slaughter_date = models.DateField(_('slaughter date'))
    slaughter_location = models.CharField(_('slaughter location'), max_length=100, blank=True, null=True)
    processor = models.CharField(_('processor'), max_length=100, blank=True, null=True)
    live_weight = models.DecimalField(_('live weight (kg)'), max_digits=6, decimal_places=2)
    carcass_weight = models.DecimalField(_('carcass weight (kg)'), max_digits=6, decimal_places=2)
    dressing_percentage = models.DecimalField(_('dressing percentage'), max_digits=5, decimal_places=2, editable=False, default=0)
    quality_grade = models.CharField(_('quality grade'), max_length=20, choices=QUALITY_CHOICES, blank=True, null=True)
    yield_grade = models.CharField(_('yield grade'), max_length=10, blank=True, null=True)
    notes = models.TextField(_('notes'), blank=True, null=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='recorded_slaughters', verbose_name=_('recorded by'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    # New fields for expected production
    expected_live_weight = models.DecimalField(_('expected live weight (kg)'), max_digits=6, decimal_places=2, blank=True, null=True)
    expected_carcass_weight = models.DecimalField(_('expected carcass weight (kg)'), max_digits=6, decimal_places=2, blank=True, null=True)
    expected_dressing_percentage = models.DecimalField(_('expected dressing percentage'), max_digits=5, decimal_places=2, blank=True, null=True)
    
    class Meta:
        verbose_name = _('slaughter record')
        verbose_name_plural = _('slaughter records')
        ordering = ['-slaughter_date']
    
    def __str__(self):
        return f"{self.animal.tag_number} - {self.slaughter_date}"
    
    def save(self, *args, **kwargs):
        if self.live_weight and self.carcass_weight and self.live_weight > 0:
            self.dressing_percentage = (self.carcass_weight / self.live_weight) * 100
        super().save(*args, **kwargs)
        # Update the animal status
        self.animal.status = 'slaughtered'
        self.animal.is_active = False
        self.animal.save(update_fields=['status', 'is_active'])
    
    @property
    def live_weight_variance(self):
        """Calculate variance between actual and expected live weight."""
        if not self.expected_live_weight or self.expected_live_weight == 0:
            return None
        return ((self.live_weight - self.expected_live_weight) / self.expected_live_weight) * 100
    
    @property
    def carcass_weight_variance(self):
        """Calculate variance between actual and expected carcass weight."""
        if not self.expected_carcass_weight or self.expected_carcass_weight == 0:
            return None
        return ((self.carcass_weight - self.expected_carcass_weight) / self.expected_carcass_weight) * 100
    
    @property
    def dressing_percentage_variance(self):
        """Calculate variance between actual and expected dressing percentage."""
        if not self.expected_dressing_percentage or self.expected_dressing_percentage == 0:
            return None
        return ((self.dressing_percentage - self.expected_dressing_percentage) / self.expected_dressing_percentage) * 100
