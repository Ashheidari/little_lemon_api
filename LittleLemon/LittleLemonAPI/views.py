from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response 
from rest_framework import status
#from rest_framework.decorators import api_view 
from rest_framework import generics
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User, Group
from .models import MenuItem, Category, Cart, OrderItem, Order
from .serializers import CategorySerializer, MenuItemSerializer, UserSerializer, CartSerializer, OrderItemSerializer, SingleOrderSerilaizer, OrderSerializer, OrderSerializerForCrew
from .permissions import IsManager, IsDeliveryCrew
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from datetime import date 
# Create your views here.

class CategoryView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle,UserRateThrottle]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    




#MenusItems endpoint /menu-items
class MenuItemView(generics.ListCreateAPIView,generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [AnonRateThrottle,UserRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price']
    search_fields = ['title', 'category__title']
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        else:
            return [(IsManager | IsAdminUser)()]
    




# Managers endpoint groups/manager/users/
class ManagerView(generics.ListCreateAPIView, generics.DestroyAPIView):
    throttle_classes = [AnonRateThrottle,UserRateThrottle]
    permission_classes = [IsManager | IsAdminUser]
    queryset = User.objects.filter(groups__name = 'Managers')
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        if username:
            user = get_object_or_404(User,username = username)
            managers = Group.objects.get(name = 'Managers')
            managers.user_set.add(user)
            return Response({"message":f"success, {user.email} promote to Managers "},status=status.HTTP_201_CREATED)

        return Response({"message":"error"},status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        userId = kwargs['userId']
        if userId:
            user = get_object_or_404(User,id = userId)
            if user.groups.filter(name='Managers'):
                managers = Group.objects.get(name = 'Managers')
                managers.user_set.remove(user)
                return Response({"message":"success"},status=status.HTTP_200_OK)
            
            return Response({"message":"This user is not manager"})
        
        return Response({"message":"userId not found"},status=status.HTTP_404_NOT_FOUND) 

# Deliveycrew endpoint groups/delivery-crew/users/
class DeliveryCrewView(generics.ListCreateAPIView, generics.DestroyAPIView):
    throttle_classes = [AnonRateThrottle,UserRateThrottle]
    permission_classes = [IsManager | IsAdminUser]
    queryset = User.objects.filter(groups__name = 'Delivery_Crews')
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        if username:
            user = get_object_or_404(User,username = username)
            delivery_crew = Group.objects.get(name = 'Delivery_Crews')
            delivery_crew.user_set.add(user)
            return Response({"message":f"success, {user.email} assigned to delivery_crew "},status=status.HTTP_201_CREATED)

        return Response({"message":"error"},status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        userId = kwargs['userId']
        if userId:
            user = get_object_or_404(User,id = userId)
            if user.groups.filter(name='Delivery_Crews'):
                delivery_crew = Group.objects.get(name = 'Delivery_Crews')
                delivery_crew.user_set.remove(user)
                return Response({"message":"success"},status=status.HTTP_200_OK)
            
            return Response({"message":"This user is not member of delivery-crew"})
        
        return Response({"message":"userId not found"},status=status.HTTP_404_NOT_FOUND)
    

#Cart endpoint /cart/menu-item
class CartView(generics.ListCreateAPIView,generics.DestroyAPIView):
    throttle_classes = [AnonRateThrottle,UserRateThrottle]
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Cart.objects.filter(user = user)
        return queryset
    
    def post(self, request, *args, **kwargs):
        user = request.user
        menu_item_id = request.data['menu-item-id']
        if menu_item_id:

            try:
                menu_item = MenuItem.objects.get(pk = menu_item_id)
                
                
                existing_cart = Cart.objects.filter(user = user, menuitem = menu_item).first()
               
                if existing_cart:
                    existing_cart.quantity += 1
                    existing_cart.price = existing_cart.quantity * existing_cart.unit_price 
                    existing_cart.save()

                    serialized_cart = self.get_serializer(existing_cart)
                    return Response(serialized_cart.data, status=status.HTTP_201_CREATED,)
            except MenuItem.DoesNotExist:
                return Response({'error': 'MenuItem not found'}, status=status.HTTP_404_NOT_FOUND)
            
            cart_item = {
                "user_id":user.pk,
                "menuitem_id":menu_item.pk,
                "quantity": 1,
                "unit_price": menu_item.price,
                "price": menu_item.price,
            }
        

            serialized_cart = self.get_serializer(data = cart_item)
            serialized_cart.is_valid(raise_exception=True)
            self.perform_create(serialized_cart)
            headers = self.get_success_headers(serialized_cart.data)
            return Response(serialized_cart.data, status=status.HTTP_201_CREATED, headers= headers)
        return Response({'error': 'MenuItem_id does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        user = self.request.user
        cart = get_object_or_404(Cart, user = user)
        cart.delete()
        return Response({"message":"cart is deleted"}, status = status.HTTP_200_OK)

#Order endpoint /orders
class OrderView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle,UserRateThrottle]
    permission_classes = [IsAuthenticated]
    serializer_class = OrderItemSerializer
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name = 'Managers') or user.is_superuser:
            queryset = OrderItem.objects.all()
            return queryset
        elif user.groups.filter(name = 'Delivery_Crews'):
            queryset = OrderItem.objects.all()
            return queryset
        else:
            queryset = OrderItem.objects.filter(order__user = user)
            return queryset

    def post(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart,user = request.user)
        try:
            order = Order.objects.create(user = request.user,status = 0, total = cart.price, date = date.today())
            order_item = OrderItem(order =order, menuitem = cart.menuitem, quantity = cart.quantity, unit_price = cart.unit_price, price = cart.price)
            order.save()
            order_item.save()
            cart.delete()
            return Response({"message": "Order placed successfully"}, status=status.HTTP_201_CREATED)
        except:
            return Response({"message":"Failed to place order"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [AnonRateThrottle,UserRateThrottle]
    serializer_class = SingleOrderSerilaizer
    
    def get_permissions(self):
        user = self.request.user
        order = Order.objects.filter(pk = self.kwargs['pk'])
        if self.request.method == 'GET' and order.user == user :
            permission_classes = [IsAuthenticated]
        elif self.request.method =='PUT' or  self.request.method =='DELETE':
            permission_classes = [IsAdminUser | IsManager]

        else:
            permission_classes = [IsManager | IsDeliveryCrew | IsAdminUser]
        return [permission() for permission in permission_classes]
    def get_queryset(self):
        queryset = OrderItem.objects.filter(pk = self.kwargs['pk'])

    
    def put(self, request, *args, **kwargs):
        serilized_order = OrderSerializer(data = request.data)
        serilized_order.is_valid(raise_exception=True)
        order = get_object_or_404(Order,pk = kwargs['pk'])
        crew = get_object_or_404(User, pk = request.data['delivery_crew'])
        if crew.groups.filter(name = "Delivery_Crews"):
            try:
                order.delivery_crew = crew
                order.status = request.data['status']
                order.save()
                return Response({"message":"status & delivery crew changed"},status=status.HTTP_201_CREATED)
            except:
                return Response({"message":"internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"messsage":"The user that you want to assign this deliver is not member of delivery crews"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk = kwargs['pk'])
        order.delete()
        return super().delete(request, *args, **kwargs)
    

    def patch(self, request, *args, **kwargs):
        if request.user.groups.filter(name = 'Delivery_Crews'):
                serilized_order = OrderSerializer(data = request.data)
                serilized_order.is_valid(raise_exception=True)
                order = get_object_or_404(Order,pk = kwargs['pk'])
                crew = get_object_or_404(User, pk = request.data['delivery_crew'])
                if crew.groups.filter(name = "Delivery_Crews"):
                    try:
                        order.delivery_crew = crew
                        order.status = request.data['status']
                        order.save()
                        return Response({"message":"status & delivery crew changed"},status=status.HTTP_201_CREATED)
                    except:
                        return Response({"message":"internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({"messsage":"The user that you want to assign this deliver is not member of delivery crews"}, status=status.HTTP_400_BAD_REQUEST)
        else: 
            serilized_order = OrderSerializerForCrew(data = request.data)
            serilized_order.is_valid(raise_exception=True)
            serilized_order.save()
            return Response({"message":"status changed by delivery guy"},status=status.HTTP_201_CREATED)       