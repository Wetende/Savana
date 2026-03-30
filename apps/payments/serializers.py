from rest_framework import serializers

from .models import Payment, PaymentAttempt


class PaymentAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentAttempt
        fields = [
            "id",
            "payment",
            "attempt_number",
            "status",
            "idempotency_key",
            "external_transaction_id",
            "request_payload",
            "response_payload",
            "error_message",
        ]


class PaymentSerializer(serializers.ModelSerializer):
    attempts = PaymentAttemptSerializer(many=True, read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "customer",
            "order",
            "quote",
            "provider",
            "status",
            "currency",
            "amount",
            "external_reference",
            "metadata",
            "paid_at",
            "attempts",
            "created_at",
        ]
        read_only_fields = ["created_at"]
