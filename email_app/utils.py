from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def send_email(subject, to_email, template_name, context):
    """
    Fonction utilitaire pour envoyer des emails.

    :param subject: Sujet de l'email
    :param to_email: Adresse email du destinataire
    :param template_name: Nom du template d'email
    :param context: Contexte pour rendre le template
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    html_content = render_to_string(template_name, context)
    email = EmailMultiAlternatives(subject, html_content, from_email, [to_email])
    email.attach_alternative(html_content, "text/html")
    email.send()
