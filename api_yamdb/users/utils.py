import random as r

from django.contrib.auth import get_user_model
from django.core.mail import send_mail

User = get_user_model()


def send_confirmation_code(user):
    """Generates confirmation code and sends it to user's email."""
    code = r.randint(1000, 9999)
    send_mail(
        'Your confirmation code for yamdb signup',
        f'Confirmation code: {code}',
        'no-reply@gmail.com',
        [user.email],
        fail_silently=False
    )
    user.confirmation_code = code
    user.save()
