from django.urls import path
from .views import (
    CandidatureListCreateView, 
    CandidatureRetrieveUpdateDestroyView, 
    CandidaturesByJobView, 
    CandidaturesByUserView
)

urlpatterns = [
    path('candidatures/', CandidatureListCreateView.as_view(), name='candidature-list-create'),
    path('candidatures/<int:pk>/', CandidatureRetrieveUpdateDestroyView.as_view(), name='candidature-detail'),
    path('candidatures/job/<int:job_id>/', CandidaturesByJobView.as_view(), name='candidatures-by-job'),
    path('candidatures/user/', CandidaturesByUserView.as_view(), name='candidatures-by-user'),
]
