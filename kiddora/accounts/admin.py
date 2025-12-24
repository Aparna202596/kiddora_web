from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = (
        'username', 'email', 'is_staff', 'is_active',
        'is_blocked', 'date_joined'
    )

    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'is_blocked')
    ordering = ('-date_joined',)
    list_per_page = 25
    readonly_fields = ('date_joined',)

    fieldsets = UserAdmin.fieldsets + (
        ('Profile Details', {
            'fields': (
                'profile_image', 'phone',
                'address_line1', 'address_line2',
                'city', 'state', 'postal_code',
                'country', 'is_blocked'
            )
        }),
    )

    actions = ['block_users', 'unblock_users']

    def block_users(self, request, queryset):
        count = queryset.update(is_blocked=True)
        self.message_user(request, f"{count} users blocked")

    def unblock_users(self, request, queryset):
        count = queryset.update(is_blocked=False)
        self.message_user(request, f"{count} users unblocked")
