import pytest
from django.utils import timezone

from .models import NewsletterSubscription
from .services import subscribe_or_resubscribe


@pytest.mark.django_db
def test_newsletter_resubscribe_service_reactivates_existing_contact():
    subscription = NewsletterSubscription.objects.create(
        email="revive@example.com",
        full_name="Old Name",
        status="unsubscribed",
        unsubscribed_at=timezone.now(),
    )

    updated = subscribe_or_resubscribe(
        data={
            "email": "revive@example.com",
            "full_name": "New Name",
            "source": "service-test",
        }
    )

    assert updated.pk == subscription.pk
    assert updated.status == "subscribed"
    assert updated.full_name == "New Name"
    assert updated.unsubscribed_at is None
