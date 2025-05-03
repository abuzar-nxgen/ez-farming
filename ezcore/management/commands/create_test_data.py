from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from ezanimal.models import AnimalType, Breed
from ezdairy.models import DairyAnimal
from ezmeat.models import MeatAnimal
from ezcore.health_and_feed.models import FeedType
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate database with initial test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating test data...')
        
        # Create superuser if it doesn't exist
        if not User.objects.filter(email='admin@ezfarming.com').exists():
            User.objects.create_superuser(
                email='admin@ezfarming.com',
                password='admin123',
                first_name='Admin',
                last_name='User',
                farm_name='EZ Farm Demo',
                preferred_language='en'
            )
            self.stdout.write(self.style.SUCCESS('Superuser created'))
        
        # Create regular user if it doesn't exist
        if not User.objects.filter(email='farmer@ezfarming.com').exists():
            User.objects.create_user(
                email='farmer@ezfarming.com',
                password='farmer123',
                first_name='Test',
                last_name='Farmer',
                farm_name='Test Farm',
                farm_location='Test Location',
                farm_size=50.0,
                preferred_language='en'
            )
            self.stdout.write(self.style.SUCCESS('Regular user created'))
        
        # Create animal types
        animal_types = [
            {
                'name': _('Cow'),
                'description': _('Domestic bovine farm animal kept for milk or meat production'),
                'farming_type': 'both'
            },
            {
                'name': _('Buffalo'),
                'description': _('Domestic bovine farm animal known for rich milk production'),
                'farming_type': 'both'
            },
            {
                'name': _('Goat'),
                'description': _('Small ruminant farm animal kept for milk or meat production'),
                'farming_type': 'both'
            },
            {
                'name': _('Sheep'),
                'description': _('Small ruminant farm animal primarily kept for meat and wool'),
                'farming_type': 'meat'
            },
        ]
        
        for animal_type_data in animal_types:
            AnimalType.objects.get_or_create(
                name=animal_type_data['name'],
                defaults={
                    'description': animal_type_data['description'],
                    'farming_type': animal_type_data['farming_type']
                }
            )
        
        self.stdout.write(self.style.SUCCESS('Animal types created'))
        
        # Create breeds
        cow_type = AnimalType.objects.get(name=_('Cow'))
        goat_type = AnimalType.objects.get(name=_('Goat'))
        
        breeds = [
            {
                'animal_type': cow_type,
                'name': _('Holstein'),
                'description': _('High milk producing dairy breed'),
                'average_milk_production': 30.0,
                'lactation_period': 305,
                'average_weight': 680.0
            },
            {
                'animal_type': cow_type,
                'name': _('Jersey'),
                'description': _('Dairy breed known for high butterfat content'),
                'average_milk_production': 20.0,
                'lactation_period': 290,
                'average_weight': 450.0
            },
            {
                'animal_type': cow_type,
                'name': _('Angus'),
                'description': _('Popular beef cattle breed'),
                'average_meat_yield': 350.0,
                'growth_rate': 1.2,
                'average_weight': 700.0
            },
            {
                'animal_type': goat_type,
                'name': _('Saanen'),
                'description': _('High milk producing dairy goat breed'),
                'average_milk_production': 3.5,
                'lactation_period': 280,
                'average_weight': 65.0
            },
        ]
        
        for breed_data in breeds:
            Breed.objects.get_or_create(
                animal_type=breed_data['animal_type'],
                name=breed_data['name'],
                defaults={
                    'description': breed_data['description'],
                    'average_milk_production': breed_data.get('average_milk_production'),
                    'lactation_period': breed_data.get('lactation_period'),
                    'average_meat_yield': breed_data.get('average_meat_yield'),
                    'growth_rate': breed_data.get('growth_rate'),
                    'average_weight': breed_data.get('average_weight')
                }
            )
        
        self.stdout.write(self.style.SUCCESS('Breeds created'))
        
        # Create feed types
        feed_types = [
            {
                'name': _('Alfalfa Hay'),
                'description': _('High-protein forage for dairy animals'),
                'feed_category': 'forage',
                'protein_percentage': 18.0,
                'suitable_for_dairy': True,
                'suitable_for_meat': True
            },
            {
                'name': _('Corn Silage'),
                'description': _('Fermented corn forage for energy'),
                'feed_category': 'forage',
                'protein_percentage': 8.0,
                'suitable_for_dairy': True,
                'suitable_for_meat': True
            },
            {
                'name': _('Dairy Concentrate'),
                'description': _('High-energy feed mix for lactating animals'),
                'feed_category': 'concentrate',
                'protein_percentage': 22.0,
                'suitable_for_dairy': True,
                'suitable_for_meat': False
            },
            {
                'name': _('Beef Finisher'),
                'description': _('High-energy feed for finishing beef cattle'),
                'feed_category': 'concentrate',
                'protein_percentage': 14.0,
                'suitable_for_dairy': False,
                'suitable_for_meat': True
            },
        ]
        
        for feed_type_data in feed_types:
            FeedType.objects.get_or_create(
                name=feed_type_data['name'],
                defaults={
                    'description': feed_type_data['description'],
                    'feed_category': feed_type_data['feed_category'],
                    'protein_percentage': feed_type_data['protein_percentage'],
                    'suitable_for_dairy': feed_type_data['suitable_for_dairy'],
                    'suitable_for_meat': feed_type_data['suitable_for_meat']
                }
            )
        
        self.stdout.write(self.style.SUCCESS('Feed types created'))
        
        # Create sample animals
        farmer = User.objects.get(email='farmer@ezfarming.com')
        holstein = Breed.objects.get(name=_('Holstein'))
        angus = Breed.objects.get(name=_('Angus'))
        
        # Create dairy animal
        if not DairyAnimal.objects.filter(tag_number='D001').exists():
            DairyAnimal.objects.create(
                owner=farmer,
                animal_type=cow_type,
                breed=holstein,
                tag_number='D001',
                name='Daisy',
                date_of_birth='2022-01-15',
                gender='female',
                weight=550.0,
                acquisition_date='2022-01-15',
                acquisition_type='born',
                status='lactating'
            )
        
        # Create meat animal
        if not MeatAnimal.objects.filter(tag_number='M001').exists():
            MeatAnimal.objects.create(
                owner=farmer,
                animal_type=cow_type,
                breed=angus,
                tag_number='M001',
                name='Angus1',
                date_of_birth='2023-03-10',
                gender='male',
                initial_weight=80.0,
                current_weight=350.0,
                acquisition_date='2023-03-10',
                acquisition_type='born',
                target_weight=550.0,
                expected_finish_date='2024-09-10',
                status='growing'
            )
        
        self.stdout.write(self.style.SUCCESS('Sample animals created'))
        
        self.stdout.write(self.style.SUCCESS('Test data creation completed successfully'))
