from django.shortcuts import render
from .serialziers import *
from backend.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated

class RegisterView(APIView):
    def post(self, request):
        
        username = request.data.get('username')
        email = request.data.get('email')

        if CustomUser.objects.filter(username=username).exists():
            return Response({
                "status": 0,
                "message": "Username already exists",
            })
        
        if CustomUser.objects.filter(email=email).exists():
            return Response({
                "status": 0,
                "message": "Email already exists",
            })
        
        
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "status":1,
                "message":"success",
                'data': {
                    "token":token.key
                }
            })
        return Response(serializer.errors,)



class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "status":1,
                "message":"success",
                'data': {
                    "token":token.key
                }
                })
        return Response({
            "status":0,
            "message":"Invalid credentials",
            })
        
class ProductViewApi(APIView):
    
    def get(self,request):
        products = Product.objects.filter(status="Active")
        serializer = ProductSerialzier(products,many=True)
        return Response({
            "status":1,
            "message":"success",
            "data":serializer.data
            
        })
        
class OrderListApi(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        user = request.user
        orders = Order.objects.filter(user=user).order_by('-id')
        serializer = OrderSerializer(orders,many=True)
        return Response({
            "status":1,
            "message":"success",
            "data":serializer.data
        })