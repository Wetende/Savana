from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomerProfile, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Commerce",
            {
                "fields": ("account_type", "is_email_verified"),
            },
        ),
    )
    list_display = ("username", "email", "account_type", "is_staff", "is_active")
    list_filter = ("account_type", "is_staff", "is_active", "is_email_verified")


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "company_name", "business_type", "preferred_contact_method")
    search_fields = ("user__username", "user__email", "company_name")
