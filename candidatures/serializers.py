from rest_framework import serializers
from .models import Candidature

class CandidatureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Candidature
        fields = ['id', 'submission_date', 'status', 'score', 'review', 'extracted_data']
        read_only_fields = ['id', 'submission_date']
