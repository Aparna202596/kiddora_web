import random
from django.core.mail import send_mail
from django.conf import settings


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(email, otp):
    send_mail(
        subject='Kiddora OTP Verification',
        message=f'Your OTP is {otp}. Valid for 5 minutes.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )

def send_welcome_email(email, username):
    send_mail(
        subject='Welcome to Kiddora!',
        message=f'Hello {username}, welcome to Kiddora! We are excited to have you on board.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )