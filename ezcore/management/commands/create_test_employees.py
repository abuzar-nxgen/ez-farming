from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create test employees with different roles for testing permissions'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating test employees with different roles...')
        
        # Create farm owner if it doesn't exist
        farm_owner = None
        if not User.objects.filter(email='farm.owner@ezfarming.com').exists():
            farm_owner = User.objects.create_user(
                email='farm.owner@ezfarming.com',
                password='owner123',
                first_name='Farm',
                last_name='Owner',
                farm_name='Test Farm',
                farm_location='Test Location',
                farm_size=100.0,
                preferred_language='en',
                is_farm_owner=True,
                role='owner'
            )
            self.stdout.write(self.style.SUCCESS('Farm owner created'))
        else:
            farm_owner = User.objects.get(email='farm.owner@ezfarming.com')
        
        # Create farm manager
        if not User.objects.filter(email='farm.manager@ezfarming.com').exists():
            User.objects.create_user(
                email='farm.manager@ezfarming.com',
                password='manager123',
                first_name='Farm',
                last_name='Manager',
                preferred_language='en',
                is_farm_owner=False,
                role='manager',
                employer=farm_owner,
                hire_date='2023-01-15',
                job_title='Farm Manager',
                contact_number='123-456-7890'
            )
            self.stdout.write(self.style.SUCCESS('Farm manager created'))
        
        # Create veterinarian
        if not User.objects.filter(email='vet@ezfarming.com').exists():
            User.objects.create_user(
                email='vet@ezfarming.com',
                password='vet123',
                first_name='Farm',
                last_name='Veterinarian',
                preferred_language='en',
                is_farm_owner=False,
                role='veterinarian',
                employer=farm_owner,
                hire_date='2023-02-20',
                job_title='Veterinarian',
                contact_number='123-456-7891'
            )
            self.stdout.write(self.style.SUCCESS('Veterinarian created'))
        
        # Create farm worker
        if not User.objects.filter(email='worker@ezfarming.com').exists():
            User.objects.create_user(
                email='worker@ezfarming.com',
                password='worker123',
                first_name='Farm',
                last_name='Worker',
                preferred_language='en',
                is_farm_owner=False,
                role='worker',
                employer=farm_owner,
                hire_date='2023-03-10',
                job_title='Farm Worker',
                contact_number='123-456-7892'
            )
            self.stdout.write(self.style.SUCCESS('Farm worker created'))
        
        # Create accountant
        if not User.objects.filter(email='accountant@ezfarming.com').exists():
            User.objects.create_user(
                email='accountant@ezfarming.com',
                password='accountant123',
                first_name='Farm',
                last_name='Accountant',
                preferred_language='en',
                is_farm_owner=False,
                role='accountant',
                employer=farm_owner,
                hire_date='2023-04-05',
                job_title='Accountant',
                contact_number='123-456-7893'
            )
            self.stdout.write(self.style.SUCCESS('Accountant created'))
        
        self.stdout.write(self.style.SUCCESS('Test employees creation completed successfully'))
