from rest_framework import serializers

from .models import ProductReview


class ProductReviewSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer.username", read_only=True)

    class Meta:
        model = ProductReview
        fields = [
            "id",
            "product",
            "customer",
            "customer_name",
            "rating",
            "title",
            "body",
            "status",
            "approved_by",
            "approved_at",
            "created_at",
        ]
        read_only_fields = ["customer", "status", "approved_by", "approved_at", "created_at"]
