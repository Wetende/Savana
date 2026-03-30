from django.db import models
from django.utils import timezone

from apps.core.models import TimeStampedModel


class NewsletterSubscription(TimeStampedModel):
    STATUS_CHOICES = [
        ("subscribed", "Subscribed"),
        ("unsubscribed", "Unsubscribed"),
    ]

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="subscribed")
    source = models.CharField(max_length=100, blank=True)
    subscribed_at = models.DateTimeField(default=timezone.now)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.email
