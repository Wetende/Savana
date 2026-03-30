from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle

from apps.core.api_mixins import ManagedModelViewSet
from apps.core.permissions import IsStaffUser

from .serializers import NewsletterSubscriptionSerializer
from .selectors import subscription_queryset
from .services import subscribe_or_resubscribe, update_subscription


@extend_schema(tags=["Newsletter"])
class NewsletterSubscriptionViewSet(ManagedModelViewSet):
    queryset = subscription_queryset()
    read_serializer_class = NewsletterSubscriptionSerializer
    write_serializer_class = NewsletterSubscriptionSerializer
    permission_classes = [IsStaffUser]
    permission_classes_by_action = {
        "create": [permissions.AllowAny],
        "list": [IsStaffUser],
        "retrieve": [IsStaffUser],
        "update": [IsStaffUser],
        "partial_update": [IsStaffUser],
        "destroy": [IsStaffUser],
    }
    throttle_classes_by_action = {
        "create": [ScopedRateThrottle],
    }
    throttle_scopes_by_action = {
        "create": "lead-capture",
    }

    def get_queryset(self):
        return subscription_queryset()

    def create(self, request, *args, **kwargs):
        serializer = self.get_write_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subscription = subscribe_or_resubscribe(data=dict(serializer.validated_data))
        return Response(
            self.get_read_serializer(subscription).data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        subscription = self.get_object()
        serializer = self.get_write_serializer(subscription, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        subscription = update_subscription(subscription=subscription, data=dict(serializer.validated_data))
        return Response(self.get_read_serializer(subscription).data)
