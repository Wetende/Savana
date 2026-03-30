from django.contrib import admin

from .models import Category, InventoryRecord, Product, ProductImage, ProductVariant, WholesaleOffer


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active")
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "status", "is_wholesale_available", "is_retail_available")
    list_filter = ("status", "is_wholesale_available", "is_retail_available", "category")
    search_fields = ("name", "slug")
    inlines = [ProductVariantInline, ProductImageInline]


@admin.register(WholesaleOffer)
class WholesaleOfferAdmin(admin.ModelAdmin):
    list_display = ("product", "grade", "minimum_order_quantity", "availability_status", "is_active")
    list_filter = ("availability_status", "is_active")


@admin.register(InventoryRecord)
class InventoryRecordAdmin(admin.ModelAdmin):
    list_display = ("product", "variant", "quantity_on_hand", "reserved_quantity", "availability_status")
