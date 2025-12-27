from django.urls import path
from . import views

urlpatterns = [
    path('admin/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin/users/', views.user_management_view, name='admin_user_management'),
    path('admin/users/toggle/<int:user_id>/', views.block_unblock_user_view, name='block_unblock_user_view'),
    
]