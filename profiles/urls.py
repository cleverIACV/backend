from django.urls import path
from .views import CreateProfilesView, UserAuthProfileView, UpdateProfileView, DeleteProfilesView, UploadResumeView, UploadCoverLetterView

urlpatterns = [
    path('profil/', UserAuthProfileView.as_view(), name='profil'),
    path('profil/create', CreateProfilesView.as_view(), name='create-profil'),
    path('profil/update/', UpdateProfileView.as_view(), name='update-profil'),
    path('profil/delete/', DeleteProfilesView.as_view(), name='delete-profil'),
    path('profil/upload_resume/', UploadResumeView.as_view(), name='upload-resume'),
    path('profil/upload_cover_letter/', UploadCoverLetterView.as_view(), name='upload-cover-letter'),
]
