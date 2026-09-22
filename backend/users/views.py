from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import UserRegisterSerializer

# Create your views here.

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]
