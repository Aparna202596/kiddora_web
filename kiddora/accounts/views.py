from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import CustomUser, EmailOTP
from .forms import (
    SignupForm, LoginForm, ForgotPasswordForm,
    OTPForm, ResetPasswordForm, ChangePasswordForm
)

# ---------------- SIGNUP ----------------
def signup_page(request):
    form = SignupForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.is_active = False
        user.save()

        EmailOTP.objects.create(user=user)
        return redirect('accounts:verify_otp', user.id)

    return render(request, 'accounts/signup.html', {'form': form})


# ---------------- LOGIN ----------------
def login_page(request):
    form = LoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = authenticate(**form.cleaned_data)
        if user:
            login(request, user)
            return redirect('accounts:home')
        messages.error(request, 'Invalid credentials')

    return render(request, 'accounts/login.html', {'form': form})


# ---------------- OTP VERIFY ----------------
def verify_otp(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    otp_obj = EmailOTP.objects.filter(user=user, is_verified=False).first()

    if not otp_obj or otp_obj.is_expired():
        return redirect('accounts:login')

    form = OTPForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        if form.cleaned_data['otp'] == otp_obj.otp:
            otp_obj.is_verified = True
            otp_obj.save()
            user.is_active = True
            user.save()
            return redirect('accounts:login')
        messages.error(request, 'Invalid OTP')

    return render(request, 'accounts/otp.html', {'form': form})

def resend_otp(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    # Invalidate previous OTPs
    EmailOTP.objects.filter(user=user, is_verified=False).update(is_verified=True)

    # Create new OTP
    EmailOTP.objects.create(user=user)

    messages.success(request, "A new OTP has been sent to your email.")
    return redirect('accounts:verify_otp', user.id)
# ---------------- FORGOT PASSWORD ----------------
def forgot_password(request):
    form = ForgotPasswordForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = CustomUser.objects.filter(
            email=form.cleaned_data['email'], is_active=True
        ).first()

        if user:
            EmailOTP.objects.create(user=user)
            return redirect('accounts:reset_password', user.id)

        messages.error(request, 'User not found')

    return render(request, 'accounts/forgot_password.html', {'form': form})


# ---------------- RESET PASSWORD ----------------
def reset_password(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    otp_obj = EmailOTP.objects.filter(user=user, is_verified=False).first()

    if not otp_obj or otp_obj.is_expired():
        return redirect('accounts:login')

    form = ResetPasswordForm(request.POST or None)
    otp_form = OTPForm(request.POST or None)

    if request.method == 'POST' and form.is_valid() and otp_form.is_valid():
        if otp_form.cleaned_data['otp'] != otp_obj.otp:
            messages.error(request, 'Invalid OTP')
        else:
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            otp_obj.is_verified = True
            otp_obj.save()
            return redirect('accounts:login')

    return render(request, 'accounts/reset_password.html', {
        'form': form, 'otp_form': otp_form
    })


# ---------------- CHANGE PASSWORD ----------------
@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "Password changed successfully.")
            return redirect('accounts:home')
    else:
        form = ChangePasswordForm(user=request.user)

    return render(request, 'accounts/change_password.html', {'form': form})

@login_required
def home_page(request):
    return render(request, 'accounts/home.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:login')


@login_required
def admin_page(request):
    if not request.user.is_staff:
        return redirect('accounts:home')

    users = CustomUser.objects.all()
    return render(request, 'accounts/admin_page.html', {'users': users})

@login_required
def admin_add(request):
    if not request.user.is_staff:
        return redirect('accounts:home')

    form = SignupForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.is_active = True
        user.save()
        messages.success(request, 'User added successfully')
        return redirect('accounts:admin_page')

    return render(request, 'accounts/admin_add.html', {'form': form})

@login_required
def admin_edit(request, id):
    if not request.user.is_staff:
        return redirect('accounts:home')

    user = get_object_or_404(CustomUser, id=id)
    form = SignupForm(request.POST or None, request.FILES or None, instance=user)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'User updated successfully')
        return redirect('accounts:admin_page')

    return render(request, 'accounts/admin_edit.html', {'form': form, 'user': user})
@login_required
def admin_delete(request, id):
    if not request.user.is_staff:
        return redirect('accounts:home')

    user = get_object_or_404(CustomUser, id=id)
    user.delete()
    messages.success(request, 'User deleted successfully')
    return redirect('accounts:admin_page')
@login_required
def toggle_block(request, id):
    if not request.user.is_staff:
        return redirect('accounts:home')

    user = get_object_or_404(CustomUser, id=id)
    user.is_blocked = not user.is_blocked
    user.save()
    status = 'blocked' if user.is_blocked else 'unblocked'
    messages.success(request, f'User {status} successfully')
    return redirect('accounts:admin_page')


