from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone

from .forms import CustomUserCreationForm
from .models import CustomUser, EmailOTP
from .utils import generate_otp, send_otp_email


def home(request):
    return render(request, 'accounts/home.html')


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            otp = generate_otp()
            EmailOTP.objects.create(user=user, otp=otp)
            send_otp_email(user.email, otp)

            return redirect('accounts:verify_otp', user_id=user.id)
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/signup.html', {'form': form})


def verify_otp(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    otp_obj = EmailOTP.objects.filter(user=user, is_verified=False).last()

    if not otp_obj:
        return redirect('accounts:login')

    if request.method == 'POST':
        otp_input = request.POST.get('otp')

        if otp_obj.is_expired():
            return render(request, 'accounts/otp.html', {'error': 'OTP expired'})

        if otp_input == otp_obj.otp:
            otp_obj.is_verified = True
            otp_obj.save()

            user.is_active = True
            user.save()
            return redirect('accounts:login')

        return render(request, 'accounts/otp.html', {'error': 'Invalid OTP'})

    return render(request, 'accounts/otp.html', {'user': user})


def resend_otp(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    EmailOTP.objects.filter(user=user, is_verified=False).delete()

    otp = generate_otp()
    EmailOTP.objects.create(user=user, otp=otp)
    send_otp_email(user.email, otp)

    return redirect('accounts:verify_otp', user_id=user.id)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_blocked:
                return render(request, 'accounts/login.html', {'error': 'Account blocked'})
            if not user.is_active:
                return render(request, 'accounts/login.html', {'error': 'Verify OTP first'})

            login(request, user)
            return redirect('accounts:home')

        return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('accounts:login')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        user = CustomUser.objects.filter(email=email).first()
        if not user:
            return render(request, 'accounts/forgot_password.html', {'error': 'Invalid email'})

        otp = generate_otp()
        EmailOTP.objects.create(user=user, otp=otp)
        send_otp_email(user.email, otp)

        return redirect('accounts:reset_password', user_id=user.id)

    return render(request, 'accounts/forgot_password.html')


def reset_password(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    otp_obj = EmailOTP.objects.filter(user=user).last()

    if request.method == 'POST':
        otp = request.POST.get('otp')
        password = request.POST.get('new_password')
        confirm = request.POST.get('confirm_password')

        if otp_obj.is_expired():
            return render(request, 'accounts/reset_password.html', {'error': 'OTP expired'})

        if otp != otp_obj.otp:
            return render(request, 'accounts/reset_password.html', {'error': 'Invalid OTP'})

        if password != confirm or len(password) < 6:
            return render(request, 'accounts/reset_password.html', {'error': 'Password invalid'})

        user.set_password(password)
        user.save()
        otp_obj.is_verified = True
        otp_obj.save()

        return redirect('accounts:login')

    return render(request, 'accounts/reset_password.html', {'user': user})
