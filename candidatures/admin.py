from django.contrib import admin
from .models import Candidature

@admin.register(Candidature)
class CandidatureAdmin(admin.ModelAdmin):
    list_display = ('id', 'candidate', 'job', 'submission_date', 'status', 'score')
    search_fields = ('candidate__user__username', 'job__title')
    list_filter = ('status', 'submission_date')
