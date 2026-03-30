from rest_framework import serializers

from .models import CustomerProfile
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = [
            "company_name",
            "business_type",
            "phone_number",
            "preferred_contact_method",
            "notes",
        ]


class UserSerializer(serializers.ModelSerializer):
    profile = CustomerProfileSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "account_type",
            "is_email_verified",
            "profile",
        ]
        read_only_fields = ["id", "account_type", "is_email_verified"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    profile = CustomerProfileSerializer(required=False)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "profile",
        ]


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    profile = CustomerProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "profile"]
