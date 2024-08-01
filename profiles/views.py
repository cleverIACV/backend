from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Profil, CustomUser
from .serializers import ProfilSerializer
from rest_framework.exceptions import ValidationError, NotAuthenticated
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CreateProfilesView(generics.CreateAPIView):
    queryset = Profil.objects.all()
    serializer_class = ProfilSerializer
    permission_classes = [IsAuthenticated]  # Assurez-vous que l'utilisateur est authentifié

    @swagger_auto_schema(tags=['Profils'])
    def perform_create(self, serializer):
        user = self.request.user  # Récupère l'utilisateur connecté
        if not user.is_authenticated:
            raise NotAuthenticated("Vous devez être connecté pour créer un profil.")
        serializer.save(user=user)

class UserAuthProfileView(generics.RetrieveAPIView):
    queryset = Profil.objects.all()
    serializer_class = ProfilSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['Profils'])
    def get_object(self):
        try:
            return Profil.objects.get(user=self.request.user)
        except Profil.DoesNotExist:
            raise NotFound("Le profil de l'utilisateur n'a pas été trouvé.")

class DeleteProfilesView(generics.DestroyAPIView):
    serializer_class = ProfilSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['Profils'])
    def get_object(self):
        try:
            return Profil.objects.get(user=self.request.user)
        except Profil.DoesNotExist:
            raise NotFound("Le profil de l'utilisateur n'a pas été trouvé.")

    @swagger_auto_schema(tags=['Profils'])
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
