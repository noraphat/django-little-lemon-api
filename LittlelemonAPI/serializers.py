from rest_framework import serializers
from django.contrib.auth.models import User, Group
from django.contrib.auth.password_validation import validate_password
from . import models

class GroupSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Group
        fields = ['name',]

class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(read_only=True, many=True)
    class Meta:
        model = User
        fields = ['username', 'id', 'email', 'groups',]
        # fields = '__all__'
        # depth = 1


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['id', 'slug', 'title']
        
class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = models.MenuItem
        fields = ['id', 'name', 'price', 'description', 'featured', 'category', 'category_id', 'image']


class CartSerializer(serializers.ModelSerializer):
    # price = serializers.SerializerMethodField(method_name = 'calculate_price')
    # unit_price = serializers.SerializerMethodField(method_name = 'menuitem_price')
    menuitem = MenuItemSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = models.Cart
        fields = ['user', 'user_id', 'menuitem', 'menuitem_id', 'quantity', 'unit_price', 'price']


class OrderItemSerializer(serializers.ModelSerializer):
    # order = UserSerializer(read_only=True)
    user_id = serializers.IntegerField()
    menuitem = MenuItemSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = models.OrderItem
        fields = ['user_id', 'menuitem', 'menuitem_id', 'quantity', 'unit_price', 'price']

class OrderSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    orderitem = OrderItemSerializer(read_only=True)
    orderitem_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = models.Order
        fields = ['id', 'user_id', 'delivery_crew','status', 'total', 'date', 'orderitem', 'orderitem_id',]


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password_confirm']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Password fields didn't match.")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(read_only=True, many=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'groups', 'date_joined', 'is_active']
        read_only_fields = ['id', 'username', 'groups', 'date_joined', 'is_active']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Booking
        fields = ['id', 'customer_name', 'email', 'phone', 'date', 'time', 'number_of_guests', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']