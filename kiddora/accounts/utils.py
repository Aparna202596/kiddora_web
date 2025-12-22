import random
from django.core.mail import send_mail

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp):
    send_mail(
        subject='Your Kiddora OTP',
        message=f'Your OTP is {otp}. Valid for 5 minutes.',
        from_email=None,  # will use DEFAULT_FROM_EMAIL from settings.py
        recipient_list=[email],
    )