from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Profil, CustomUser
from .serializers import ProfilSerializer
from rest_framework.exceptions import ValidationError, NotAuthenticated
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CreateProfilesView(generics.CreateAPIView):
    queryset = Profil.objects.all()
    serializer_class = ProfilSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['Profils'])
    def perform_create(self, serializer):
        user = self.request.user
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
            user = self.request.user
            return Profil.objects.get(user=user)
        except Profil.DoesNotExist:
            raise NotFound("Le profil de l'utilisateur n'a pas été trouvé.")

class UpdateProfileView(generics.UpdateAPIView):
    queryset = Profil.objects.all()
    serializer_class = ProfilSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['Profils'])
    def get_object(self):
        try:
            user = self.request.user
            return Profil.objects.get(user=user)
        except Profil.DoesNotExist:
            raise NotFound("Le profil de l'utilisateur n'a pas été trouvé.")

    @swagger_auto_schema(tags=['Profils'])
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

class DeleteProfilesView(generics.DestroyAPIView):
    serializer_class = ProfilSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['Profils'])
    def get_object(self):
        try:
            user = self.request.user
            return Profil.objects.get(user=user)
        except Profil.DoesNotExist:
            raise NotFound("Le profil de l'utilisateur n'a pas été trouvé.")

    @swagger_auto_schema(tags=['Profils'])
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class UploadResumeView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Profils'],
        operation_description="Upload a resume",
        manual_parameters=[
            openapi.Parameter(
                'resume', openapi.IN_FORM, description="Resume file", type=openapi.TYPE_FILE, required=True
            ),
        ],
        responses={201: 'Resume uploaded successfully', 400: 'No file provided'}
    )
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            profil = Profil.objects.get(user__email=user.email)
        except Profil.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

        file = request.FILES.get('resume')
        if file:
            profil.resume = file
            profil.save()
            return Response({"message": "Resume uploaded successfully"}, status=status.HTTP_201_CREATED)
        return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

class UploadCoverLetterView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Profils'],
        operation_description="Upload a cover letter",
        manual_parameters=[
            openapi.Parameter(
                'cover_letter', openapi.IN_FORM, description="Cover letter file", type=openapi.TYPE_FILE, required=True
            ),
        ],
        responses={201: 'Cover letter uploaded successfully', 400: 'No file provided'}
    )
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            profil = Profil.objects.get(user__email=user.email)
        except Profil.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

        file = request.FILES.get('cover_letter')
        if file:
            profil.cover_letter = file
            profil.save()
            return Response({"message": "Cover letter uploaded successfully"}, status=status.HTTP_201_CREATED)
        return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)