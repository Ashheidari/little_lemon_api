from rest_framework import serializers
from .models import MenuItem,Category,Cart,Order,OrderItem
from django.contrib.auth.models import User,Group
from rest_framework.validators import UniqueTogetherValidator


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title']


class MenuItemSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only = True)
    category = CategorySerializer(read_only = True)
    class Meta:
        model = MenuItem
        fields = ['id','title','price','featured','category','category_id']




class UserSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = User
        fields = ['id','username','email','groups']
        depth = 1


class CartSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only =True)
    menuitem_id = serializers.IntegerField(write_only =True)
    user = UserSerializer(read_only=True)
    menuitem = MenuItemSerializer(read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitem', 'quantity', 'unit_price', 'price','user_id', 'menuitem_id']
        depth = 1

    
    # def caluculate_total(self, cart:Cart):
    #     return cart.price * cart.quantity


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields= '__all__'
        depth = 1

class MenuItemHelperSerialzer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['title', 'price']
class SingleOrderSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['menuitem, quantity']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields =['delivery_crew','status']


class OrderSerializerForCrew(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["status"]