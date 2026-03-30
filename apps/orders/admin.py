from django.contrib import admin

from .models import Address, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("full_name", "company_name", "city", "country")
    search_fields = ("full_name", "company_name", "email")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "customer", "status", "payment_status", "total_amount")
    list_filter = ("status", "payment_status", "currency")
    search_fields = ("order_number", "customer__email")
    inlines = [OrderItemInline]
