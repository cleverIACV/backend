# email_app/urls.py
from django.urls import path
from .views import SendTestEmailView

urlpatterns = [
    path('send/mail/', SendTestEmailView.as_view(), name='send-test-email'),
]
