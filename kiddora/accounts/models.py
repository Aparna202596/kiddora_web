from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid

class CustomUser(AbstractUser):

    ROLE_ADMIN = 'admin'
    ROLE_CUSTOMER = 'customer'

    ROLE_CHOICES = (
        (ROLE_ADMIN, 'Admin'),
        (ROLE_CUSTOMER, 'Customer'),)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_CUSTOMER, db_index=True)
    email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)
    USERNAME_FIELD = 'username'   # change to 'email' if required
    REQUIRED_FIELDS = ['email', 'full_name']

    def __str__(self):
        return f"{self.username} ({self.role})"

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_customer(self):
        return self.role == self.ROLE_CUSTOMER

# User Addresses
ADDRESS_TYPE_CHOICES = (
    ('home', 'Home'),
    ('office', 'Office'),
    ('other', 'Other'),
)
class UserAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPE_CHOICES, default='home')
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.address_line1}, {self.city}"
