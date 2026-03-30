from decimal import Decimal

from rest_framework import serializers

from django.contrib.auth import get_user_model

from .models import Inquiry, InquiryItem, Quote, QuoteItem

User = get_user_model()


class InquiryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InquiryItem
        fields = [
            "id",
            "product",
            "variant",
            "requested_quantity",
            "quantity_unit",
            "notes",
        ]


class InquiryReadSerializer(serializers.ModelSerializer):
    items = InquiryItemSerializer(many=True, required=False)

    class Meta:
        model = Inquiry
        fields = [
            "id",
            "customer",
            "full_name",
            "email",
            "phone_number",
            "company_name",
            "business_type",
            "message",
            "status",
            "source",
            "items",
            "created_at",
        ]
        read_only_fields = ["customer", "status", "created_at"]

class InquiryWriteSerializer(serializers.ModelSerializer):
    items = InquiryItemSerializer(many=True, required=False)

    class Meta:
        model = Inquiry
        fields = [
            "customer",
            "full_name",
            "email",
            "phone_number",
            "company_name",
            "business_type",
            "message",
            "status",
            "source",
            "items",
        ]
        extra_kwargs = {
            "customer": {"queryset": User.objects.all(), "required": False, "allow_null": True},
            "status": {"required": False},
        }


class QuoteItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuoteItem
        fields = [
            "id",
            "product",
            "variant",
            "product_name",
            "sku",
            "quantity",
            "unit_price",
            "line_total",
            "notes",
        ]
        read_only_fields = ["line_total"]


class QuoteReadSerializer(serializers.ModelSerializer):
    items = QuoteItemSerializer(many=True, required=False)

    class Meta:
        model = Quote
        fields = [
            "id",
            "guest_access_token",
            "reference",
            "inquiry",
            "customer",
            "status",
            "currency",
            "subtotal_amount",
            "tax_amount",
            "shipping_amount",
            "discount_amount",
            "total_amount",
            "notes",
            "expires_at",
            "accepted_at",
            "rejected_at",
            "items",
            "created_at",
        ]
        read_only_fields = ["guest_access_token", "reference", "accepted_at", "rejected_at", "created_at"]

class QuoteWriteSerializer(serializers.ModelSerializer):
    items = QuoteItemSerializer(many=True, required=False)

    class Meta:
        model = Quote
        fields = [
            "inquiry",
            "customer",
            "status",
            "currency",
            "subtotal_amount",
            "tax_amount",
            "shipping_amount",
            "discount_amount",
            "total_amount",
            "notes",
            "expires_at",
            "items",
        ]
        extra_kwargs = {
            "customer": {"queryset": User.objects.all(), "required": False, "allow_null": True},
            "inquiry": {"required": False, "allow_null": True},
            "status": {"required": False},
            "subtotal_amount": {"required": False},
            "tax_amount": {"required": False},
            "shipping_amount": {"required": False},
            "discount_amount": {"required": False},
            "total_amount": {"required": False},
            "currency": {"required": False},
            "notes": {"required": False},
            "expires_at": {"required": False, "allow_null": True},
        }


class QuoteAcceptSerializer(serializers.Serializer):
    accepted = serializers.BooleanField(default=True)
