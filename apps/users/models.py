from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.core.models import TimeStampedModel


class User(AbstractUser):
    ACCOUNT_TYPE_CHOICES = [
        ("customer", "Customer"),
        ("buyer", "Buyer"),
        ("staff", "Staff"),
    ]

    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES, default="customer")
    is_email_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_staff and self.account_type == "customer":
            self.account_type = "staff"
        super().save(*args, **kwargs)


class CustomerProfile(TimeStampedModel):
    CONTACT_METHOD_CHOICES = [
        ("email", "Email"),
        ("phone", "Phone"),
        ("whatsapp", "WhatsApp"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    company_name = models.CharField(max_length=255, blank=True)
    business_type = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=30, blank=True)
    preferred_contact_method = models.CharField(
        max_length=20,
        choices=CONTACT_METHOD_CHOICES,
        default="email",
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Profile for {self.user.username}"
