from django.conf import settings
from django.core.mail import EmailMessage


def notify_new_message(message, recipient):
    """Prévient par e-mail à chaque nouveau message de contact (n'échoue jamais)."""
    if not recipient:
        return
    nom = " ".join(message.name.split())  # supprime tout retour à la ligne
    EmailMessage(
        subject=f"Portfolio : nouveau message de {nom}",
        body=f"De : {nom} <{message.email}>\n\n{message.message}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient],
        reply_to=[message.email],
    ).send(fail_silently=True)
