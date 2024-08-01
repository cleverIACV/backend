from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from .serializers import CreateUserSerializer, CustomUserSerializer, RegisterSerializer, LoginSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer
from backoffice.models import CustomUser
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework.authtoken.models import Token 
from rest_framework_simplejwt.tokens import RefreshToken
from email_app.utils import send_email

# Vue pour créer un nouvel utilisateur
class CreateUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer
    

# Vue pour lister tous les utilisateurs
class ListUsersView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

# Vue pour enregistrer un nouvel utilisateur
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        subject = 'Activate Your Account'
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_link = reverse('validate-account') + f"?uidb64={uid}&token={token}"
        activation_url = f"http://{current_site.domain}{activation_link}"
        context = {
            'user': user,
            'message': f"Please click the link to activate your account: {activation_url}",
            'subject': subject,
        }
        send_email(subject, user.email, 'email/default_email.html', context)
        return user

# Vue pour connecter un utilisateur
# class LoginView(generics.GenericAPIView):
#     serializer_class = LoginSerializer
#     def post(self, request, *args, **kwargs):
        # serializer = LoginSerializer(data=request.data)
        # if serializer.is_valid():
        #     # Authentifie l'utilisateur
        #     user = authenticate(
        #         request,
        #         username=serializer.validated_data['username'],
        #         password=serializer.validated_data['password']
        #     )
            
        #     # Si l'utilisateur est authentifié, le connecter
        #     if user is not None:
        #         login(request, user)
        #         # Générer un token pour l'utilisateur
        #         token, created = Token.objects.get_or_create(user=user)
        #         return Response({
        #             'token': token.key,
        #             'user_id': user.pk,
        #             'username': user.username,
        #             'email': user.email
        #         }, status=status.HTTP_200_OK)
        #     else:
        #         return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                request,
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vue pour valider un compte utilisateur via un lien de confirmation
class ValidateAccountView(APIView):
    def get(self, request, *args, **kwargs):
        uidb64 = request.query_params.get('uidb64')
        token = request.query_params.get('token')
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'detail': 'Account successfully validated'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

# Vue pour demander une réinitialisation de mot de passe
class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        
        # Générer un token de réinitialisation de mot de passe
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        current_site = get_current_site(request)
        
        # Construire le lien de réinitialisation de mot de passe
        mail_subject = 'Reset your password'
        reset_link = reverse('password-reset-confirm', kwargs={'uidb64': uid, 'token': token})
        reset_url = f"http://{current_site.domain}{reset_link}"
        message = f"Click the link to reset your password: {reset_url}"
        
        # Envoyer l'email de réinitialisation de mot de passe
        send_mail(mail_subject, message, 'noreply@mydomain.com', [user.email])
        return Response({'detail': 'Password reset link sent'}, status=status.HTTP_200_OK)

# Vue pour confirmer la réinitialisation du mot de passe
class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uidb64 = serializer.validated_data['uidb64']
        token = serializer.validated_data['token']
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            # Réinitialiser le mot de passe de l'utilisateur
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'detail': 'Password successfully reset'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid token or user'}, status=status.HTTP_400_BAD_REQUEST)