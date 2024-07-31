from django.urls import path
from .views import CreateUserView, ListUsersView

urlpatterns = [
    path('users/', ListUsersView.as_view(), name='list-users'),
    path('users/create/', CreateUserView.as_view(), name='create-user'),
]
