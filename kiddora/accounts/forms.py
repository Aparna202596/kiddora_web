# accounts/forms.py
from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = CustomUser
        fields = [
            'username', 
            'email', 
            'profile_image', 
            'phone', 
            'address_line1', 
            'address_line2',
            'city',
            'state',
            'postal_code',
            'country',
            'password'
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and len(password) < 6:
            self.add_error('password', 'Password must be at least 6 characters long.')

        if password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        help_text="",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    profile_image = forms.ImageField(required=False)
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Phone number'})
    )
    address_line1 = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Address line 1'})
    )
    address_line2 = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Address line 2'})
    )
    city = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'City'})
    )
    state = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'State'})
    )
    postal_code = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Postal Code'})
    )
    country = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Country'})
    )

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'profile_image', 'phone', 'address_line1',
            'address_line2', 'city', 'state', 'postal_code', 'country',
            'password1', 'password2'
        ]