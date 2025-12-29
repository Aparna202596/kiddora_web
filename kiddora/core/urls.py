from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.notlogged_home, name='anonymous_user_home'),
    path('about-us/', views.aboutus_view, name='about_us'),
    path('contact-us/', views.contactus_view, name='contact_us'),
    path('privacy-policy/', views.privacy_policy_view, name='privacy_policy'),
    path('terms-conditions/', views.terms_conditions_view, name='terms_conditions'),
    path('return-policy/', views.return_policy_view, name='return_policy'),
    path('cookie-policy/', views.cookie_policy_view, name='cookie_policy'),
    path('blog/', views.blog_view, name='blog'),
    
    path('home/', views.home, name='home'),
    path('admin/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin/users/', views.user_management_view, name='admin_user_management'),
    path('admin/users/toggle/<int:user_id>/', views.block_unblock_user_view, name='block_unblock_user_view'),
    
]