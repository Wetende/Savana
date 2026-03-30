from .models import Category, InventoryRecord, Product, ProductVariant, WholesaleOffer


def category_queryset_for_user(user):
    queryset = Category.objects.order_by("name")
    if user.is_staff:
        return queryset
    return queryset.filter(is_active=True)


def product_queryset_for_user(user):
    queryset = Product.objects.select_related("category").prefetch_related(
        "images",
        "variants",
        "wholesale_offer",
    )
    if user.is_staff:
        return queryset
    return queryset.filter(status="published")


def variant_queryset_for_user(user):
    queryset = ProductVariant.objects.select_related("product")
    if user.is_staff:
        return queryset
    return queryset.filter(is_active=True, product__status="published")


def wholesale_offer_queryset_for_user(user):
    queryset = WholesaleOffer.objects.select_related("product").order_by("product__name")
    if user.is_staff:
        return queryset
    return queryset.filter(is_active=True, product__status="published")


def inventory_queryset():
    return InventoryRecord.objects.select_related("product", "variant")
