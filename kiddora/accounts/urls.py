from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('blocked/', views.blocked_user_view, name='blocked'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('resend-otp/', views.resend_otp_view, name='resend_otp'), 
    path('social-login/callback/', views.social_login_callback, name='social_login_callback'),

    path('forgot-password/', views.forgot_password_view, name='forget_password'),
    path('reset-password/', views.reset_password_view, name='reset_password'),
    path('change-password/', views.change_password_view, name='change_password'),

    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    
    path('address/add/', views.add_address_view, name='add_address'),
    path('address/edit/<int:address_id>/', views.edit_address_view, name='edit_address'),
    path('address/delete/<int:address_id>/', views.delete_address_view, name='delete_address'),
    path('address/default/<int:address_id>/', views.set_default_view, name='set_default_address'),



]

