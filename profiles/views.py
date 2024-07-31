from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from backoffice.models import CustomUser

class Profil(generics.CreateAPIView):
    