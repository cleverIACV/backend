from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from backoffice.models import CustomUser

# Create your models here.

class Profil(models.Model):
    name_company = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    phone_company = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    address_company = models.CharField(max_length=255)
    resume = models.DecimalField(max_digits=10, decimal_places=2)
    cover_letter = models.DecimalField(max_digits=10, decimal_places=2)
    speciality = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    degree_level = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.id} {{self.name_company}} {{self.phone}} {{self.phone_company}} {{self.address}} {{self.address_company}} {{self.resume}} {{self.cover_letter}} {{self.speciality}} {{self.description}} {{self.degree_level}} {{self.start_date}} [{self.end_date}]"


