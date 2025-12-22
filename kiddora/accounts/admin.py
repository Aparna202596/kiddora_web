from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Display
    list_display = (
        'username',
        'email',
        'is_staff',
        'is_active',
        'is_blocked',
        'date_joined',
    )

    # Search
    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
    )

    # Filters
    list_filter = (
        'is_staff',
        'is_active',
        'is_blocked',
        'date_joined',
    )

    # Sorting
    ordering = ('-date_joined',)

    # Pagination
    list_per_page = 25

    # Bulk actions
    actions = ['block_users', 'unblock_users']

    # Custom fields in admin edit page
    fieldsets = UserAdmin.fieldsets + (
        (
            'Profile Details',
            {
                'fields': (
                    'profile_image',
                    'phone',
                    'address_line1',
                    'address_line2',
                    'city',
                    'state',
                    'postal_code',
                    'country',
                    'is_blocked',
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
