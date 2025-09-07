# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Django REST API for the Little Lemon restaurant management system. The API provides comprehensive functionality for menu management, table reservations, user authentication, and static content serving.

## New Project Requirements

### 1. Django Project Setup
- **Project Name**: "littlelemon"
- **Framework**: Django + Django REST Framework
- **Database**: MySQL (production configuration)
- **Static Files**: HTML content serving capability
- **Authentication**: Token-based authentication

### 2. Core Models
- **Menu Model**: 
  - name (CharField)
  - price (DecimalField)
  - description (TextField)
  - category (CharField/ForeignKey)
- **Booking Model**:
  - customer_name (CharField)
  - date (DateField)
  - time (TimeField)
  - number_of_guests (IntegerField)
  - phone (CharField)

### 3. API Endpoints Structure
```
GET /api/menu/ - List all menu items
POST /api/menu/ - Create new menu item
GET /api/bookings/ - List all bookings
POST /api/bookings/ - Create new booking
PUT /api/bookings/{id}/ - Update specific booking
DELETE /api/bookings/{id}/ - Delete specific booking
```

### 4. Authentication System
- User registration endpoint
- Token authentication implementation
- Login/logout functionality
- Protected endpoints with proper permissions

### 5. Testing Requirements
- Unit tests for all API endpoints
- CRUD operations testing
- Authentication flow testing

## Development Commands

### Initial Setup
```bash
# Create virtual environment
python -m venv littlelemon-env
source littlelemon-env/bin/activate  # On Windows: littlelemon-env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create Django project
django-admin startproject littlelemon .

# Create API app
python manage.py startapp api

# Setup database (MySQL)
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Database Operations
```bash
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset database (if needed)
python manage.py flush
```

### Testing
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test api

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## Required Dependencies (requirements.txt)
```
Django>=4.2.0
djangorestframework>=3.14.0
mysqlclient>=2.1.1
django-cors-headers>=4.0.0
djangorestframework-simplejwt>=5.2.0
coverage>=7.0.0
```

## Architecture

### Project Structure
```
littlelemon/
├── littlelemon/          # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── api/                  # API application
│   ├── models.py        # Menu, Booking models
│   ├── serializers.py   # DRF serializers
│   ├── views.py         # API views
│   ├── urls.py          # API routing
│   └── tests.py         # Unit tests
├── static/              # Static HTML files
├── requirements.txt
├── README.txt
└── manage.py
```

### Database Configuration (MySQL)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'littlelemon_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Settings Configuration
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'api',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

## API Documentation

### Menu Endpoints
- **GET /api/menu/** - Retrieve all menu items
- **POST /api/menu/** - Create new menu item (requires authentication)

### Booking Endpoints
- **GET /api/bookings/** - Retrieve all bookings (requires authentication)
- **POST /api/bookings/** - Create new booking
- **PUT /api/bookings/{id}/** - Update booking (requires authentication)
- **DELETE /api/bookings/{id}/** - Delete booking (requires authentication)

### Authentication Endpoints
- **POST /api/auth/register/** - User registration
- **POST /api/auth/login/** - User login (returns token)
- **POST /api/auth/logout/** - User logout

## File Requirements

### README.txt
Should include:
- API endpoint documentation
- Setup instructions
- Database configuration
- Testing procedures

### Static HTML Files
- Restaurant homepage
- Menu display page
- Booking form page
- Contact information

## Development Guidelines

1. **Model Design**: Use appropriate field types and constraints
2. **API Security**: Implement proper authentication and permissions
3. **Error Handling**: Provide meaningful error messages
4. **Data Validation**: Use DRF serializers for input validation
5. **Testing**: Achieve comprehensive test coverage
6. **Documentation**: Maintain clear API documentation

## Current Implementation Status

This repository currently contains an existing Little Lemon API implementation. The new requirements above represent a redesign/enhancement of the current system with:
- Updated model structure
- MySQL database support
- Enhanced authentication
- Comprehensive testing
- Static file serving capability