from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token
from decimal import Decimal
from datetime import date, time
from .models import Category, MenuItem, Cart, Order, OrderItem, Booking


class TestFixtures:
    
    @staticmethod
    def create_users_and_groups():
        manager_group = Group.objects.create(name='Manager')
        delivery_group = Group.objects.create(name='Delivery crew')
        
        customer = User.objects.create_user(
            username='customer',
            password='password123',
            email='customer@example.com',
            first_name='John',
            last_name='Customer'
        )
        
        manager = User.objects.create_user(
            username='manager',
            password='password123',
            email='manager@example.com',
            first_name='Jane',
            last_name='Manager'
        )
        
        delivery = User.objects.create_user(
            username='delivery',
            password='password123',
            email='delivery@example.com',
            first_name='Bob',
            last_name='Driver'
        )
        
        manager.groups.add(manager_group)
        delivery.groups.add(delivery_group)
        
        return {
            'customer': customer,
            'manager': manager,
            'delivery': delivery,
            'manager_group': manager_group,
            'delivery_group': delivery_group
        }
    
    @staticmethod
    def create_tokens(users):
        tokens = {}
        for role, user in users.items():
            if isinstance(user, User):
                tokens[role] = Token.objects.create(user=user)
        return tokens
    
    @staticmethod
    def create_categories():
        return {
            'appetizers': Category.objects.create(
                slug='appetizers',
                title='Appetizers'
            ),
            'mains': Category.objects.create(
                slug='main-courses',
                title='Main Courses'
            ),
            'desserts': Category.objects.create(
                slug='desserts',
                title='Desserts'
            ),
            'beverages': Category.objects.create(
                slug='beverages',
                title='Beverages'
            )
        }
    
    @staticmethod
    def create_menu_items(categories):
        return {
            'greek_salad': MenuItem.objects.create(
                name='Greek Salad',
                price=Decimal('12.50'),
                description='Fresh vegetables with feta cheese and olive oil',
                category=categories['appetizers'],
                featured=True
            ),
            'bruschetta': MenuItem.objects.create(
                name='Bruschetta',
                price=Decimal('8.95'),
                description='Grilled bread with fresh tomatoes and basil',
                category=categories['appetizers'],
                featured=False
            ),
            'lemon_dessert': MenuItem.objects.create(
                name='Lemon Dessert',
                price=Decimal('6.99'),
                description='Traditional lemon cake with cream',
                category=categories['desserts'],
                featured=True
            ),
            'pasta_primavera': MenuItem.objects.create(
                name='Pasta Primavera',
                price=Decimal('18.50'),
                description='Seasonal vegetables with pasta',
                category=categories['mains'],
                featured=False
            ),
            'coffee': MenuItem.objects.create(
                name='Espresso',
                price=Decimal('3.50'),
                description='Italian espresso coffee',
                category=categories['beverages'],
                featured=False
            )
        }
    
    @staticmethod
    def create_bookings(users):
        return {
            'booking1': Booking.objects.create(
                customer_name=users['customer'].username,
                email=users['customer'].email,
                phone='555-0123',
                date=date(2025, 12, 25),
                time=time(19, 30),
                number_of_guests=4
            ),
            'booking2': Booking.objects.create(
                customer_name='Guest User',
                email='guest@example.com',
                phone='555-0456',
                date=date(2025, 12, 31),
                time=time(20, 0),
                number_of_guests=2
            ),
            'booking3': Booking.objects.create(
                customer_name=users['customer'].username,
                email=users['customer'].email,
                phone='555-0123',
                date=date(2026, 1, 15),
                time=time(18, 0),
                number_of_guests=6
            )
        }
    
    @staticmethod
    def create_cart_items(users, menu_items):
        return {
            'cart1': Cart.objects.create(
                user=users['customer'],
                menuitem=menu_items['greek_salad'],
                quantity=2,
                unit_price=menu_items['greek_salad'].price,
                price=menu_items['greek_salad'].price * 2
            ),
            'cart2': Cart.objects.create(
                user=users['customer'],
                menuitem=menu_items['lemon_dessert'],
                quantity=1,
                unit_price=menu_items['lemon_dessert'].price,
                price=menu_items['lemon_dessert'].price
            )
        }
    
    @staticmethod
    def create_order_items(users, menu_items):
        return {
            'order_item1': OrderItem.objects.create(
                user=users['customer'],
                menuitem=menu_items['pasta_primavera'],
                quantity=1,
                unit_price=menu_items['pasta_primavera'].price,
                price=menu_items['pasta_primavera'].price
            ),
            'order_item2': OrderItem.objects.create(
                user=users['customer'],
                menuitem=menu_items['bruschetta'],
                quantity=2,
                unit_price=menu_items['bruschetta'].price,
                price=menu_items['bruschetta'].price * 2
            )
        }
    
    @staticmethod
    def create_orders(users, order_items):
        return {
            'order1': Order.objects.create(
                user=users['customer'],
                delivery_crew=users['delivery'],
                status=False,
                total=order_items['order_item1'].price,
                orderitem=order_items['order_item1']
            ),
            'order2': Order.objects.create(
                user=users['customer'],
                status=True,
                total=order_items['order_item2'].price,
                orderitem=order_items['order_item2']
            )
        }
    
    @classmethod
    def create_all_fixtures(cls):
        users = cls.create_users_and_groups()
        tokens = cls.create_tokens(users)
        categories = cls.create_categories()
        menu_items = cls.create_menu_items(categories)
        bookings = cls.create_bookings(users)
        cart_items = cls.create_cart_items(users, menu_items)
        order_items = cls.create_order_items(users, menu_items)
        orders = cls.create_orders(users, order_items)
        
        return {
            'users': users,
            'tokens': tokens,
            'categories': categories,
            'menu_items': menu_items,
            'bookings': bookings,
            'cart_items': cart_items,
            'order_items': order_items,
            'orders': orders
        }


class APITestMixin:
    def setUp(self):
        self.fixtures = TestFixtures.create_all_fixtures()
        self.client = APIClient()
    
    def authenticate_user(self, role='customer'):
        """Helper method to authenticate a user by role"""
        token = self.fixtures['tokens'][role]
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    
    def get_user(self, role='customer'):
        """Helper method to get a user by role"""
        return self.fixtures['users'][role]
    
    def get_menu_item(self, name='greek_salad'):
        """Helper method to get a menu item by name"""
        return self.fixtures['menu_items'][name]
    
    def get_category(self, name='appetizers'):
        """Helper method to get a category by name"""
        return self.fixtures['categories'][name]