from decimal import Decimal

from django.conf import settings
from django.db import models

from apps.core.model_mixins import ReferenceCodeMixin
from apps.core.models import TimeStampedModel


class Address(TimeStampedModel):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="addresses",
        null=True,
        blank=True,
    )
    full_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=30, blank=True)
    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=2, default="US")

    def __str__(self):
        return f"{self.full_name} - {self.city}"


class Order(ReferenceCodeMixin, TimeStampedModel):
    reference_prefix = "ORD"
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("fulfilled", "Fulfilled"),
        ("cancelled", "Cancelled"),
    ]
    PAYMENT_STATUS_CHOICES = [
        ("unpaid", "Unpaid"),
        ("authorized", "Authorized"),
        ("paid", "Paid"),
        ("refunded", "Refunded"),
        ("failed", "Failed"),
    ]

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="orders",
        null=True,
        blank=True,
    )
    quote = models.OneToOneField(
        "sales.Quote",
        on_delete=models.SET_NULL,
        related_name="order",
        null=True,
        blank=True,
    )
    order_number = models.CharField(max_length=40, unique=True, blank=True)
    billing_address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        related_name="billing_orders",
        null=True,
        blank=True,
    )
    shipping_address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        related_name="shipping_orders",
        null=True,
        blank=True,
    )
    currency = models.CharField(max_length=10, default="USD")
    subtotal_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    shipping_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    shipping_method = models.CharField(max_length=100, blank=True)
    shipping_quote_reference = models.CharField(max_length=100, blank=True)
    tracking_number = models.CharField(max_length=100, blank=True)
    tracking_url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default="unpaid")
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.ensure_reference_code("order_number"):
            super().save(update_fields=["order_number"])

    def recalculate_totals(self, save=True):
        subtotal = sum((item.line_total for item in self.items.all()), Decimal("0.00"))
        self.subtotal_amount = subtotal
        self.total_amount = (
            subtotal
            + Decimal(self.tax_amount)
            + Decimal(self.shipping_amount)
            - Decimal(self.discount_amount)
        )
        if save:
            self.save(update_fields=["subtotal_amount", "total_amount"])
        return self.total_amount

    def __str__(self):
        return self.order_number or f"Order {self.pk}"


class OrderItem(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        "catalog.Product",
        on_delete=models.SET_NULL,
        related_name="order_items",
        null=True,
        blank=True,
    )
    variant = models.ForeignKey(
        "catalog.ProductVariant",
        on_delete=models.SET_NULL,
        related_name="order_items",
        null=True,
        blank=True,
    )
    product_name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, blank=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=2, default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    line_total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    def save(self, *args, **kwargs):
        self.line_total = Decimal(self.quantity) * Decimal(self.unit_price)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_name} ({self.order.order_number})"
