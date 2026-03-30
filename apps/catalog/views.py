from drf_spectacular.utils import extend_schema
from apps.core.api_mixins import ManagedModelViewSet
from apps.core.permissions import IsStaffOrReadOnly, IsStaffUser

from .models import Category, InventoryRecord, Product, ProductVariant, WholesaleOffer
from .selectors import (
    category_queryset_for_user,
    inventory_queryset,
    product_queryset_for_user,
    variant_queryset_for_user,
    wholesale_offer_queryset_for_user,
)
from .serializers import (
    CategorySerializer,
    InventoryRecordSerializer,
    ProductSerializer,
    ProductVariantSerializer,
    WholesaleOfferSerializer,
)


@extend_schema(tags=["Catalog"])
class CategoryViewSet(ManagedModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        return category_queryset_for_user(self.request.user)


@extend_schema(tags=["Catalog"])
class ProductViewSet(ManagedModelViewSet):
    queryset = Product.objects.select_related("category").prefetch_related("images", "variants", "wholesale_offer")
    serializer_class = ProductSerializer
    permission_classes = [IsStaffOrReadOnly]
    lookup_field = "slug"

    def get_queryset(self):
        return product_queryset_for_user(self.request.user)


@extend_schema(tags=["Catalog"])
class ProductVariantViewSet(ManagedModelViewSet):
    queryset = ProductVariant.objects.select_related("product")
    serializer_class = ProductVariantSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        return variant_queryset_for_user(self.request.user)


@extend_schema(tags=["Catalog"])
class WholesaleOfferViewSet(ManagedModelViewSet):
    queryset = WholesaleOffer.objects.select_related("product").order_by("product__name")
    serializer_class = WholesaleOfferSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        return wholesale_offer_queryset_for_user(self.request.user)


@extend_schema(tags=["Catalog"])
class InventoryRecordViewSet(ManagedModelViewSet):
    queryset = InventoryRecord.objects.select_related("product", "variant")
    serializer_class = InventoryRecordSerializer
    permission_classes = [IsStaffUser]

    def get_queryset(self):
        return inventory_queryset()
