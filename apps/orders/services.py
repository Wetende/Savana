from django.db import transaction
from rest_framework import serializers

from .models import Order, OrderItem
from .notifications import notify_order_status_updated


def _sync_order_items(order, items_data):
    order.items.all().delete()
    for item_data in items_data:
        OrderItem.objects.create(order=order, **item_data)
    order.recalculate_totals()


@transaction.atomic
def create_order(*, data):
    items_data = data.pop("items", [])
    order = Order.objects.create(**data)
    _sync_order_items(order, items_data)
    return order


@transaction.atomic
def update_order(*, order, data):
    items_data = data.pop("items", None)
    previous_status = order.status
    for field, value in data.items():
        setattr(order, field, value)
    order.save()
    if items_data is not None:
        _sync_order_items(order, items_data)
    else:
        order.recalculate_totals()
    if previous_status != order.status:
        transaction.on_commit(lambda: notify_order_status_updated(order))
    return order


@transaction.atomic
def create_order_from_quote(*, quote):
    if quote.status == "converted" and hasattr(quote, "order"):
        return quote.order
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
        )
        order.recalculate_totals()
        quote.status = "converted"
        quote.save(update_fields=["status"])
    order.refresh_from_db()
    return order
