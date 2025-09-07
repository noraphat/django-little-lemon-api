#!/usr/bin/env python3
"""
Script to create sample data for Little Lemon restaurant
Run with: python manage.py shell < create_sample_data.py
"""

import os
import django
from datetime import date, time, datetime, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Littlelemon.settings')
django.setup()

from LittlelemonAPI.models import Category, MenuItem, Booking

# Create categories
categories = [
    {'title': 'Appetizers', 'slug': 'appetizers'},
    {'title': 'Main Courses', 'slug': 'main-courses'},
    {'title': 'Desserts', 'slug': 'desserts'},
    {'title': 'Beverages', 'slug': 'beverages'},
]

print("Creating categories...")
for cat_data in categories:
    category, created = Category.objects.get_or_create(
        slug=cat_data['slug'],
        defaults={'title': cat_data['title']}
    )
    if created:
        print(f"Created category: {category.title}")
    else:
        print(f"Category already exists: {category.title}")

# Create menu items
menu_items = [
    {
        'name': 'Mediterranean Bruschetta',
        'price': 12.99,
        'description': 'Fresh tomatoes, basil, garlic, and olive oil on toasted bread',
        'category_slug': 'appetizers',
        'featured': True
    },
    {
        'name': 'Greek Salad',
        'price': 14.50,
        'description': 'Fresh vegetables with feta cheese, olives, and Greek dressing',
        'category_slug': 'appetizers',
        'featured': False
    },
    {
        'name': 'Grilled Salmon',
        'price': 28.99,
        'description': 'Fresh Atlantic salmon with lemon herbs and Mediterranean vegetables',
        'category_slug': 'main-courses',
        'featured': True
    },
    {
        'name': 'Chicken Souvlaki',
        'price': 24.99,
        'description': 'Grilled chicken skewers with Greek seasonings, served with rice and pita',
        'category_slug': 'main-courses',
        'featured': False
    },
    {
        'name': 'Lamb Moussaka',
        'price': 26.99,
        'description': 'Traditional Greek casserole with layers of lamb, eggplant, and béchamel sauce',
        'category_slug': 'main-courses',
        'featured': True
    },
    {
        'name': 'Baklava',
        'price': 8.99,
        'description': 'Traditional Greek pastry with phyllo, nuts, and honey',
        'category_slug': 'desserts',
        'featured': False
    },
    {
        'name': 'Greek Yogurt Parfait',
        'price': 9.50,
        'description': 'Thick Greek yogurt with honey, nuts, and fresh berries',
        'category_slug': 'desserts',
        'featured': False
    },
    {
        'name': 'Fresh Lemonade',
        'price': 4.99,
        'description': 'Freshly squeezed lemon juice with mint',
        'category_slug': 'beverages',
        'featured': False
    },
    {
        'name': 'Greek Coffee',
        'price': 3.99,
        'description': 'Traditional Greek coffee served strong and sweet',
        'category_slug': 'beverages',
        'featured': False
    },
]

print("\nCreating menu items...")
for item_data in menu_items:
    category = Category.objects.get(slug=item_data['category_slug'])
    menu_item, created = MenuItem.objects.get_or_create(
        name=item_data['name'],
        defaults={
            'price': item_data['price'],
            'description': item_data['description'],
            'category': category,
            'featured': item_data['featured']
        }
    )
    if created:
        print(f"Created menu item: {menu_item.name}")
    else:
        print(f"Menu item already exists: {menu_item.name}")

# Create sample bookings
today = date.today()
bookings = [
    {
        'customer_name': 'Maria Gonzalez',
        'email': 'maria.gonzalez@email.com',
        'phone': '+1-555-0123',
        'date': today + timedelta(days=1),
        'time': time(18, 30),
        'number_of_guests': 4
    },
    {
        'customer_name': 'John Smith',
        'email': 'john.smith@email.com',
        'phone': '+1-555-0124',
        'date': today + timedelta(days=2),
        'time': time(19, 0),
        'number_of_guests': 2
    },
    {
        'customer_name': 'Elena Petrov',
        'email': 'elena.petrov@email.com',
        'phone': '+1-555-0125',
        'date': today + timedelta(days=3),
        'time': time(20, 0),
        'number_of_guests': 6
    },
    {
        'customer_name': 'Ahmed Hassan',
        'email': 'ahmed.hassan@email.com',
        'phone': '+1-555-0126',
        'date': today + timedelta(days=5),
        'time': time(17, 30),
        'number_of_guests': 3
    },
    {
        'customer_name': 'Sophie Laurent',
        'email': 'sophie.laurent@email.com',
        'phone': '+1-555-0127',
        'date': today + timedelta(days=7),
        'time': time(19, 30),
        'number_of_guests': 2
    },
]

print("\nCreating bookings...")
for booking_data in bookings:
    booking, created = Booking.objects.get_or_create(
        customer_name=booking_data['customer_name'],
        date=booking_data['date'],
        time=booking_data['time'],
        defaults={
            'email': booking_data['email'],
            'phone': booking_data['phone'],
            'number_of_guests': booking_data['number_of_guests']
        }
    )
    if created:
        print(f"Created booking: {booking.customer_name} - {booking.date} {booking.time}")
    else:
        print(f"Booking already exists: {booking.customer_name} - {booking.date} {booking.time}")

print("\n✅ Sample data creation completed!")
print(f"Categories: {Category.objects.count()}")
print(f"Menu Items: {MenuItem.objects.count()}")
print(f"Bookings: {Booking.objects.count()}")