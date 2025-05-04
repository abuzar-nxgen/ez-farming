from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    """Custom User model with email as the unique identifier."""

    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    farm_name = models.CharField(_('farm name'), max_length=255, blank=True, null=True)
    farm_location = models.CharField(_('farm location'), max_length=255, blank=True, null=True)
    farm_size = models.FloatField(_('farm size (acres)'), blank=True, null=True)
    preferred_language = models.CharField(_('preferred language'), max_length=10,
                                          choices=[('en', 'English'), ('ur', 'Urdu')],
                                          default='en')
    is_farm_owner = models.BooleanField(_('farm owner status'), default=True)

    # New fields for employee management
    role = models.CharField(_('role'), max_length=50,
                            choices=[
                                ('owner', 'Farm Owner'),
                                ('manager', 'Farm Manager'),
                                ('veterinarian', 'Veterinarian'),
                                ('worker', 'Farm Worker'),
                                ('accountant', 'Accountant')
                            ],
                            default='owner')

    # For employees, link to their employer (farm owner)
    employer = models.ForeignKey('self', on_delete=models.CASCADE,
                                 null=True, blank=True,
                                 related_name='employees',
                                 verbose_name=_('employer'))

    # Employee-specific fields
    hire_date = models.DateField(_('hire date'), null=True, blank=True)
    job_title = models.CharField(_('job title'), max_length=100, blank=True, null=True)
    contact_number = models.CharField(_('contact number'), max_length=20, blank=True, null=True)

    # Permissions for different farm operations
    can_manage_animals = models.BooleanField(_('can manage animals'), default=False)
    can_manage_health = models.BooleanField(_('can manage health records'), default=False)
    can_manage_feeding = models.BooleanField(_('can manage feeding'), default=False)
    can_manage_inventory = models.BooleanField(_('can manage inventory'), default=False)
    can_manage_sales = models.BooleanField(_('can manage sales'), default=False)
    can_manage_employees = models.BooleanField(_('can manage employees'), default=False)
    can_view_reports = models.BooleanField(_('can view reports'), default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # Set default permissions based on role
        if self.role == 'owner':
            self.is_farm_owner = True
            self.can_manage_animals = True
            self.can_manage_health = True
            self.can_manage_feeding = True
            self.can_manage_inventory = True
            self.can_manage_sales = True
            self.can_manage_employees = True
            self.can_view_reports = True
        elif self.role == 'manager':
            self.is_farm_owner = False
            self.can_manage_animals = True
            self.can_manage_health = True
            self.can_manage_feeding = True
            self.can_manage_inventory = True
            self.can_manage_sales = True
            self.can_manage_employees = False
            self.can_view_reports = True
        elif self.role == 'veterinarian':
            self.is_farm_owner = False
            self.can_manage_animals = True
            self.can_manage_health = True
            self.can_manage_feeding = False
            self.can_manage_inventory = False
            self.can_manage_sales = False
            self.can_manage_employees = False
            self.can_view_reports = False
        elif self.role == 'worker':
            self.is_farm_owner = False
            self.can_manage_animals = True
            self.can_manage_health = False
            self.can_manage_feeding = True
            self.can_manage_inventory = False
            self.can_manage_sales = False
            self.can_manage_employees = False
            self.can_view_reports = False
        elif self.role == 'accountant':
            self.is_farm_owner = False
            self.can_manage_animals = False
            self.can_manage_health = False
            self.can_manage_feeding = False
            self.can_manage_inventory = True
            self.can_manage_sales = True
            self.can_manage_employees = False
            self.can_view_reports = True

        super().save(*args, **kwargs)
