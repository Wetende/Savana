from .models import Payment, PaymentAttempt


def payment_queryset_for_user(user):
    queryset = Payment.objects.select_related("customer", "order", "quote").prefetch_related("attempts")
    if user.is_staff:
        return queryset
    return queryset.filter(customer=user)


def payment_attempt_queryset():
    return PaymentAttempt.objects.select_related("payment")
