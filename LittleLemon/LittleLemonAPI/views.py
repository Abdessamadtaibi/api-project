from django.shortcuts import render,get_object_or_404
from rest_framework import generics,status
from rest_framework.views import APIView
from .models import MenuItems,Category,Order,Card,OrderItem
from . import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAdminUser ,IsAuthenticated,AllowAny
from django.contrib.auth.models import User,Group



class MenuItemViewAdmin(generics.ListCreateAPIView):
    queryset = MenuItems.objects.all()
    serializer_class = serializers.MenuitemSerializers
    permission_classes = [IsAdminUser] 



class CategoryViewAdmin(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializers
    permission_classes = [IsAdminUser] 



@api_view(['GET'])
@permission_classes([IsAdminUser])
def manager(request):
    manager_group = Group.objects.get(name = "Manager")
    managers = manager_group.user_set.all()
    serializer = serializers.UserSerializer(managers,many=True)
    return Response(serializer.data)



@api_view(['POST','DELETE'])
@permission_classes([IsAdminUser])
def manager_users(request):
    username = request.data["username"]
    if username:
        user = get_object_or_404(User,username=username)
        managers = Group.objects.get(name = "Manager")
        if request.method == 'POST':
            managers.user_set.add(user)
            return Response({"message":"User added to the Manager Group"})
        elif request.method == 'DELETE':
            managers.user_set.remove(user)
            return Response({"message":"User removed to the Manager Group"})
    return Response({"message":"Error"},status.HTTP_400_BAD_REQUEST)



class MenuItemManagerView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
            if request.user.groups.filter(name="Manager").exists():
                return Response({"message":f" Hi {request.user.username} "})
            else:
                 return Response({"message":"Error , you are not Manager"},status.HTTP_404_NOT_FOUND)
    def post(self, request):
                if request.user.groups.filter(name="Manager").exists():
                    item_id = request.data.get("item_id") 
                    if item_id:
                        MenuItems.objects.update(featured=False)
                        try:
                            item = MenuItems.objects.get(id=item_id)
                            item.featured=True
                            item.save()
                            return Response({"message":f" the item {item.id} is updated to item_of_the_day"})
                        except MenuItems.DoesNotExist : 
                            return Response({"message":"Item not existe"},status.HTTP_404_NOT_FOUND)
                    else: 
                        return Response({"message":"Error, item_id not existe"},status.HTTP_400_BAD_REQUEST)
                else: 
                        return Response({"message":"Error , you are not Manager"},status.HTTP_404_NOT_FOUND)



class DeliveryCrewManagerView(generics.GenericAPIView):
     permission_classes=[IsAuthenticated]
     def get(self, request):
            if request.user.groups.filter(name="Manager").exists():
                Delivery_group = Group.objects.get(name = "Delivery_Crew")
                delivery = Delivery_group.user_set.all()
                serializer = serializers.UserSerializer(delivery,many=True)
                return Response(serializer.data)
     def put(self, request):
                if request.user.groups.filter(name="Manager").exists():
                    username= request.data.get("username")
                    order_id = request.data.get("id_order")
                    delivery_group = Group.objects.get(name="Delivery_Crew")
                    if username:
                        user = User.objects.get(username=username)
                        delivery_group.user_set.add(user)
                        if order_id:
                            if user.groups.filter(name="Delivery_Crew").exists():
                                try:
                                    order = Order.objects.get(id=order_id)
                                    order.delivery_crew = user
                                    order.save()
                                    return Response({"message":f" the order {order.id} is added to {username}"})
                                except Order.DoesNotExist:
                                    return Response({"message":"order not existe"},status.HTTP_404_NOT_FOUND)
                            else:
                                return Response({"message":"username is not Delivery_Crew"},status.HTTP_400_BAD_REQUEST)
                        return Response({"message":f" {user} is added to the Delivery_Crew group"})
                    else:
                        return Response({"message":"Error"},status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"message":"you are not manager"},status.HTTP_400_BAD_REQUEST)



class DeliveryCrewView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.user.groups.filter(name="Delivery_Crew").exists():
            orders = Order.objects.filter(delivery_crew=request.user)
            serializer = serializers.OrderSerializer(orders,many=True)
            return Response(serializer.data)
        else:
            return Response({"message":"you are not delivery-crew"},status.HTTP_403_FORBIDDEN)
    def post(self, request):
            if request.user.groups.filter(name="Delivery_Crew").exists():
                order_id = request.data.get("id_order")
                if order_id:
                    order = get_object_or_404(Order,id=order_id)
                    if order.delivery_crew==request.user:
                        order.status = True
                        order.save()
                        return Response({"message":f" the order {order.id} is delivered "})
                    else:
                        return Response({"message":f" you don't have the order "},status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"message":"Error, id_order not fund "},status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message":"you are not delivery-crew"},status.HTTP_403_FORBIDDEN)



class RegisterView(APIView):
        permission_classes = [AllowAny]
        def post(self,request):
            serializer = serializers.RegisterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User registered successfully"})
            else:
                return Response({"message": "Error"},status.HTTP_400_BAD_REQUEST)
            


class CategoryCustomerView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        category = Category.objects.all()
        serializer = serializers.CategorySerializers(category,many=True)
        return Response(serializer.data)
    


class MenuItemCustomerView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = MenuItems.objects.all()
    serializer_class = serializers.MenuitemSerializers
    filterset_fields = ['name','price']
    search_fields = ['name','category']
    def get(self,request):
        menuitem = MenuItems.objects.all()
        serializer = serializers.MenuitemSerializers(menuitem,many=True)
        return Response(serializer.data)
    def put(self,request):
        menuitem_id = request.data.get("menuitem")
        if menuitem_id:
            try:
                menuitem = MenuItems.objects.get(id=menuitem_id)
                cart = Card.objects.get(user=request.user)
                cart.menuitem = menuitem
                cart.save()
                return Response({"message": f" {menuitem.title} added to your cart "})
            except MenuItems.DoesNotExist:
                return Response({"message": "Menu-Items does not exist"},status.HTTP_403_FORBIDDEN)
        else:
            return Response({"message": "Error"},status.HTTP_400_BAD_REQUEST)



class ItemsCardCustomerView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            card = Card.objects.get(user=request.user)
        except Card.DoesNotExist:
            return Response({"message": "card does not exist"},status.HTTP_404_NOT_FOUND)
        items = card.menuitem.all()
        serializer = serializers.MenuitemSerializers(items,many=True)
        return Response(serializer.data)
    


class OrdersCustomerView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.OrderItemSerializer
    def get_queryset(self):
         return OrderItem.objects.filter(order__user=self.request.user)

         