from rest_framework import serializers

from apps.core.emailing import send_system_email

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


class OrderSerializer(serializers.ModelSerializer):
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

    def _sync_items(self, order, items_data):
        order.items.all().delete()
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        order.recalculate_totals()

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        order = Order.objects.create(**validated_data)
        self._sync_items(order, items_data)
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop("items", None)
        previous_status = instance.status
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        if items_data is not None:
            self._sync_items(instance, items_data)
        else:
            instance.recalculate_totals()
        if previous_status != instance.status and instance.customer and instance.customer.email:
            send_system_email(
                subject=f"Order {instance.order_number} updated",
                message=f"Your order is now marked as {instance.status}.",
                recipient_list=[instance.customer.email],
            )
        return instance
