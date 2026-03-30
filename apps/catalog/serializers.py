from rest_framework import serializers

from .models import Category, InventoryRecord, Product, ProductImage, ProductVariant, WholesaleOffer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "is_active"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "alt_text", "is_primary", "sort_order"]


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "product",
            "name",
            "sku",
            "packaging_size",
            "packaging_unit",
            "roast_type",
            "retail_price",
            "is_active",
        ]


class WholesaleOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = WholesaleOffer
        fields = [
            "id",
            "product",
            "grade",
            "minimum_order_quantity",
            "quantity_unit",
            "quote_only",
            "buyer_notes",
            "availability_status",
            "lead_time_days",
            "is_active",
        ]


class InventoryRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryRecord
        fields = [
            "id",
            "product",
            "variant",
            "quantity_on_hand",
            "reserved_quantity",
            "low_stock_threshold",
            "availability_status",
        ]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        source="category",
        queryset=Category.objects.all(),
        write_only=True,
    )
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    wholesale_offer = WholesaleOfferSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "category",
            "category_id",
            "short_description",
            "description",
            "origin_country",
            "status",
            "is_wholesale_available",
            "is_retail_available",
            "images",
            "variants",
            "wholesale_offer",
        ]
