from django.db import transaction

from .models import Payment, PaymentAttempt


@transaction.atomic
def create_payment(*, data):
    return Payment.objects.create(**data)


@transaction.atomic
def update_payment(*, payment, data):
    for field, value in data.items():
        setattr(payment, field, value)
    payment.save()
    return payment


@transaction.atomic
def create_payment_attempt(*, data):
    return PaymentAttempt.objects.create(**data)


@transaction.atomic
def update_payment_attempt(*, attempt, data):
    for field, value in data.items():
        setattr(attempt, field, value)
    attempt.save()
    return attempt


def handle_webhook_event(*, provider, payload):
    return {
        "received": True,
        "provider": provider,
        "payload": payload,
    }
