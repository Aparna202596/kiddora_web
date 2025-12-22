from django.shortcuts import render, redirect
from .forms import SignupForm
from django.utils import timezone
from .models import EmailOTP, CustomUser
from .utils import generate_otp, send_otp_email
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

def home(request):
    return render(request, 'accounts/home.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user and not user.is_blocked:
            login(request, user)
            return redirect('accounts:home')
        elif user and user.is_blocked:
            return render(request, 'accounts/login.html', {'error': 'Your account is blocked'})
    return render(request, 'accounts/login.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('accounts:home')
    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            otp = generate_otp()
            EmailOTP.objects.create(user=user, otp=otp)
            send_otp_email(user.email, otp)
            return redirect('accounts:reset_password', user_id=user.id)
        except CustomUser.DoesNotExist:
            return render(request, 'accounts/forgot_password.html', {'error': 'Email not registered'})
    return render(request, 'accounts/forgot_password.html')

def reset_password(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    otp_obj = EmailOTP.objects.filter(user=user).last()
    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if otp_obj.is_expired():
            return render(request, 'accounts/reset_password.html', {'error': 'OTP expired', 'user': user})

        if otp_input != otp_obj.otp:
            return render(request, 'accounts/reset_password.html', {'error': 'Invalid OTP', 'user': user})

        if new_password != confirm_password or len(new_password) < 6:
            return render(request, 'accounts/reset_password.html', {'error': 'Password invalid or mismatch', 'user': user})

        user.set_password(new_password)
        user.save()
        otp_obj.is_verified = True
        otp_obj.save()
        return redirect('accounts:login')
    
    return render(request, 'accounts/reset_password.html', {'user': user})

def verify_otp(request, user_id):
    otp_obj = EmailOTP.objects.filter(user_id=user_id).last()

    if request.method == 'POST':
        otp_input = request.POST.get('otp')

        if otp_obj.is_expired():
            return render(request, 'accounts/otp.html', {'error': 'OTP expired'})

        if otp_input == otp_obj.otp:
            otp_obj.is_verified = True
            otp_obj.save()
            otp_obj.user.is_active = True
            otp_obj.user.save()
            return redirect('accounts:home')

    return render(request, 'accounts/otp.html', {'user': otp_obj.user})

def resend_otp(request, user_id):
    otp = generate_otp()
    user = CustomUser.objects.get(id=user_id)
    EmailOTP.objects.create(user=user, otp=otp)
    send_otp_email(user.email, otp)
    return redirect('accounts:verify_otp', user_id=user_id)
