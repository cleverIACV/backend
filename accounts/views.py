from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from backoffice.models import CustomUser
from .serializers import CreateUserSerializer, CustomUserSerializer

class CreateUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer

class ListUsersView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
