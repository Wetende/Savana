from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import GuestQuoteView, InquiryViewSet, QuoteViewSet

router = DefaultRouter()
router.register("inquiries", InquiryViewSet, basename="sales-inquiry")
router.register("quotes", QuoteViewSet, basename="sales-quote")

urlpatterns = [
    path(
        "guest-quotes/<str:reference>/<uuid:token>/",
        GuestQuoteView.as_view(),
        name="guest-quote-detail",
    ),
]
urlpatterns += router.urls
