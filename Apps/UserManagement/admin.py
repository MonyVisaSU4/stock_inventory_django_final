from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from Apps.UserManagement.models import User


# Register your models here.
@admin.register(User)
class CustomUser(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'phone_number', 'address', 'profile_picture', 'date_of_birth')
        }),
    )