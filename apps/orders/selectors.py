from .models import Address, Order


def address_queryset_for_user(user):
    queryset = Address.objects.select_related("customer").order_by("-created_at")
    if user.is_staff:
        return queryset
    return queryset.filter(customer=user)


def order_queryset_for_user(user):
    queryset = Order.objects.select_related(
        "customer",
        "quote",
        "billing_address",
        "shipping_address",
    ).prefetch_related("items")
    if user.is_staff:
        return queryset
    return queryset.filter(customer=user)
