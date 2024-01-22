from rest_framework import serializers
from .models import MenuItem,Category,Cart,Order,OrderItem
from django.contrib.auth.models import User,Group


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']


class MenuItemSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only = True)
    category = CategorySerializer(read_only = True)
    class Meta:
        model = MenuItem
        fields = ['id','title','featured','price','category','category_id']




class UserSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = User
        fields = ['id','username','email','groups']