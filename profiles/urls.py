from django.urls import path
from .views import CreateProfilesView, UserAuthProfileView, DeleteProfilesView
 
urlpatterns = [
    path('profil/', UserAuthProfileView.as_view(), name='profil'),
    path('profil/create', CreateProfilesView.as_view(), name='create profil'),
    path('profil/delete/<int:user_id>/', DeleteProfilesView.as_view(), name='destroy profil'),
]