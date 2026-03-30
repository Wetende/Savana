from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import PaymentAttemptViewSet, PaymentViewSet, PaymentWebhookStubView

router = DefaultRouter()
router.register("attempts", PaymentAttemptViewSet, basename="payments-attempt")
router.register("", PaymentViewSet, basename="payments-payment")

urlpatterns = [
    path("webhooks/<str:provider>/", PaymentWebhookStubView.as_view(), name="payment-webhook"),
]
urlpatterns += router.urls
