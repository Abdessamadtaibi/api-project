from .models import MenuItems,Category,Order,OrderItem
from rest_framework import serializers
from django.contrib.auth.models import User



class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"



class MenuitemSerializers(serializers.ModelSerializer):
    class Meta:
        model = MenuItems
        fields = ['id', 'title', 'price','category','featured']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id','delivery_crew','total','date','status')



class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order','menuitem', 'quantity', 'unit_price', 'price']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('username','email','password')
    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            email=validated_data.get['email'],
            password=validated_data['password'],
        )
        return user
