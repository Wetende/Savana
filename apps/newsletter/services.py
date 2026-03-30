from django.db import transaction
from django.utils import timezone

from .models import NewsletterSubscription


@transaction.atomic
def subscribe_or_resubscribe(*, data):
    subscription, created = NewsletterSubscription.objects.get_or_create(
        email=data["email"],
        defaults=data,
    )
    if created:
        return subscription

    subscription.full_name = data.get("full_name", subscription.full_name)
    subscription.source = data.get("source", subscription.source)
    subscription.status = "subscribed"
    subscription.unsubscribed_at = None
    subscription.save(
        update_fields=[
            "full_name",
            "source",
            "status",
            "unsubscribed_at",
        ]
    )
    return subscription


@transaction.atomic
def update_subscription(*, subscription, data):
    previous_status = subscription.status
    for field, value in data.items():
        setattr(subscription, field, value)
    if previous_status != subscription.status and subscription.status == "unsubscribed":
        subscription.unsubscribed_at = timezone.now()
    subscription.save()
    return subscription
