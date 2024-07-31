from django.urls import path
from .models import Profil

urlpatterns = [
    path('users/profil', Profil.as_view(), name='list-users'),
]
