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

    def create(self, validated_data):
        subscription, created = NewsletterSubscription.objects.get_or_create(
            email=validated_data["email"],
            defaults=validated_data,
        )
        if not created:
            subscription.full_name = validated_data.get("full_name", subscription.full_name)
            subscription.source = validated_data.get("source", subscription.source)
            subscription.status = "subscribed"
            subscription.unsubscribed_at = None
            subscription.save()
        return subscription

    def update(self, instance, validated_data):
        previous_status = instance.status
        for field, value in validated_data.items():
            setattr(instance, field, value)
        if previous_status != instance.status and instance.status == "unsubscribed":
            instance.unsubscribed_at = timezone.now()
        instance.save()
        return instance
