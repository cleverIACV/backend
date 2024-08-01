from rest_framework import generics, permissions
from .models import Job, Category, ContractType
from .serializers import JobSerializer, CategorySerializer, ContractTypeSerializer
from .permissions import IsRecruiter
from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(tags=['Jobs'])
class JobCreateView(generics.CreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)

@swagger_auto_schema(tags=['Jobs'])
class JobListView(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

@swagger_auto_schema(tags=['Jobs'])
class RecruiterJobListView(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]

    def get_queryset(self):
        return Job.objects.filter(posted_by=self.request.user)

@swagger_auto_schema(tags=['Jobs'])
class JobDetailView(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

@swagger_auto_schema(tags=['Categories'])
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

@swagger_auto_schema(tags=['Contract Types'])
class ContractTypeListView(generics.ListAPIView):
    queryset = ContractType.objects.all()
    serializer_class = ContractTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
