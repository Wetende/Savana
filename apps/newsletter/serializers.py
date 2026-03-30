from django.utils import timezone
from rest_framework import serializers

from .models import NewsletterSubscription


class NewsletterSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscription
        fields = [
            "id",
            "email",
            "full_name",
            "status",
            "source",
            "subscribed_at",
            "unsubscribed_at",
        ]
        read_only_fields = ["subscribed_at", "unsubscribed_at"]
