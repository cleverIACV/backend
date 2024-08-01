from django.db import models
from backoffice.models import CustomUser

class Category(models.Model):
    name = models.CharField(max_length=255)

class ContractType(models.Model):
    name = models.CharField(max_length=255)

class Job(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    contract_type = models.ForeignKey(ContractType, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    company_name= models.CharField(max_length=255)
    requirements = models.TextField()
    location = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    posted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
