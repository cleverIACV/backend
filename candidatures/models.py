from django.db import models
from backoffice.models import CustomUser  # Import de l'utilisateur personnalisé si nécessaire
from profiles.models import Profil
from jobs.models import Job

class Candidature(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    candidate = models.ForeignKey(Profil, on_delete=models.CASCADE, related_name='candidatures')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='candidatures')
    submission_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    score = models.FloatField(null=True, blank=True)
    review = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Candidature {self.id} - {self.candidate.user.username} for {self.job.title}"
