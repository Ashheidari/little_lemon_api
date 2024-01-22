from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.decorators import api_view 
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User, Group
from .models import MenuItem
from .serializers import MenuItemSerializer, UserSerializer
from .permissions import IsManager
# Create your views here.

class MenuItemView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer



class ManagerView(generics.ListCreateAPIView):
    permission_classes = [IsManager]
    queryset = User.objects.filter(groups__name = 'Managers')
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        if username:
            user = get_object_or_404(User,username = username)
            managers = Group.objects.get(name = 'Managers')
            managers.user_set.add(user)
            return Response({"message":"ok"})

            
        return Response({"message":"error"},status=status.HTTP_400_BAD_REQUEST)