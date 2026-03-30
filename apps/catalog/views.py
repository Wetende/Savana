from rest_framework import viewsets

from apps.core.permissions import IsStaffOrReadOnly, IsStaffUser

from .models import Category, InventoryRecord, Product, ProductVariant, WholesaleOffer
from .serializers import (
    CategorySerializer,
    InventoryRecordSerializer,
    ProductSerializer,
    ProductVariantSerializer,
    WholesaleOfferSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(is_active=True)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("category").prefetch_related("images", "variants", "wholesale_offer")
    serializer_class = ProductSerializer
    permission_classes = [IsStaffOrReadOnly]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(status="published")


class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.select_related("product")
    serializer_class = ProductVariantSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(is_active=True, product__status="published")


class WholesaleOfferViewSet(viewsets.ModelViewSet):
    queryset = WholesaleOffer.objects.select_related("product").order_by("product__name")
    serializer_class = WholesaleOfferSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(is_active=True, product__status="published")


class InventoryRecordViewSet(viewsets.ModelViewSet):
    queryset = InventoryRecord.objects.select_related("product", "variant")
    serializer_class = InventoryRecordSerializer
    permission_classes = [IsStaffUser]
