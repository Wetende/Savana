from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import GuestQuoteAcceptView, GuestQuoteDetailView, InquiryViewSet, QuoteViewSet

router = DefaultRouter()
router.register("inquiries", InquiryViewSet, basename="sales-inquiry")
router.register("quotes", QuoteViewSet, basename="sales-quote")

urlpatterns = [
    path(
        "guest-quotes/<str:reference>/<uuid:token>/",
        GuestQuoteDetailView.as_view(),
        name="guest-quote-detail",
    ),
    path(
        "guest-quotes/<str:reference>/<uuid:token>/accept/",
        GuestQuoteAcceptView.as_view(),
        name="guest-quote-accept",
    ),
]
urlpatterns += router.urls
