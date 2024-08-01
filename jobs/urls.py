from django.urls import path
from .views import JobCreateView, JobListView, RecruiterJobListView, JobDetailView, CategoryListView, ContractTypeListView

urlpatterns = [
    path('jobs/create/', JobCreateView.as_view(), name='job-create'),
    path('jobs/', JobListView.as_view(), name='job-list'),
    path('jobs/recruiter/', RecruiterJobListView.as_view(), name='recruiter-job-list'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job-detail'),

    # List of categories and contract types
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('contract-types/', ContractTypeListView.as_view(), name='contracttype-list'),
]
