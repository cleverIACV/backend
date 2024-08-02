from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Candidature
from .serializers import CandidatureSerializer
from drf_yasg.utils import swagger_auto_schema
from ia_ner_nlp.cv_extraction import CVExtractor
from profiles.models import Profil 

class CandidatureListCreateView(generics.ListCreateAPIView):
    queryset = Candidature.objects.all()
    serializer_class = CandidatureSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['Candidatures'])
    def perform_create(self, serializer):
        user = self.request.user
        try:
            profile = Profil.objects.get(user=user)
        except Profil.DoesNotExist:
            raise NotFound("Le profil de l'utilisateur n'a pas été trouvé.")

        # Extraire les données du CV du profil
        cv_file_path = profile.resume.path  # Assurez-vous que le chemin du fichier CV est correct
        extracted_data = CVExtractor.extract_cv_data(cv_file_path)
        
        serializer.save(candidate=profile, extracted_data=extracted_data)

class CandidatureRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidature.objects.all()
    serializer_class = CandidatureSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['Candidatures'])
    def get_queryset(self):
        user = self.request.user
        try:
            profile = Profil.objects.get(user=user)
        except Profil.DoesNotExist:
            raise NotFound("Le profil de l'utilisateur n'a pas été trouvé.")
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
        try:
            profile = Profil.objects.get(user=user)
        except Profil.DoesNotExist:
            raise NotFound("Le profil de l'utilisateur n'a pas été trouvé.")
        return Candidature.objects.filter(candidate=profile)
