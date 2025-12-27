from django.contrib import admin
from .models import CustomUser, UserAddress

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'email_verified')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email', 'phone')
    ordering = ('-date_joined',)


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'state', 'country', 'is_default')
    list_filter = ('city', 'state', 'country')

