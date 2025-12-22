from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, EmailOTP


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = (
        'username', 'email', 'is_staff', 'is_active',
        'is_blocked', 'date_joined'
    )

    list_filter = ('is_staff', 'is_active', 'is_blocked')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    list_per_page = 25

    actions = ['block_users', 'unblock_users']

    fieldsets = UserAdmin.fieldsets + (
        (
            'Additional Info',
            {
                'fields': (
                    'profile_image', 'phone',
                    'address_line1', 'address_line2',
                    'city', 'state', 'postal_code', 'country',
                    'is_blocked'
                )
            },
        ),
    )

    def block_users(self, request, queryset):
        queryset.update(is_blocked=True)

    def unblock_users(self, request, queryset):
        queryset.update(is_blocked=False)

    block_users.short_description = "Block selected users"
    unblock_users.short_description = "Unblock selected users"


@admin.register(EmailOTP)
class EmailOTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp', 'is_verified', 'created_at')
    ordering = ('-created_at',)