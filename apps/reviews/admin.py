from django.contrib import admin

from .models import ProductReview


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "customer", "rating", "status", "created_at")
    list_filter = ("status", "rating")
    search_fields = ("product__name", "customer__username", "title")
