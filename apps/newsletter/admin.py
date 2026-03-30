from django.contrib import admin

from .models import NewsletterSubscription


@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("email", "status", "source", "subscribed_at")
    list_filter = ("status", "source")
    search_fields = ("email", "full_name")
