from django.urls import path
from .views import CreateProfilesView, UserAuthProfileView, UpdateProfileView, DeleteProfilesView

urlpatterns = [
    path('profil/', UserAuthProfileView.as_view(), name='profil'),
    path('profil/create', CreateProfilesView.as_view(), name='create-profil'),
    path('profil/update/', UpdateProfileView.as_view(), name='update-profil'),
    path('profil/delete/', DeleteProfilesView.as_view(), name='delete-profil'),
]
