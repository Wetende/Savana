from django.core.exceptions import ValidationError
from django.db import models

from apps.core.model_mixins import AutoSlugMixin
from apps.core.models import TimeStampedModel


class Category(AutoSlugMixin, TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        self.ensure_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(AutoSlugMixin, TimeStampedModel):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    short_description = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    origin_country = models.CharField(max_length=100, default="Kenya")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    is_wholesale_available = models.BooleanField(default=True)
    is_retail_available = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        self.ensure_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductVariant(TimeStampedModel):
    UNIT_CHOICES = [
        ("g", "Grams"),
        ("kg", "Kilograms"),
        ("bag", "Bag"),
    ]

    ROAST_CHOICES = [
        ("green", "Green"),
        ("light", "Light"),
        ("medium", "Medium"),
        ("dark", "Dark"),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True)
    packaging_size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    packaging_unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default="kg")
    roast_type = models.CharField(max_length=20, choices=ROAST_CHOICES, default="green")
    retail_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["product__name", "name"]

    def __str__(self):
        return f"{self.product.name} - {self.name}"


class ProductImage(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="images",
        null=True,
        blank=True,
    )
    image = models.ImageField(upload_to="products/")
    alt_text = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"Image for {self.product.name}"


class WholesaleOffer(TimeStampedModel):
    AVAILABILITY_CHOICES = [
        ("available", "Available"),
        ("limited", "Limited"),
        ("sold_out", "Sold Out"),
        ("inquiry", "Inquiry Required"),
    ]

    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="wholesale_offer")
    grade = models.CharField(max_length=100, blank=True)
    minimum_order_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    quantity_unit = models.CharField(max_length=20, default="bag")
    quote_only = models.BooleanField(default=True)
    buyer_notes = models.TextField(blank=True)
    availability_status = models.CharField(
        max_length=20,
        choices=AVAILABILITY_CHOICES,
        default="available",
    )
    lead_time_days = models.PositiveIntegerField(default=7)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Wholesale offer for {self.product.name}"


class InventoryRecord(TimeStampedModel):
    AVAILABILITY_CHOICES = WholesaleOffer.AVAILABILITY_CHOICES

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="inventory_records")
    variant = models.OneToOneField(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="inventory_record",
        null=True,
        blank=True,
    )
    quantity_on_hand = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    reserved_quantity = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    low_stock_threshold = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    availability_status = models.CharField(
        max_length=20,
        choices=AVAILABILITY_CHOICES,
        default="available",
    )

    class Meta:
        ordering = ["product__name", "variant__name", "id"]

    def clean(self):
        if self.variant and self.variant.product_id != self.product_id:
            raise ValidationError("The selected variant must belong to the selected product.")
        if (
            self.variant_id is None
            and InventoryRecord.objects.filter(product=self.product, variant__isnull=True)
            .exclude(pk=self.pk)
            .exists()
        ):
            raise ValidationError("Only one product-level inventory record is allowed per product.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Inventory for {self.variant or self.product}"
