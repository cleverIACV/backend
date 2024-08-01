from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Candidature
from .serializers import CandidatureSerializer
from drf_yasg.utils import swagger_auto_schema

class CandidatureListCreateView(generics.ListCreateAPIView):
    queryset = Candidature.objects.all()
    serializer_class = CandidatureSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['Candidatures'])
    def perform_create(self, serializer):
        user = self.request.user
        profile = user.profile  # Assurez-vous que chaque utilisateur a un profil
        serializer.save(candidate=profile)

class CandidatureRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidature.objects.all()
    serializer_class = CandidatureSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['Candidatures'])
    def get_queryset(self):
        user = self.request.user
        profile = user.profile
        return Candidature.objects.filter(candidate=profile)

    @swagger_auto_schema(tags=['Candidatures'])
    def get_object(self):
        try:
            candidature = super().get_object()
            if candidature.candidate.user != self.request.user:
                raise NotFound("Le profil de l'utilisateur n'a pas été trouvé.")
            return candidature
        except Candidature.DoesNotExist:
            raise NotFound("La candidature n'a pas été trouvée.")

class CandidaturesByJobView(generics.ListAPIView):
    serializer_class = CandidatureSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['Candidatures'])
    def get_queryset(self):
        job_id = self.kwargs['job_id']
        return Candidature.objects.filter(job_id=job_id)

class CandidaturesByUserView(generics.ListAPIView):
    serializer_class = CandidatureSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['Candidatures'])
    def get_queryset(self):
        user = self.request.user
        profile = user.profile
        return Candidature.objects.filter(candidate=profile)
