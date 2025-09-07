from django.contrib import admin
from .models import Category, MenuItem, Cart, OrderItem, Order, Booking

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title']

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'featured']
    list_filter = ['category', 'featured']
    search_fields = ['name', 'description']
    list_editable = ['price', 'featured']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'menuitem', 'quantity', 'unit_price', 'price']
    list_filter = ['user']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'menuitem', 'quantity', 'unit_price', 'price']
    list_filter = ['user']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'total', 'date', 'delivery_crew']
    list_filter = ['status', 'date', 'delivery_crew']
    search_fields = ['user__username']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'email', 'phone', 'date', 'time', 'number_of_guests']
    list_filter = ['date', 'number_of_guests']
    search_fields = ['customer_name', 'email', 'phone']
    date_hierarchy = 'date'
    ordering = ['date', 'time']
