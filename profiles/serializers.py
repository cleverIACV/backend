from rest_framework import serializers
from .models import Profil

class ProfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profil
        fields = '__all__'

    def create(self, validated_data):
        profile = Profil.objects.create(**validated_data)
        return profile

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.street = validated_data.get('street', instance.street)
        instance.postal_code = validated_data.get('postal_code', instance.postal_code)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)
        instance.country = validated_data.get('country', instance.country)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.name_company = validated_data.get('name_company', instance.name_company)
        instance.phone_company = validated_data.get('phone_company', instance.phone_company)
        instance.resume = validated_data.get('resume', instance.resume)
        instance.cover_letter = validated_data.get('cover_letter', instance.cover_letter)
        instance.job_title = validated_data.get('job_title', instance.job_title)
        instance.description = validated_data.get('description', instance.description)
        instance.degree_level = validated_data.get('degree_level', instance.degree_level)
        instance.availability = validated_data.get('availability', instance.availability)
        
        instance.save()
        return instance
