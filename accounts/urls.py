from django.urls import path
from .views import CreateUserView, ListUsersView, RegisterView, LoginView, ValidateAccountView, PasswordResetRequestView, PasswordResetConfirmView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Liste des utilisateurs
    path('users/', ListUsersView.as_view(), name='list-users'),
    
    # Création d'un utilisateur
    path('users/create/', CreateUserView.as_view(), name='create-user'),
    
    # Enregistrement d'un nouvel utilisateur
    path('register/', RegisterView.as_view(), name='register'),
    
    # Connexion d'un utilisateur
    # path('login/', LoginView.as_view(), name='login'),
    path('login/', LoginView.as_view(), name='login'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Validation du compte utilisateur
    path('register/validate/account/', ValidateAccountView.as_view(), name='validate-account'),
    
    # Demande de réinitialisation du mot de passe
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    
    # Confirmation de la réinitialisation du mot de passe
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]
