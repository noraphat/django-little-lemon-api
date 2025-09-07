from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from . import models
from decimal import Decimal
import datetime

# Authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

# Throttle
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.decorators import throttle_classes

# Determine whether the user is admin
from rest_framework.permissions import IsAdminUser

# Manage users and group
from django.contrib.auth.models import User, Group

# Serialization
from . import serializers

# Authentication views
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

# Pagination
from django.core.paginator import Paginator, EmptyPage

# Create your views here.
@api_view()
def home(request):
    return Response('The home view.', status.HTTP_200_OK)

# Test: throttle test
@api_view()
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def throttle_check(request):
    return Response({"message": "Throttle check."})

# Test: Change user's group only by admin
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAdminUser])
def manager_admin(request):
    username = request.data['username']
    message = 'User ' + username + ' '
    if username:
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name="Manager")
        if request.method == 'POST':
            managers.user_set.add(user)
            message += 'is set as manager.'
        elif request.method == 'DELETE':
            managers.user_set.remove(user)
            message += 'is deleted from manager group.'
        elif request.method == 'GET':
            serialized_item = serializers.UserSerializer(managers, many=True)
            return Response(serialized_item.data)
        return Response({"message": message})
    return Response({"message": "error"}, status.HTTP_400_BAD_REQUEST)

# Test: serialization of Group
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAdminUser])
def group_view(request):
    if request.method == 'GET':
        serialized_item = serializers.GroupSerializer(Group.objects.all(), many=True)
        return Response(serialized_item.data)

# endpoint: /api/category
# allow GET for all users
# allow POST only for managers
# GET: Lists all categories. Return a 200 – Ok HTTP status code
# POST: Creates a new category and returns 201 - Created
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def category(request):
    if request.method == 'GET':
        items = models.Category.objects.all()
        serialized_item = serializers.CategorySerializer(items, many=True)
        return Response(serialized_item.data, status.HTTP_200_OK)
    if request.method == 'POST' and request.user.groups.filter(name='Manager').exists():
        serialized_item = serializers.CategorySerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_201_CREATED)
    return Response({"message": "You are not authorized."}, status.HTTP_403_FORBIDDEN)

# endpoint: /api/category/{categoryItem}
# allow GET for all users
# allow PUT, PATCH, DELETE only for managers
# GET: Lists single category item. Return a 200 – Ok HTTP status code
# PUT, PATCH: Updates single category item
# DELETE: Deletes menu item
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def category_single(request, id):
    item = get_object_or_404(models.Category, pk=id)
    if request.method == 'GET':
        serialized_item = serializers.CategorySerializer(item)
        return Response(serialized_item.data, status.HTTP_200_OK)
    elif request.method == 'POST':
        return Response({"message": "You are not authorized."}, status.HTTP_403_FORBIDDEN)
    if not request.user.groups.filter(name='Manager').exists():
        return Response({"message": "You are not authorized."}, status.HTTP_403_FORBIDDEN)
    if request.method == 'PUT':
        serialized_item = serializers.CategorySerializer(item, data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_205_RESET_CONTENT)
    if request.method == 'PATCH':
        serialized_item = serializers.CategorySerializer(item, data=request.data, partial=True)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_205_RESET_CONTENT)
    if request.method == 'DELETE':
        item.delete()
        # message = item.title + ' is deleted.'
        return Response(status.HTTP_204_NO_CONTENT)

# endpoint: /api/menu-items
# allow GET for all users
# allow POST only for managers
# GET: Lists all menu items. Return a 200 – Ok HTTP status code
# POST: Creates a new menu item and returns 201 - Created
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def menuitems(request):
    if request.method == 'GET':
        items = models.MenuItem.objects.all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage', default=2)
        page = request.query_params.get('page', default=1)
        if category_name:
            items = items.filter(category__title=category_name)
        if to_price:
            items = items.filter(price__lte=to_price)
        if search:
            items = items.filter(title__icontains=search)
        if ordering:
            ordering_fields = ordering.split(",")
            items = items.order_by(*ordering_fields)
        
        paginator = Paginator(items, per_page=perpage)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []
        serialized_item = serializers.MenuItemSerializer(items, many=True)
        return Response(serialized_item.data, status.HTTP_200_OK)
    if request.method == 'POST' and request.user.groups.filter(name='Manager').exists():
        serialized_item = serializers.MenuItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_201_CREATED)
    return Response({"message": "You are not authorized."}, status.HTTP_403_FORBIDDEN)

# endpoint: /api/menu-items/{menuItem}
# allow GET for all users
# allow PUT, PATCH, DELETE only for managers
# GET: Lists single menu item. Return a 200 – Ok HTTP status code
# PUT, PATCH: Updates single menu item
# DELETE: Deletes menu item
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def menuitems_single(request, id):
    item = get_object_or_404(models.MenuItem, pk=id)
    if request.method == 'GET':
        serialized_item = serializers.MenuItemSerializer(item)
        return Response(serialized_item.data, status.HTTP_200_OK)
    elif request.method == 'POST' or not request.user.groups.filter(name='Manager').exists():
        return Response({"message": "You are not authorized."}, status.HTTP_403_FORBIDDEN)
    if request.method == 'PUT':
        serialized_item = serializers.MenuItemSerializer(item, data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_205_RESET_CONTENT)
    if request.method == 'PATCH':
        serialized_item = serializers.MenuItemSerializer(item, data=request.data, partial=True)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_205_RESET_CONTENT)
    if request.method == 'DELETE':
        item.delete()
        return Response(status.HTTP_204_NO_CONTENT)

# endpoint: /api/groups/manager/users
# allow GET and POST method for Manager only
# GET: Returns all managers
# POST: Assigns the user in the payload to the manager group and returns 201-Created
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def manager_set(request):
    if not request.user.groups.filter(name='Manager').exists():
        return Response({"message": "You are not authorized."}, status.HTTP_403_FORBIDDEN)
    
    if request.method == 'POST':
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
        else:
            return Response({"message": "Username is incorrect or not existed."}, status.HTTP_400_BAD_REQUEST)
        managers = Group.objects.get(name="Manager")
        managers.user_set.add(user)
        message = 'User ' + username + ' ' 'is set as manager.'
        return Response({"message": message}, status.HTTP_201_CREATED) 
    elif request.method == 'GET':
        managers = User.objects.filter(groups = Group.objects.get(name="Manager"))
        # managers = User.objects.all()
        serialized_item = serializers.UserSerializer(managers, many=True)
        return Response(serialized_item.data)
        # return Response(managers)

# endpoint: /api/groups/manager/users/{userId}
# allow DELETE for Manager only
# DELETE: Removes this particular user from the manager group and returns 200 – Success if everything is okay.
#         If the user is not found, returns 404 – Not found
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def manager_delete(request, id):
    if request.user.groups.filter(name='Manager').exists():
        if request.method != 'DELETE':
            return Response({"message": "This endpoint only supports DELETE."}, status.HTTP_400_BAD_REQUEST) 
        user = get_object_or_404(User, id=id)
        if user.groups.filter(name='Manager').exists():
            managers = Group.objects.get(name="Manager")
            managers.user_set.remove(user)
            message = 'User ' + user.get_username + ' ' + 'is not manager now.'
            return Response({"message": message}, status.HTTP_200_OK)
        else:
            return Response({"message": "This user is not a manager"}, status.HTTP_400_BAD_REQUEST) 
    else:
        return Response({"message": "You are not authorized."}, status.HTTP_403_FORBIDDEN)

# endpoint: /api/groups/delivery-crew/users
# allow GET and POST method for Manager only
# GET: Returns all Returns all delivery crew
# POST: Assigns the user in the payload to the delivery crew group and returns 201-Created
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def delivery_set(request):
    if not request.user.groups.filter(name='Manager').exists():
        return Response({"message": "You are not authorized."}, status.HTTP_403_FORBIDDEN)
    
    if request.method == 'POST':
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
        else:
            return Response({"message": "Username is incorrect or not existed."}, status.HTTP_400_BAD_REQUEST)
        crews = Group.objects.get(name="Delivery crew")
        crews.user_set.add(user)
        message = 'User ' + username + ' ' 'is set as delivery crew.'
        return Response({"message": message}, status.HTTP_201_CREATED) 
    elif request.method == 'GET':
        crews = User.objects.filter(groups = Group.objects.get(name="Delivery crew"))
        serialized_item = serializers.UserSerializer(crews, many=True)
        return Response(serialized_item.data)

# endpoint: /api/groups/delivery-crew/users/{userId}
# allow DELETE for Manager only
# DELETE: Removes this particular user from the delivery crew group and returns 200 – Success if everything is okay.
#         If the user is not found, returns 404 – Not found
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def delivery_delete(request, id):
    if request.user.groups.filter(name='Manager').exists():
        if request.method != 'DELETE':
            return Response({"message": "This endpoint only supports DELETE."}, status.HTTP_400_BAD_REQUEST) 
        user = get_object_or_404(User, id=id)
        if user.groups.filter(name='Delivery crew').exists():
            crews = Group.objects.get(name="Delivery crew")
            crews.user_set.remove(user)
            message = 'User ' + user.get_username + ' ' + 'is not delivery crew now.'
            return Response({"message": message}, status.HTTP_200_OK)
        else:
            return Response({"message": "This user is not a delivery crew"}, status.HTTP_400_BAD_REQUEST) 
    else:
        return Response({"message": "You are not authorized."}, status.HTTP_403_FORBIDDEN)
    

# endpoint: /api/cart/menu-items
# allow GET, POST, DELETE for Costomer
# GET: Returns current items in the cart for the current user token
# POST: Adds the menu item to the cart. Sets the authenticated user as the user id for these cart items
# DELETE: Deletes all menu items created by the current user token
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def cart(request):
    if request.method == 'GET':
        try:
            cart = models.Cart.objects.get(user=request.user)
        except:
            return Response({"message": "The cart is empty."}, status.HTTP_400_BAD_REQUEST)
        # serialized_item = serializers.MenuItemSerializer(cart.menuitem_id)
        serialized_item = serializers.CartSerializer(cart)
        return Response(serialized_item.data, status.HTTP_200_OK)
    if request.method == 'POST':
        if models.Cart.objects.filter(user=request.user).exists():
            return Response({"message": "The user has already a cart."}, status.HTTP_400_BAD_REQUEST)
        menuitem = request.data["menuitem"]
        quantity = request.data["quantity"]
        unit_price = models.MenuItem.objects.get(pk=menuitem).price
        price = Decimal(quantity) * unit_price
        data = {"menuitem_id": menuitem, 
                "quantity": quantity,
                "unit_price": unit_price,
                "price": price,
                "user_id": request.user.id,
        }
        serialized_item = serializers.CartSerializer(data=data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        message = 'Cart is created.'
        return Response({"message": message}, status.HTTP_201_CREATED)
    if request.method == 'DELETE':
        cart = get_object_or_404(models.Cart, user=request.user)
        cart.delete()
        return Response(status.HTTP_204_NO_CONTENT)

# endpoint: /api/orders
# allow GET for all users, POST for Customer
# GET: Customer: Returns all orders with order items created by this user
#      Manager: Returns all orders with order items by all users
#      Delivery crew: Returns all orders with order items assigned to the delivery crew
# POST: Creates a new order item for the current user. 
#       Gets current cart items from the cart endpoints and adds those items to the order items table. 
#       Then deletes all items from the cart for this user.
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def order(request):
    if request.method == 'GET':
        if request.user.groups.filter(name='Manager').exists():
            orders = models.Order.objects.all()
            to_price = request.query_params.get('to_price')
            search = request.query_params.get('search')
            ordering = request.query_params.get('ordering')
            perpage = request.query_params.get('perpage', default=2)
            page = request.query_params.get('page', default=1)
            if to_price:
                orders = orders.filter(total__lte=to_price)
            if search:
                orders = orders.filter(status__icontains=search)
            if ordering:
                ordering_fields = ordering.split(",")
                orders = orders.order_by(*ordering_fields)
            
            paginator = Paginator(orders, per_page=perpage)
            try:
                orders = paginator.page(number=page)
            except EmptyPage:
                orders = []
            serialized_order = serializers.OrderSerializer(orders, many=True)
            return Response(serialized_order.data, status.HTTP_200_OK)
        elif request.user.groups.filter(name='Delivery crew').exists():
            orders = models.Order.objects.filter(delivery_crew=request.user)
            serialized_order = serializers.OrderSerializer(orders, many=True)
            return Response(serialized_order.data, status.HTTP_200_OK)
        else: # customer view
            if models.Order.objects.filter(user=request.user).exists():
                order = models.Order.objects.filter(user=request.user)
                serialized_order = serializers.OrderSerializer(order)
                return Response(serialized_order.data, status.HTTP_200_OK)
            else:
                return Response(status.HTTP_404_NOT_FOUND)
    if request.method == 'POST':
        cart = get_object_or_404(models.Cart, user=request.user)
        # create order and orderitem
        
        orderitem_data = {
            "user_id": cart.user_id,
            "menuitem_id": cart.menuitem_id,
            "quantity": cart.quantity,
            "unit_price": cart.unit_price,
            "price": cart.price
        }
        serialized_orderitem = serializers.OrderItemSerializer(data=orderitem_data)
        serialized_orderitem.is_valid(raise_exception=True)
        serialized_orderitem.save()
        orderitem = models.OrderItem.objects.get(user=request.user, menuitem=cart.menuitem)
        order_data = {
            "user_id": cart.user_id,
            "total": cart.price,
            "orderitem_id": orderitem.id,
        }
        serialized_order = serializers.OrderSerializer(data=order_data)
        serialized_order.is_valid(raise_exception=True)
        serialized_order.save()
        
        cart.delete()
        message = 'Order is created.'
        return Response({"message": message}, status.HTTP_201_CREATED)
    return Response({"message": "You are not authorized."}, status.HTTP_403_FORBIDDEN) 

# endpoint: /api/orders/{orderId}
# allow GET, PUT, PATCH for Customer, DELETE for Manager, PATCH for Delivery crew
# GET: Customer: Returns all items for this order id. 
#                If the order ID doesn’t belong to the current user, it displays an appropriate HTTP error status code.
# PUT, PATCH: Updates the order. 
#             A manager can use this endpoint to set a delivery crew to this order, and also update the order status to 0 or 1.
#             If a delivery crew is assigned to this order and the status = 0, it means the order is out for delivery.
#             If a delivery crew is assigned to this order and the status = 1, it means the order has been delivered.
# PATCH: Delivery crew: A delivery crew can use this endpoint to update the order status to 0 or 1. 
#                       The delivery crew will not be able to update anything else in this order.
# DELETE: Manager: Deletes this order
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def order_single(request, id):
    order = get_object_or_404(models.Order, pk=id)
    if request.method == 'GET':
        if order.user != request.user:
            return Response({"message": "You are not authorized."}, status.HTTP_403_FORBIDDEN)
        serialized_order = serializers.OrderSerializer(order)
        return Response(serialized_order.data, status.HTTP_200_OK)
    if request.method == 'PUT':
        # only manager could perform PUT action
        if not request.user.groups.filter(name='Manager').exists():
            return Response({"message": "You are not authorized."}, status.HTTP_403_FORBIDDEN) 
        serialized_item = serializers.OrderSerializer(order, data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_205_RESET_CONTENT)
    if request.method == 'PATCH':
        if request.user.groups.filter(name='Delivery crew').exists(): 
            # delivery crew can only PATCH the order where the delivery crew is him/her.
            if order.delivery_crew != request.user:
                return Response({"message": "You are not authorized."}, status.HTTP_403_FORBIDDEN)
            # only status of the order can be changed
            deliverystatus = request.data["status"]
            status_data = {"status": deliverystatus}
            serialized_item = serializers.OrderSerializer(order, data=status_data, partial=True)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data, status.HTTP_205_RESET_CONTENT)
        if request.user.groups.filter(name='Manager').exists():
            serialized_item = serializers.OrderSerializer(order, data=request.data, partial=True)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data, status.HTTP_205_RESET_CONTENT)
        return Response({"message": "You are not authorized."}, status.HTTP_403_FORBIDDEN) 
    if request.method == 'DELETE':
        if not request.user.groups.filter(name='Manager').exists():
            return Response({"message": "You are not authorized."}, status.HTTP_403_FORBIDDEN)
        order.delete()
        return Response(status.HTTP_204_NO_CONTENT)


class IsManagerOrReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user.groups.filter(name='Manager').exists()


class LittleLemonPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class MenuViewSet(viewsets.ModelViewSet):
    queryset = models.MenuItem.objects.all()
    serializer_class = serializers.MenuItemSerializer
    permission_classes = [IsManagerOrReadOnly]
    pagination_class = LittleLemonPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'featured', 'price']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'category']
    ordering = ['name']

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def create(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({"message": "You are not authorized."}, status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({"message": "You are not authorized."}, status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({"message": "You are not authorized."}, status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({"message": "You are not authorized."}, status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = models.Booking.objects.all()
    serializer_class = serializers.BookingSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LittleLemonPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['date', 'number_of_guests']
    search_fields = ['customer_name', 'email', 'phone']
    ordering_fields = ['date', 'time', 'customer_name', 'number_of_guests']
    ordering = ['date', 'time']

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        if self.request.user.groups.filter(name='Manager').exists():
            return models.Booking.objects.all()
        return models.Booking.objects.filter(customer_name=self.request.user.username)

    def perform_create(self, serializer):
        if not self.request.user.groups.filter(name='Manager').exists():
            serializer.save(customer_name=self.request.user.username)
        else:
            serializer.save()

    def update(self, request, *args, **kwargs):
        booking = self.get_object()
        if not request.user.groups.filter(name='Manager').exists() and booking.customer_name != request.user.username:
            return Response({"message": "You can only update your own bookings."}, status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        booking = self.get_object()
        if not request.user.groups.filter(name='Manager').exists() and booking.customer_name != request.user.username:
            return Response({"message": "You can only update your own bookings."}, status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        booking = self.get_object()
        if not request.user.groups.filter(name='Manager').exists() and booking.customer_name != request.user.username:
            return Response({"message": "You can only delete your own bookings."}, status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = serializers.UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'User created successfully',
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if username and password:
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Login successful',
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'token': token.key
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    try:
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({'error': 'No token found'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    if request.method == 'GET':
        serializer = serializers.UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = serializers.UserProfileSerializer(request.user, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)