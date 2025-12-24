from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('home/', views.home_page, name='home'),
    path('signup/', views.signup_page, name='signup'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('otp/verify/<int:user_id>/', views.verify_otp, name='verify_otp'),
    path('otp/resend/<int:user_id>/', views.resend_otp, name='resend_otp'),
    path('change-password/', views.change_password, name='change_password'),
    path('password/forgot/', views.forgot_password, name='forgot_password'),
    path('password/reset/<int:user_id>/', views.reset_password, name='reset_password'),

    path('admin/users/', views.admin_page, name='admin_page'),
    path('admin/users/add/', views.admin_add, name='admin_add'),
    path('admin/users/edit/<int:id>/', views.admin_edit, name='admin_edit'),
    path('admin/users/delete/<int:id>/', views.admin_delete, name='admin_delete'),
    path('admin/users/toggle/<int:id>/', views.toggle_block, name='toggle_block'),
]

