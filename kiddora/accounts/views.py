from django.shortcuts import render,redirect, get_object_or_404
from core.decorators import user_login_required
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount
from django.contrib import messages
from django.contrib.auth import get_user_model,login,authenticate,update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from .models import UserAddress,CustomUser
from .utils import generate_otp
User = get_user_model()

# Signup View, with basic validation
# user creation, and OTP/email verification trigger
def signup_view(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
# Basic validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('accounts:signup')
# Check for existing username/email/phone
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('accounts:signup')
# Check for existing username
        if phone and User.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already exists")
            return redirect('accounts:signup')
# Create user
        otp = generate_otp()
        user = User.objects.create(
            username=username,
            full_name=full_name,
            email=email,
            phone=phone,
            password=make_password(password),
            is_active=False,
            email_verified=False,
            otp=otp,
            otp_created_at=timezone.now())
# Send verification email with OTP
        send_mail(
            subject="Your OTP for Kiddora Signup",
            message=f"Hi {full_name},\n\nYour OTP for email verification is: {otp} valid for 10 minutes.\n\nThank you for signing up!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False)
        request.session['otp_user_id'] = user.id
        messages.success(request, "Account created. Please verify your email.")
        return redirect('accounts:login')
    return render(request, 'accounts/signup.html')

# Login View, with email/username and password
def login_view(request):
    if request.method == "POST":
        identifier = request.POST.get('identifier')  # username or email
        password = request.POST.get('password')
# Allow login via email or username
        user = User.objects.filter(email=identifier).first() or \
            User.objects.filter(username=identifier).first()
        if user is None:
            messages.error(request, "Invalid credentials")
            return redirect('accounts:login')
        user = authenticate(request, username=user.username, password=password)
        if user is None:
            messages.error(request, "Invalid credentials")
            return redirect('accounts:login')
        if not user.email_verified:
            messages.error(request, "Please verify your email before login")
            return redirect('accounts:login')
        login(request, user)  # SESSION CREATED
        return redirect('core:home_view')
    return render(request, 'accounts/login.html')

# Social Login Callback View, to handle post-login actions, user creation if needed
def social_login_callback(request):
    social_account = SocialAccount.objects.filter(user=request.user).first()
    if not social_account:
        messages.error(request, "Social login failed.")
        return redirect('accounts:login')
    email = social_account.extra_data.get('email')
    full_name = social_account.extra_data.get('name')
    user = User.objects.filter(email=email).first()      # Check if user exists
    if not user:
        user = User.objects.create_user(       # Create a new user if doesn't exist
            username=email.split('@')[0],
            email=email,
            full_name=full_name,
            is_active=True,
            email_verified=True)  # Mark as verified since social login is trusted
    login(request, user)   # Log the user in
    messages.success(request, f"Welcome, {user.full_name}!")
    return redirect('products:home')

# OTP Verification View, for verifying email after signup
def verify_otp_view(request):
    user_id = request.session.get('otp_user_id')
    if not user_id:
        messages.error(request, "No OTP verification pending")
        return redirect('accounts:signup')
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        if user.otp != entered_otp: 
            messages.error(request, "Invalid OTP")
            return redirect('accounts:verify_otp')
        if timezone.now() > user.otp_created_at + timedelta(minutes=10): #
            messages.error(request, "OTP expired. Please resend OTP.")
            return redirect('accounts:verify_otp')
    # OTP is valid
        user.is_active = True
        user.email_verified = True
        user.otp = None
        user.otp_created_at = None
        user.save()
        messages.success(request, "Email verified successfully. You can now login.")
        return redirect('accounts:login')
    return render(request, 'accounts/verify_otp.html')

# Forgot Password View, to initiate password reset via OTP
def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            messages.error(request, "No active account found with this email.")
            return redirect('accounts:forget_password')
        # Generate OTP
        otp = generate_otp()
        # Store OTP + email in session
        request.session['reset_otp'] = otp
        request.session['reset_email'] = email
        # Send OTP email
        send_mail(
            subject='Kiddora Password Reset OTP',
            message=f'Your password reset OTP is {otp}. It is valid for a short time.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False)
        messages.success(request, "OTP has been sent to your email.")
        return redirect('accounts:reset_password')
    return render(request, 'accounts/forget_password.html')

# Reset Password View, to reset password after OTP verification
def reset_password_view(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        session_otp = request.session.get('reset_otp')
        email = request.session.get('reset_email')
        if not session_otp or not email:
            messages.error(request, "Session expired. Please try again.")
            return redirect('accounts:forget_password')
        if entered_otp != session_otp:
            messages.error(request, "Invalid OTP.")
            return redirect('accounts:reset_password')
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('accounts:reset_password')
        if len(new_password) < 6:
            messages.error(request, "Password must be at least 6 characters.")
            return redirect('accounts:reset_password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('accounts:forget_password')
# Set new password
        user.password = make_password(new_password)
        user.save()
# Clear session
        del request.session['reset_otp']
        del request.session['reset_email']
        messages.success(request, "Password reset successful. Please login.")
        return redirect('accounts:login')
    return render(request, 'accounts/reset_password.html')

@user_login_required
def change_password_view(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('accounts:change_password')

        user = authenticate(username=request.user.username, password=current_password)
        if not user:
            messages.error(request, 'Current password is incorrect')
            return redirect('accounts:change_password')

        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)

        messages.success(request, 'Password updated successfully')
        return redirect('accounts:profile')

    return render(request, 'accounts/change_password.html')

# Resend OTP View, for resending OTP if expired or lost
def resend_otp_view(request):
    user_id = request.session.get('otp_user_id')
    if not user_id:
        messages.error(request, "No OTP verification pending")
        return redirect('accounts:signup')
    user = User.objects.get(id=user_id)
# Check if last OTP was sent less than 1 minute ago
    if user.otp_created_at and timezone.now() < user.otp_created_at + timedelta(seconds=60):
        messages.error(request, "Please wait before requesting a new OTP.")
        return redirect('accounts:verify_otp')
    # Generate new OTP
    otp = generate_otp()
    user.otp = otp
    user.otp_created_at = timezone.now()
    user.save()
    # Send OTP via email
    send_mail(
        subject="Your new OTP for Kiddora Signup",
        message=f"Hello {user.full_name}, your new OTP is {otp}. It is valid for 10 minutes.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False)
    messages.success(request, "A new OTP has been sent to your email.")
    return redirect('accounts:verify_otp')

@user_login_required
def profile_view(request):
    user = request.user
    addresses = UserAddress.objects.filter(user=user).order_by('-is_default')
    return render(request, 'admin_profile/profile.html', {
        'user_obj': user,
        'addresses': addresses
    })

@user_login_required
def edit_profile_view(request):
    user = request.user
    if request.method == 'POST':
        user.full_name = request.POST.get('full_name')
        user.phone = request.POST.get('phone')
        if 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']
        user.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('accounts:profile')
    return render(request, 'admin_profile/profile_edit.html', {'user_obj': user})

@user_login_required
def add_address_view(request):
    if request.method == 'POST':
        UserAddress.objects.create(
            user=request.user,
            address_line1=request.POST['address_line1'],
            city=request.POST['city'],
            state=request.POST['state'],
            country=request.POST['country'],
            pincode=request.POST['pincode'],
            address_type=request.POST['address_type']
        )
        messages.success(request, 'Address added')
        return redirect('accounts:profile')

    return render(request, 'accounts/add_address.html')

@user_login_required
def edit_address_view(request, address_id):
    address = get_object_or_404(UserAddress, id=address_id, user=request.user)

    if request.method == 'POST':
        address.address_line1 = request.POST['address_line1']
        address.city = request.POST['city']
        address.state = request.POST['state']
        address.country = request.POST['country']
        address.pincode = request.POST['pincode']
        address.save()
        messages.success(request, 'Address updated')
        return redirect('accounts:profile')

    return render(request, 'accounts/edit_address.html', {'address': address})

@user_login_required
def delete_address_view(request, address_id):
    address = get_object_or_404(UserAddress, id=address_id, user=request.user)
    address.delete()
    messages.success(request, 'Address deleted')
    return redirect('accounts:profile')

@user_login_required
def set_default_view(request, address_id):
    UserAddress.objects.filter(user=request.user).update(is_default=False)
    UserAddress.objects.filter(id=address_id, user=request.user).update(is_default=True)
    return redirect('accounts:profile')

# Blocked User View, for users who are blocked
def blocked_user_view(request):
    return render(request, 'blocked.html')

