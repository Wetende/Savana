from .models import NewsletterSubscription


def subscription_queryset():
    return NewsletterSubscription.objects.order_by("-created_at")
