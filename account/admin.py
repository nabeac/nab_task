from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User 

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Extra Info", {"fields": ("phone", "body")}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Extra Info", {"fields": ("phone", "body")}),
    )

    list_display = ("username", "email", "phone", "is_staff")
