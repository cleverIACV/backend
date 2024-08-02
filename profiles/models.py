from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from backoffice.models import CustomUser
from datetime import date
from django.core.exceptions import ValidationError

# Age validator : Si l'âge est inférieur à 18 ans, renvoyer une erreur
def validate_age(value):
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 18:
        raise ValidationError("L'utilisateur doit avoir au moins 18 ans.")

# Validator : Si la date de disponibilité est antérieure à la date d'aujourd'hui, renvoyer une erreur
def validate_availability(value):
    if value < date.today():
        raise ValidationError("La disponibilité ne peut pas être antérieure à la date d'aujourd'hui.")

class Profil(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profil')
    image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    date_of_birth = models.DateField(validators=[validate_age])

    street = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    name_company = models.CharField(max_length=255)
    phone_company = models.CharField(max_length=20)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    cover_letter = models.FileField(upload_to='cover_letters/', blank=True, null=True)
    extracted_data = models.JSONField(default=dict, blank=True, null=True)
    final_analyse_cv_data = models.TextField()
    job_title = models.CharField(max_length=255)
    description = models.TextField()
    degree_level = models.CharField(max_length=255)
    availability = models.DateField(validators=[validate_availability])
    

    def __str__(self):
        return (
            f"User ID: {self.user.id}, "
            f"Phone: {self.phone}, "
            f"Street: {self.street}, "
            f"Postal Code: {self.postal_code}, "
            f"City: {self.city}, "
            f"State: {self.state}, "
            f"Country: {self.country}, "
            f"Company Name: {self.name_company}, "
            f"Company Phone: {self.phone_company}, "
            f"Resume: {self.resume}, "
            f"Cover Letter: {self.cover_letter}, "
            f"Job Title: {self.job_title}, "
            f"Description: {self.description}, "
            f"Degree Level: {self.degree_level}, "
            f"Availability: {self.availability}"
        )
