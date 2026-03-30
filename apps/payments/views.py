from drf_spectacular.utils import OpenApiParameter, extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework import permissions, response, status
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from apps.core.api_mixins import ManagedModelViewSet
from apps.core.permissions import IsOwnerOrStaff, IsStaffUser

from .models import Payment, PaymentAttempt
from .serializers import PaymentAttemptSerializer, PaymentSerializer
from .selectors import payment_attempt_queryset, payment_queryset_for_user
from .services import (
    create_payment,
    create_payment_attempt,
    handle_webhook_event,
    update_payment,
    update_payment_attempt,
)

payment_webhook_request_serializer = inline_serializer(
    name="PaymentWebhookRequestSerializer",
    fields={
        "event": serializers.CharField(required=False),
        "data": serializers.JSONField(required=False),
    },
)

payment_webhook_response_serializer = inline_serializer(
    name="PaymentWebhookResponseSerializer",
    fields={
        "received": serializers.BooleanField(),
        "provider": serializers.CharField(),
        "payload": serializers.JSONField(),
    },
)


@extend_schema(tags=["Payments"])
class PaymentViewSet(ManagedModelViewSet):
    queryset = Payment.objects.none()
    read_serializer_class = PaymentSerializer
    write_serializer_class = PaymentSerializer
    permission_classes = [IsStaffUser]
    permission_classes_by_action = {
        "list": [permissions.IsAuthenticated, IsOwnerOrStaff],
        "retrieve": [permissions.IsAuthenticated, IsOwnerOrStaff],
        "create": [IsStaffUser],
        "update": [IsStaffUser],
        "partial_update": [IsStaffUser],
        "destroy": [IsStaffUser],
    }

    def get_queryset(self):
        return payment_queryset_for_user(self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = create_payment(data=dict(serializer.validated_data))
        return response.Response(self.get_serializer(payment).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        payment = self.get_object()
        serializer = self.get_serializer(payment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        payment = update_payment(payment=payment, data=dict(serializer.validated_data))
        return response.Response(self.get_serializer(payment).data)


@extend_schema(tags=["Payments"])
class PaymentAttemptViewSet(ManagedModelViewSet):
    queryset = PaymentAttempt.objects.none()
    read_serializer_class = PaymentAttemptSerializer
    write_serializer_class = PaymentAttemptSerializer
    permission_classes = [IsStaffUser]

    def get_queryset(self):
        return payment_attempt_queryset()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        attempt = create_payment_attempt(data=dict(serializer.validated_data))
        return response.Response(self.get_serializer(attempt).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        attempt = self.get_object()
        serializer = self.get_serializer(attempt, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        attempt = update_payment_attempt(attempt=attempt, data=dict(serializer.validated_data))
        return response.Response(self.get_serializer(attempt).data)


class PaymentWebhookStubView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "webhook"

    @extend_schema(
        tags=["Payments"],
        parameters=[
            OpenApiParameter(
                name="provider",
                location=OpenApiParameter.PATH,
                required=True,
                type=str,
            )
        ],
        request=payment_webhook_request_serializer,
        responses={202: payment_webhook_response_serializer},
    )
    def post(self, request, provider):
        return response.Response(handle_webhook_event(provider=provider, payload=request.data), status=status.HTTP_202_ACCEPTED)
