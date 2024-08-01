from rest_framework import serializers
from .models import Candidature

class CandidatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidature
        fields = ['id', 'candidate', 'job', 'submission_date', 'status', 'score', 'review']
        read_only_fields = ['id', 'submission_date']
