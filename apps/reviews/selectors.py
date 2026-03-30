from .models import ProductReview


def review_queryset_for_user(user):
    queryset = ProductReview.objects.select_related("product", "customer", "approved_by")
    if user.is_staff:
        return queryset
    return queryset.filter(status="approved")
