from django.contrib import admin

from .models import Payment, PaymentAttempt


class PaymentAttemptInline(admin.TabularInline):
    model = PaymentAttempt
    extra = 0


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "provider", "status", "amount", "currency", "customer")
    list_filter = ("provider", "status", "currency")
    inlines = [PaymentAttemptInline]
