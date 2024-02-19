import math 
from datetime import date
from rest_framework import generics,status
from .models import *
from .serializers import *
from .permissions import *
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .pagination import MenuItemListPagination
from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
# Create your views here.
#=====================================================
# Create MenuItemListView.
class MenuItemListView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    search_fields = ['title','category__title']
    ordering_fields=['price','category']
    pagination_class = MenuItemListPagination
    def get_permissions(self):
        if self.request.method == 'GET':
            return[IsAuthenticated()]
        elif self.request.method == "POST":
            return[IsAdminUser()]
        else:
            return[]
#=====================================================
# GET AND ADD  Create CategoryView.
class CategoryView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    def get_permissions(self):
        if self.request.method == "POST" or "GET":
            return[IsAdminUser()]
        else:
            return[]
#=====================================================
# PATCH AND DELETE MenuItemDetailView.
class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    pagination_class = MenuItemListPagination
    def get_permissions(self):
        if self.request.method == 'PATCH':
            return[IsAuthenticated(), IsAdminUser() or Manager()]
        if self.request.method == 'DELETE':
            return[IsAuthenticated(),IsAdminUser()]
        else:
            return[IsAuthenticated()]
    def patch(self,request, *args, **kwargs):
        menuitems = self.get_object()
        serializer = self.get_serializer(menuitems,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#=====================================================
#adding manager to group
class ManagersAddView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = User.objects.filter(groups__name=Manager)
    serializer_class = ManagerAddSerializer
    permission_classes = [IsAuthenticated, Manager | IsAdminUser]
    pagination_class = MenuItemListPagination

    def create(self,request,*args, **kwargs):
        username = request.data['username']
        if username is None:
            return Response({'message': 'Username not provided'}, status=status.HTTP_400_BAD_REQUEST)
        manager_group = Group.objects.get(name='Manager')
        user = get_object_or_404(User, username=username)
        if user in manager_group.user_set.all():            
            return Response({'message': 'User is already in the manager group'}, status=status.HTTP_400_BAD_REQUEST)   
        else:
            manager_group.user_set.add(user)
        return Response(data={'message': 'User added to Managers group'}, status=status.HTTP_201_CREATED)
#=====================================================
#Removing manager to group
class ManagersRemoveView(generics.DestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = User.objects.filter(groups__name=Manager)
    serializer_class = ManagerAddSerializer
    permission_classes = [IsAuthenticated, Manager | IsAdminUser]
    pagination_class = MenuItemListPagination

    def delete(self,request,*args,**kwargs):
        user_id = kwargs.get('pk')
        if not user_id:
            return Response({'message': 'User ID not provided'}, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User,pk=user_id)
        manager_group = Group.objects.get(name='Manager')
        if user not in manager_group.user_set.all():            
            return Response({'message': 'User is not in the manager group'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            manager_group.user_set.remove(user)
            return Response({'message': f'{user.username} is removed from Managers group'}, status=status.HTTP_204_NO_CONTENT)        
#=====================================================
#adding to DeliverCrew
class DeliverCrewAddView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = User.objects.filter(groups__name=DeliveryCrew)
    serializer_class = ManagerAddSerializer
    permission_classes = [IsAuthenticated, Manager | IsAdminUser]
    pagination_class = MenuItemListPagination

    def create(self,request,*arg,**kwargs):
        username=request.data['username']
        if username is None:
            return Response({'message': 'Username not provided'}, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, username=username)
        delivery_crew_group = Group.objects.get(name='DeliveryCrew')
        if user in delivery_crew_group.user_set.all():
            return Response({'message': 'User is already in the Delivery Crew group'}, status=status.HTTP_400_BAD_REQUEST)   
        else:
            delivery_crew_group.user_set.add(user)
            return Response(data={'message': 'User added to Delivery Crew group'}, status=status.HTTP_201_CREATED)
#=====================================================
#Removing to DeliverCrew
class DeliverCrewRemoveView(generics.DestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = User.objects.filter(groups__name=DeliveryCrew)
    serializer_class = ManagerAddSerializer
    permission_classes = [IsAuthenticated, Manager | IsAdminUser]
    pagination_class = MenuItemListPagination

    def delete(self,request,*args,**kwargs):
        user_id = kwargs.get('pk')
        if not user_id:
            return Response({'message': 'User ID not provided'}, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User,pk=user_id)
        delivery_crew_group = Group.objects.get(name='DeliveryCrew')
        if user not in delivery_crew_group.user_set.all():
            return Response({'message': 'User is not in the DeliveryCrew'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            delivery_crew_group.user_set.remove(user)
            return Response({'message': f'{user.username} is removed from DeliveryCrew group'}, status=status.HTTP_204_NO_CONTENT)        
#=====================================================
# ADD or DELETE menu items to cart
class CartRequestsView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
    pagination_class = MenuItemListPagination

    def get_queryset(self,*args,**kwargs):
        user_cart = Cart.objects.filter(user=self.request.user)
        return user_cart
    
    def create(self,request,*args,**kwargs):
        serializers_item = CartAddSerializer(data=request.data)
        serializers_item.is_valid(raise_exception=True)
        id = request.data['menuitems']
        quantity = request.data['quantity']
        item = get_object_or_404(MenuItem,id=id)
        price = int(quantity) * item.price
        try:
            Cart.objects.create(user=request.user, quantity=quantity, unit_price=item.price, price=price, menuitems_id=id)
        except:
            return Response({'message': f'{item.title} is already in your cart'}, status=status.HTTP_409_CONFLICT)        
        return Response({'message': f'{item.title} is added to your cart'}, status=status.HTTP_201_CREATED)
            
    def delete(self,request,*args,**kwargs):
        if request.data['menuitems']:
            serializers_item=CartRemoveSerializer(data=request.data)
            serializers_item.is_valid(raise_exception=True)
            menuitems = request.data['menuitems']
            cart = get_object_or_404(Cart,user=request.user,menuitems=menuitems)
            cart.delete()
            return Response({'message': f'{cart.menuitems.title} Item removed from cart'}, status=status.HTTP_204_NO_CONTENT)
        else:
            Cart.objects.filter(user=request.user).delete()
            return Response({'message': 'All Items removed from cart'}, status=status.HTTP_204_NO_CONTENT)
#=====================================================
class OrderRequestsView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = OrderSerializer
    pagination_class = MenuItemListPagination
    
    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if user.groups.filter(name='Manager').exists() or user.is_superuser:
            queryset = Order.objects.all()
        elif user.groups.filter(name='DeliveryCrew').exists():
            queryset = Order.objects.filter(delivery_crew=user)
        else:
            queryset = Order.objects.filter(user=user)
        return queryset

    def get_permissions(self):
        if self.request.method in ['GET', 'POST']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, Manager | IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def post(self, request, *args, **kwargs):
        cart = Cart.objects.filter(user=request.user)
        if not cart.exists():
            return Response({'message': 'Your cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
        total = sum(float(item.price) for item in cart)
        order = Order.objects.create(user=request.user, status=False, total=total, date=date.today())
        for item in cart.values():
            menuitem = get_object_or_404(MenuItem, id=item['menuitems_id'])
            unit_price = menuitem.price
            quantity = item['quantity']
            price = unit_price * quantity
            OrderItem.objects.create(order=order, menuitems=menuitem, quantity=quantity, unit_price=unit_price, price=price)
        cart.delete()
        return Response({'message': f'Your order has been placed! Your order number is {order.id}'}, status=status.HTTP_201_CREATED)
#=====================================================
class SingleOrderView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = Order.objects.all()
    serializer_class = SingleOrderSerializer
    def update(self, request, *args, **kwargs):
        order = self.get_object()
        if request.user.groups.filter(name='DeliveryCrew').exists():
            # Allow delivery crew to update only if the order is assigned to them
            if order.delivery_crew == request.user:
                return super().update(request, *args, **kwargs)
            else:
                return Response("Not allowed", status=status.HTTP_403_FORBIDDEN)
        
        if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
            return super().update(request, *args, **kwargs)
        else:
            # Deny access for users who are not managers or delivery crew
            return Response("Not allowed", status=status.HTTP_403_FORBIDDEN)