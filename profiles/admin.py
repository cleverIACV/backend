from django.contrib import admin
from .models import Profil

@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'date_of_birth', 'phone', 'city', 'country', 'job_title', 'extracted_data', 'final_analyse_cv_data')
    search_fields = ('user__email', 'user__username', 'phone', 'city', 'country', 'job_title')
    list_filter = ('gender', 'city', 'country', 'job_title')
