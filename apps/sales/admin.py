from django.contrib import admin

from .models import Inquiry, InquiryItem, Quote, QuoteItem


class InquiryItemInline(admin.TabularInline):
    model = InquiryItem
    extra = 0


class QuoteItemInline(admin.TabularInline):
    model = QuoteItem
    extra = 0


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "company_name", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("full_name", "email", "company_name")
    inlines = [InquiryItemInline]


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ("reference", "customer", "status", "total_amount", "created_at")
    list_filter = ("status", "currency")
    search_fields = ("reference", "customer__email")
    inlines = [QuoteItemInline]
