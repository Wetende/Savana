from django.shortcuts import get_object_or_404

from .models import Inquiry, Quote


def inquiry_queryset_for_user(user):
    queryset = Inquiry.objects.prefetch_related("items").select_related("customer")
    if user.is_staff:
        return queryset
    return queryset.filter(customer=user)


def quote_queryset_for_user(user):
    queryset = Quote.objects.prefetch_related("items").select_related("customer", "inquiry")
    if user.is_staff:
        return queryset
    return queryset.filter(customer=user)


def get_guest_quote(reference, token):
    queryset = Quote.objects.prefetch_related("items").select_related("customer", "inquiry")
    return get_object_or_404(
        queryset,
        reference=reference,
        guest_access_token=token,
    )
