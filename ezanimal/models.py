from django.db import models
from django.utils.translation import gettext_lazy as _


class AnimalType(models.Model):
    """
    Model representing different types of animals (e.g., Cow, Goat, Sheep, Buffalo).
    This is a system-generated model that supports multilingual fields.
    """
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    farming_type = models.CharField(
        _('farming type'),
        max_length=20,
        choices=[
            ('dairy', _('Dairy')),
            ('meat', _('Meat')),
            ('both', _('Both Dairy and Meat'))
        ],
        default='both'
    )
    is_active = models.BooleanField(_('active'), default=True)
    
    class Meta:
        verbose_name = _('animal type')
        verbose_name_plural = _('animal types')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Breed(models.Model):
    """
    Model representing different breeds within an animal type.
    This is a system-generated model that supports multilingual fields.
    """
    animal_type = models.ForeignKey(
        AnimalType, 
        on_delete=models.CASCADE,
        related_name='breeds',
        verbose_name=_('animal type')
    )
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    
    # Characteristics
    average_weight = models.DecimalField(
        _('average weight (kg)'),
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )
    average_height = models.DecimalField(
        _('average height (cm)'),
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    # Dairy-specific characteristics
    average_milk_production = models.DecimalField(
        _('average milk production (liters/day)'),
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_('Average milk production per day for dairy animals')
    )
    lactation_period = models.IntegerField(
        _('lactation period (days)'),
        null=True,
        blank=True,
        help_text=_('Average lactation period in days')
    )
    
    # Meat-specific characteristics
    average_meat_yield = models.DecimalField(
        _('average meat yield (kg)'),
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_('Average meat yield per animal')
    )
    growth_rate = models.DecimalField(
        _('growth rate (kg/month)'),
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_('Average weight gain per month')
    )
    
    # Common characteristics
    gestation_period = models.IntegerField(
        _('gestation period (days)'),
        null=True,
        blank=True,
        help_text=_('Average gestation period in days')
    )
    maturity_age = models.IntegerField(
        _('maturity age (months)'),
        null=True,
        blank=True,
        help_text=_('Age at which the animal reaches maturity in months')
    )
    
    is_active = models.BooleanField(_('active'), default=True)
    
    class Meta:
        verbose_name = _('breed')
        verbose_name_plural = _('breeds')
        ordering = ['animal_type', 'name']
        unique_together = ['animal_type', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.animal_type.name})"
