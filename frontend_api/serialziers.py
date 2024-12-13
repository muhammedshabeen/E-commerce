from rest_framework import serializers
from backend.models import *

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            user_type="Customer",
        )
        return user
    
class ProductSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title','description','price','stock','average_rating','image','color','size',]
        
        

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerialzier()
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['order_id', 'status', 'created_at', 'address', 'total_amount', 'items']