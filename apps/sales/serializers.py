from decimal import Decimal

from django.utils import timezone
from rest_framework import serializers

from apps.core.emailing import send_system_email
from apps.orders.models import Order, OrderItem

from .models import Inquiry, InquiryItem, Quote, QuoteItem


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


class InquirySerializer(serializers.ModelSerializer):
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

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        request = self.context.get("request")
        customer = request.user if request and request.user.is_authenticated else None
        inquiry = Inquiry.objects.create(customer=customer, **validated_data)
        InquiryItem.objects.bulk_create(
            [InquiryItem(inquiry=inquiry, **item_data) for item_data in items_data]
        )
        send_system_email(
            subject="Wholesale inquiry received",
            message=f"Thanks {inquiry.full_name}, we received your inquiry.",
            recipient_list=[inquiry.email],
        )
        return inquiry


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


class QuoteSerializer(serializers.ModelSerializer):
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

    def _sync_items(self, quote, items_data):
        quote.items.all().delete()
        total = Decimal("0.00")
        for item_data in items_data:
            item = QuoteItem.objects.create(quote=quote, **item_data)
            total += item.line_total
        quote.subtotal_amount = total
        quote.total_amount = total + quote.tax_amount + quote.shipping_amount - quote.discount_amount
        quote.save(
            update_fields=[
                "subtotal_amount",
                "total_amount",
                "tax_amount",
                "shipping_amount",
                "discount_amount",
            ]
        )

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        inquiry = validated_data.get("inquiry")
        if validated_data.get("customer") is None and inquiry and inquiry.customer_id:
            validated_data["customer"] = inquiry.customer
        quote = Quote.objects.create(**validated_data)
        self._sync_items(quote, items_data)
        if quote.status == "sent":
            email = quote.customer.email if quote.customer else getattr(quote.inquiry, "email", None)
            if email:
                send_system_email(
                    subject=f"Quote {quote.reference} sent",
                    message=f"Your quote {quote.reference} is ready.",
                    recipient_list=[email],
                )
        return quote

    def update(self, instance, validated_data):
        items_data = validated_data.pop("items", None)
        previous_status = instance.status
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        if items_data is not None:
            self._sync_items(instance, items_data)
        if previous_status != instance.status and instance.status == "sent":
            email = instance.customer.email if instance.customer else getattr(instance.inquiry, "email", None)
            if email:
                send_system_email(
                    subject=f"Quote {instance.reference} sent",
                    message=f"Your quote {instance.reference} is ready.",
                    recipient_list=[email],
                )
        return instance


class QuoteAcceptSerializer(serializers.Serializer):
    accepted = serializers.BooleanField(default=True)


def create_order_from_quote(quote: Quote) -> Order:
    if quote.status != "accepted":
        raise serializers.ValidationError("Only accepted quotes can be converted to orders.")
    order, created = Order.objects.get_or_create(
        quote=quote,
        defaults={
            "customer": quote.customer,
            "currency": quote.currency,
            "subtotal_amount": quote.subtotal_amount,
            "tax_amount": quote.tax_amount,
            "shipping_amount": quote.shipping_amount,
            "discount_amount": quote.discount_amount,
            "total_amount": quote.total_amount,
            "notes": quote.notes,
            "status": "pending",
        },
    )
    if created:
        OrderItem.objects.bulk_create(
            [
                OrderItem(
                    order=order,
                    product=item.product,
                    variant=item.variant,
                    product_name=item.product_name,
                    sku=item.sku,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    line_total=item.line_total,
                )
                for item in quote.items.all()
            ]
        )
        order.recalculate_totals()
        quote.status = "converted"
        quote.save(update_fields=["status"])
    return order
