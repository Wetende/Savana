from rest_framework import serializers

from .models import Address, Order, OrderItem


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id",
            "full_name",
            "company_name",
            "email",
            "phone_number",
            "line1",
            "line2",
            "city",
            "state",
            "postal_code",
            "country",
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "variant",
            "product_name",
            "sku",
            "quantity",
            "unit_price",
            "line_total",
        ]
        read_only_fields = ["line_total"]


class OrderReadSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, required=False)
    billing_address = AddressSerializer(read_only=True)
    shipping_address = AddressSerializer(read_only=True)
    billing_address_id = serializers.PrimaryKeyRelatedField(
        source="billing_address",
        queryset=Address.objects.all(),
        write_only=True,
        allow_null=True,
        required=False,
    )
    shipping_address_id = serializers.PrimaryKeyRelatedField(
        source="shipping_address",
        queryset=Address.objects.all(),
        write_only=True,
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "customer",
            "quote",
            "billing_address",
            "shipping_address",
            "billing_address_id",
            "shipping_address_id",
            "currency",
            "subtotal_amount",
            "tax_amount",
            "shipping_amount",
            "discount_amount",
            "total_amount",
            "shipping_method",
            "shipping_quote_reference",
            "tracking_number",
            "tracking_url",
            "status",
            "payment_status",
            "notes",
            "items",
            "created_at",
        ]
        read_only_fields = ["order_number", "created_at"]

class OrderWriteSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, required=False)
    billing_address_id = serializers.PrimaryKeyRelatedField(
        source="billing_address",
        queryset=Address.objects.all(),
        write_only=True,
        allow_null=True,
        required=False,
    )
    shipping_address_id = serializers.PrimaryKeyRelatedField(
        source="shipping_address",
        queryset=Address.objects.all(),
        write_only=True,
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Order
        fields = [
            "customer",
            "quote",
            "billing_address_id",
            "shipping_address_id",
            "currency",
            "subtotal_amount",
            "tax_amount",
            "shipping_amount",
            "discount_amount",
            "total_amount",
            "shipping_method",
            "shipping_quote_reference",
            "tracking_number",
            "tracking_url",
            "status",
            "payment_status",
            "notes",
            "items",
        ]
        extra_kwargs = {
            "customer": {"required": False, "allow_null": True},
            "quote": {"required": False, "allow_null": True},
            "currency": {"required": False},
            "subtotal_amount": {"required": False},
            "tax_amount": {"required": False},
            "shipping_amount": {"required": False},
            "discount_amount": {"required": False},
            "total_amount": {"required": False},
            "shipping_method": {"required": False},
            "shipping_quote_reference": {"required": False},
            "tracking_number": {"required": False},
            "tracking_url": {"required": False},
            "status": {"required": False},
            "payment_status": {"required": False},
            "notes": {"required": False},
        }
