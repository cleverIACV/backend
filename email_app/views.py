from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import send_email

class SendTestEmailView(APIView):
    """
    Vue pour envoyer un email de test.
    """
    def get(self, request, *args, **kwargs):
        subject = 'Test Email'
        to_email = 'jose.tetevi@gmail.com'  # Remplacez par l'email du destinataire
        context = {
            'user': {'first_name': 'Test User'},
            'message': 'This is a test email sent from Django.',
            'subject': subject,
        }
        send_email(subject, to_email, 'email_app/default_email.html', context)
        return Response({'detail': 'Test email sent successfully'})
