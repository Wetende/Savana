from decimal import Decimal

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from .models import Inquiry, InquiryItem, Quote, QuoteItem
from .notifications import notify_inquiry_received, notify_quote_accepted, notify_quote_sent


def _quote_total(quote, subtotal):
    return (
        subtotal
        + Decimal(quote.tax_amount)
        + Decimal(quote.shipping_amount)
        - Decimal(quote.discount_amount)
    )


def _sync_quote_items(quote, items_data):
    quote.items.all().delete()
    subtotal = Decimal("0.00")
    for item_data in items_data:
        item = QuoteItem.objects.create(quote=quote, **item_data)
        subtotal += item.line_total
    quote.subtotal_amount = subtotal
    quote.total_amount = _quote_total(quote, subtotal)
    quote.save(
        update_fields=[
            "subtotal_amount",
            "total_amount",
            "tax_amount",
            "shipping_amount",
            "discount_amount",
        ]
    )


@transaction.atomic
def create_inquiry(*, actor, data):
    items_data = data.pop("items", [])
    explicit_customer = data.pop("customer", None)
    customer = explicit_customer if actor and actor.is_staff else None
    if actor and actor.is_authenticated and not actor.is_staff:
        customer = actor
    inquiry = Inquiry.objects.create(customer=customer, **data)
    InquiryItem.objects.bulk_create(
        InquiryItem(inquiry=inquiry, **item_data) for item_data in items_data
    )
    transaction.on_commit(lambda: notify_inquiry_received(inquiry))
    return inquiry


@transaction.atomic
def create_quote(*, data):
    items_data = data.pop("items", [])
    inquiry = data.get("inquiry")
    if data.get("customer") is None and inquiry and inquiry.customer_id:
        data["customer"] = inquiry.customer

    quote = Quote.objects.create(**data)
    _sync_quote_items(quote, items_data)
    if quote.status == "sent":
        transaction.on_commit(lambda: notify_quote_sent(quote))
    return quote


@transaction.atomic
def update_quote(*, quote, data):
    items_data = data.pop("items", None)
    previous_status = quote.status
    for field, value in data.items():
        setattr(quote, field, value)
    quote.save()

    if items_data is not None:
        _sync_quote_items(quote, items_data)
    else:
        quote.total_amount = _quote_total(quote, quote.subtotal_amount)
        quote.save(update_fields=["total_amount"])

    if previous_status != quote.status and quote.status == "sent":
        transaction.on_commit(lambda: notify_quote_sent(quote))
    return quote


@transaction.atomic
def accept_quote(*, quote):
    if quote.status in {"accepted", "converted"}:
        return quote

    quote.status = "accepted"
    quote.accepted_at = timezone.now()
    quote.save(update_fields=["status", "accepted_at"])
    transaction.on_commit(lambda: notify_quote_accepted(quote))
    return quote


def assert_quote_can_convert_to_order(quote):
    if quote.status != "accepted":
        raise serializers.ValidationError("Only accepted quotes can be converted to orders.")
