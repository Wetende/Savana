import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.orders.models import Order
from .models import Payment

User = get_user_model()


@pytest.mark.django_db
def test_payment_status_choices_support_core_lifecycle():
    payment = Payment.objects.create(amount="99.00", status="pending")
    payment.status = "succeeded"
    payment.save()

    payment.refresh_from_db()
    assert payment.status == "succeeded"


@pytest.mark.django_db
def test_payment_endpoints_cover_payments_attempts_and_webhook(staff_client, customer_client, customer_user):
    order = Order.objects.create(customer=customer_user, status="pending", total_amount="250.00")

    create_payment = staff_client.post(
        "/api/v1/payments/",
        {
            "customer": customer_user.id,
            "order": order.id,
            "provider": "manual",
            "status": "pending",
            "currency": "USD",
            "amount": "250.00",
        },
        format="json",
    )
    assert create_payment.status_code == 201
    payment_id = create_payment.data["id"]

    assert staff_client.get("/api/v1/payments/").status_code == 200
    assert customer_client.get("/api/v1/payments/").status_code == 200
    assert staff_client.get(f"/api/v1/payments/{payment_id}/").status_code == 200

    patch_payment = staff_client.patch(
        f"/api/v1/payments/{payment_id}/",
        {"status": "processing"},
        format="json",
    )
    assert patch_payment.status_code == 200

    create_attempt = staff_client.post(
        "/api/v1/payments/attempts/",
        {
            "payment": payment_id,
            "attempt_number": 1,
            "status": "pending",
            "idempotency_key": "attempt-1",
        },
        format="json",
    )
    assert create_attempt.status_code == 201
    attempt_id = create_attempt.data["id"]

    assert staff_client.get("/api/v1/payments/attempts/").status_code == 200
    assert staff_client.get(f"/api/v1/payments/attempts/{attempt_id}/").status_code == 200
    assert staff_client.patch(
        f"/api/v1/payments/attempts/{attempt_id}/",
        {"status": "succeeded"},
        format="json",
    ).status_code == 200

    webhook_client = APIClient()
    webhook_response = webhook_client.post(
        "/api/v1/payments/webhooks/stripe/",
        {"event": "payment.succeeded"},
        format="json",
    )
    assert webhook_response.status_code == 202

    assert staff_client.delete(f"/api/v1/payments/attempts/{attempt_id}/").status_code == 204
    assert staff_client.delete(f"/api/v1/payments/{payment_id}/").status_code == 204
