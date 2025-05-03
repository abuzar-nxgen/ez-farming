# EZ Farming - Livestock Management System

EZ Farming is a comprehensive Django Rest Framework (DRF) backend for a livestock management system designed to help farm owners efficiently manage their livestock operations. The system supports both dairy and meat farming with a modular architecture that can be extended to other farming types in the future.

## Features

- **Multilingual Support**: English and Urdu languages
- **User Management**: 
  - Custom user model with email authentication using django-allauth
  - Employee management with role-based permissions (Owner, Manager, Veterinarian, Worker, Accountant)
- **Animal Management**:
  - Animal types and breeds registration
  - Dairy animal tracking with milk production records
  - Meat animal tracking with weight records and slaughter data
- **Health Management**:
  - Health records and treatments
  - Vaccination tracking
- **Feeding Management**:
  - Feed types and feeding schedules
  - Feeding records
- **Inventory Management**:
  - Inventory tracking for feed, medicine, and supplies
  - Low stock alerts
- **Financial Management**:
  - Sales tracking for animals, milk, and meat
  - Expense tracking
- **API Documentation**: Swagger and ReDoc interfaces

## Technical Stack

- **Backend**: Django Rest Framework (Python)
- **Database**: SQLite (can be configured for PostgreSQL)
- **Authentication**: Django's built-in authentication with django-allauth
- **API Documentation**: drf-yasg (Swagger/ReDoc)
- **Internationalization**: Django i18n for multilingual support

## Project Structure

The project follows a modular structure with separate apps for different functionalities:

- **ezcore**: Core functionality, user model, health and feeding models, inventory and sales models
- **ezanimal**: Animal types and breeds
- **ezdairy**: Dairy animal management and milk production
- **ezmeat**: Meat animal management and slaughter records

## Role-Based Permissions

The system implements a comprehensive role-based permission system:

- **Farm Owner**: Full access to all farm data and operations
- **Farm Manager**: Can manage animals, health records, feeding, inventory, and sales
- **Veterinarian**: Can manage animals and health records
- **Farm Worker**: Can manage animals and feeding
- **Accountant**: Can manage inventory and sales, and view reports

Each role has specific permissions that determine what data they can access and what operations they can perform.

## API Endpoints

The API is organized into the following main sections:

- `/api/animal/`: Animal types and breeds
- `/api/dairy/`: Dairy animals and milk production
- `/api/meat/`: Meat animals, weight records, and slaughter data
- `/api/core/health-feeding/`: Health records, vaccinations, feed types, and feeding
- `/api/core/inventory-sales/`: Inventory, sales, and expenses
- `/api/users/`: User management including employee management

## Installation and Setup

### Prerequisites

- Python 3.10+
- pip

### Installation Steps

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ez_farming.git
   cd ez_farming
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Apply migrations:
   ```
   python manage.py migrate
   ```

4. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

5. Load test data (optional):
   ```
   python manage.py create_test_data
   python manage.py create_test_employees
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

## API Documentation

The API documentation is available at:

- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`

## Authentication

The API uses token-based authentication. To obtain a token:

1. Make a POST request to `/api-token-auth/` with your email and password
2. Include the token in the Authorization header for subsequent requests:
   ```
   Authorization: Token your_token_here
   ```

## Test Users

The system comes with pre-configured test users for different roles:

- **Farm Owner**: farm.owner@ezfarming.com / owner123
- **Farm Manager**: farm.manager@ezfarming.com / manager123
- **Veterinarian**: vet@ezfarming.com / vet123
- **Farm Worker**: worker@ezfarming.com / worker123
- **Accountant**: accountant@ezfarming.com / accountant123

## Development

### Creating Migrations

```
python manage.py makemigrations
```

### Applying Migrations

```
python manage.py migrate
```

### Running Tests

```
python manage.py test
```

## Deployment

For production deployment:

1. Set `DEBUG = False` in settings.py
2. Configure a production-ready database (PostgreSQL recommended)
3. Set up a proper web server (Nginx, Apache) with WSGI/ASGI
4. Configure static files serving
5. Set up proper security measures (HTTPS, secure cookies, etc.)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Django and Django Rest Framework communities
- All contributors to the project
