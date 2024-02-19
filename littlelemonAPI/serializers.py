from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ['username']
#=====================================================
class MenuItemSerializer(serializers.ModelSerializer):
    category_title = serializers.ReadOnlyField(source='category.title')
    class Meta():
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category','category_title']
        #validate data from reputed data
    def validate_title(self,value):
        if MenuItem.objects.filter(title=value).exists():
            raise serializers.ValidationError("Item with this title already exists.")
        return value
#=====================================================
class CategorySerializer(serializers.ModelSerializer):
    class Meta():
        model = Category
        fields = ['title','slug','id']
#validate data from reputed data
    def validate_title(self,value):
        if Category.objects.filter(title=value).exists():
            raise serializers.ValidationError("Category with this title already exists.")
        return value
#=====================================================
class ManagerAddSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ['id','username','email']
#=====================================================
class CartSerializer(serializers.ModelSerializer):
    menuitems = MenuItemSerializer()
    class Meta():
        model = Cart
        fields = ['menuitems','quantity','price',]
#=====================================================      
class CartAddSerializer(serializers.ModelSerializer):
    class Meta():
        model = Cart
        fields = ['menuitems','quantity']
        extra_kwargs = {
            'quantity': {'min_value': 1},
        }
#=====================================================           
class CartRemoveSerializer(serializers.ModelSerializer):
    class Meta():
        model = Cart
        fields = ['menuitems']
#=====================================================
class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta():
        model = Order
        fields = "__all__"
#=====================================================
class SingleOrderSerializer(serializers.ModelSerializer):
    orderItem = OrderSerializer(many=True, read_only=True, source='order')
    class Meta:
        model = Order
        fields= ['id', 'user', 'delivery_crew', 'status', 'date', 'total', 'orderItem']