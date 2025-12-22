from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, EmailOTP

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'is_staff', 'is_active', 'is_blocked','date_joined')
    list_filter = ('is_staff', 'is_active', 'is_blocked','date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    actions = ['block_users', 'unblock_users']

    def block_users(self, request, queryset):
        queryset.update(is_blocked=True)
    block_users.short_description = "Block selected users"

    def unblock_users(self, request, queryset):
        queryset.update(is_blocked=False)
    unblock_users.short_description = "Unblock selected users"
    #fieldsets = UserAdmin.fieldsets + (
    #    (None, {'fields': ('profile_image', 'phone', 'address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country', 'is_blocked')}),
    # )

#admin.site.register(CustomUser, CustomUserAdmin)
#admin.site.register(EmailOTP)
#@admin.register(EmailOTP)