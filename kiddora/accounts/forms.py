from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import CustomUser

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'profile_image', 'phone',
            'address_line1', 'address_line2',
            'city', 'state', 'postal_code', 'country'
        ]

    def clean(self):
        cleaned = super().clean()
        pwd = cleaned.get('password')
        cpwd = cleaned.get('confirm_password')

        if pwd and len(pwd) < 6:
            self.add_error('password', 'Minimum 6 characters required')

        if pwd != cpwd:
            self.add_error('confirm_password', 'Passwords do not match')

        return cleaned


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()


class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6)


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('new_password')
        p2 = cleaned.get('confirm_password')

        if p1 != p2 or len(p1) < 6:
            raise forms.ValidationError("Invalid password")
        return cleaned


class ChangePasswordForm(PasswordChangeForm):
    pass
