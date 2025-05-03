from django.db import models
from django.utils.translation import gettext_lazy as _
from ezanimal.models import AnimalType, Breed
from ezcore.models import User


class DairyAnimal(models.Model):
    """Model for dairy animals."""
    
    STATUS_CHOICES = [
        ('active', _('Active')),
        ('dry', _('Dry')),
        ('pregnant', _('Pregnant')),
        ('sold', _('Sold')),
        ('deceased', _('Deceased')),
    ]
    
    GENDER_CHOICES = [
        ('female', _('Female')),
        ('male', _('Male')),
    ]
    
    tag_number = models.CharField(_('tag number'), max_length=50, unique=True)
    name = models.CharField(_('name'), max_length=100, blank=True, null=True)
    animal_type = models.ForeignKey(AnimalType, on_delete=models.PROTECT, related_name='dairy_animals', verbose_name=_('animal type'))
    breed = models.ForeignKey(Breed, on_delete=models.PROTECT, related_name='dairy_animals', verbose_name=_('breed'))
    date_of_birth = models.DateField(_('date of birth'), blank=True, null=True)
    gender = models.CharField(_('gender'), max_length=10, choices=GENDER_CHOICES, default='female')
    mother = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='offspring', verbose_name=_('mother'))
    father_tag = models.CharField(_('father tag'), max_length=50, blank=True, null=True)
    acquisition_date = models.DateField(_('acquisition date'), blank=True, null=True)
    acquisition_price = models.DecimalField(_('acquisition price'), max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='active')
    notes = models.TextField(_('notes'), blank=True, null=True)
    is_active = models.BooleanField(_('is active'), default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dairy_animals', verbose_name=_('owner'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    # New fields for breed-based defaults
    breed_avg_milk_production = models.DecimalField(_('breed average milk production (liters/day)'), max_digits=6, decimal_places=2, blank=True, null=True)
    
    class Meta:
        verbose_name = _('dairy animal')
        verbose_name_plural = _('dairy animals')
        ordering = ['tag_number']
    
    def __str__(self):
        return f"{self.tag_number} - {self.name or 'Unnamed'}"


class MilkProduction(models.Model):
    """Model for milk production records."""
    
    TIME_CHOICES = [
        ('morning', _('Morning')),
        ('evening', _('Evening')),
        ('both', _('Both')),
    ]
    
    animal = models.ForeignKey(DairyAnimal, on_delete=models.CASCADE, related_name='milk_records', verbose_name=_('animal'))
    date = models.DateField(_('date'))
    time_of_day = models.CharField(_('time of day'), max_length=10, choices=TIME_CHOICES, default='both')
    morning_amount = models.DecimalField(_('morning amount (liters)'), max_digits=6, decimal_places=2, default=0)
    evening_amount = models.DecimalField(_('evening amount (liters)'), max_digits=6, decimal_places=2, default=0)
    total_amount = models.DecimalField(_('total amount (liters)'), max_digits=6, decimal_places=2, editable=False, default=0)
    fat_content = models.DecimalField(_('fat content (%)'), max_digits=4, decimal_places=2, blank=True, null=True)
    protein_content = models.DecimalField(_('protein content (%)'), max_digits=4, decimal_places=2, blank=True, null=True)
    notes = models.TextField(_('notes'), blank=True, null=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='recorded_milk_productions', verbose_name=_('recorded by'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    # New fields for expected production
    expected_amount = models.DecimalField(_('expected amount (liters)'), max_digits=6, decimal_places=2, blank=True, null=True)
    expected_next_week = models.DecimalField(_('expected daily amount next week (liters)'), max_digits=6, decimal_places=2, blank=True, null=True)
    expected_next_month = models.DecimalField(_('expected daily amount next month (liters)'), max_digits=6, decimal_places=2, blank=True, null=True)
    
    class Meta:
        verbose_name = _('milk production')
        verbose_name_plural = _('milk productions')
        ordering = ['-date']
        unique_together = ['animal', 'date']
    
    def __str__(self):
        return f"{self.animal.tag_number} - {self.date} - {self.total_amount}L"
    
    def save(self, *args, **kwargs):
        self.total_amount = self.morning_amount + self.evening_amount
        super().save(*args, **kwargs)
    
    @property
    def production_variance(self):
        """Calculate variance between actual and expected production."""
        if not self.expected_amount or self.expected_amount == 0:
            return None
        return ((self.total_amount - self.expected_amount) / self.expected_amount) * 100


class Lactation(models.Model):
    """Model for lactation records."""
    
    animal = models.ForeignKey(DairyAnimal, on_delete=models.CASCADE, related_name='lactations', verbose_name=_('animal'))
    lactation_number = models.PositiveIntegerField(_('lactation number'))
    start_date = models.DateField(_('start date'))
    end_date = models.DateField(_('end date'), blank=True, null=True)
    total_production = models.DecimalField(_('total production (liters)'), max_digits=10, decimal_places=2, blank=True, null=True)
    peak_production = models.DecimalField(_('peak production (liters/day)'), max_digits=6, decimal_places=2, blank=True, null=True)
    peak_date = models.DateField(_('peak date'), blank=True, null=True)
    notes = models.TextField(_('notes'), blank=True, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    # New fields for expected production
    expected_total_production = models.DecimalField(_('expected total production (liters)'), max_digits=10, decimal_places=2, blank=True, null=True)
    expected_peak_production = models.DecimalField(_('expected peak production (liters/day)'), max_digits=6, decimal_places=2, blank=True, null=True)
    expected_duration_days = models.PositiveIntegerField(_('expected duration (days)'), blank=True, null=True)
    
    class Meta:
        verbose_name = _('lactation')
        verbose_name_plural = _('lactations')
        ordering = ['-start_date']
        unique_together = ['animal', 'lactation_number']
    
    def __str__(self):
        return f"{self.animal.tag_number} - Lactation {self.lactation_number}"
    
    @property
    def duration_days(self):
        """Calculate the duration of the lactation in days."""
        if not self.end_date:
            return None
        return (self.end_date - self.start_date).days
    
    @property
    def production_variance(self):
        """Calculate variance between actual and expected total production."""
        if not self.expected_total_production or self.expected_total_production == 0 or not self.total_production:
            return None
        return ((self.total_production - self.expected_total_production) / self.expected_total_production) * 100
