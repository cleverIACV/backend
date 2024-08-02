from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Candidature
from .serializers import CandidatureSerializer
from drf_yasg.utils import swagger_auto_schema
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
        
        serializer.save(candidate=profile)

    @swagger_auto_schema(tags=['Candidatures'])
    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        # Créer la candidature
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Retourner la réponse avec toutes les données
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_success_headers(self, data):
        try:
            return {'Location': str(data['url'])}
        except (TypeError, KeyError):
            return {}



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
