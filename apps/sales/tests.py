import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.catalog.models import Category, Product
from apps.orders.models import Order
from apps.sales.models import Inquiry, Quote

User = get_user_model()


@pytest.mark.django_db
def test_guest_inquiry_creation():
    category = Category.objects.create(name="Wholesale")
    product = Product.objects.create(
        name="Kenya AA",
        category=category,
        description="Top grade",
        status="published",
    )

    client = APIClient()
    response = client.post(
        "/api/v1/sales/inquiries/",
        {
            "full_name": "Jane Buyer",
            "email": "jane@example.com",
            "company_name": "Buyer Co",
            "items": [
                {
                    "product": product.id,
                    "requested_quantity": "10",
                    "quantity_unit": "bag",
                }
            ],
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.data["full_name"] == "Jane Buyer"


@pytest.mark.django_db
def test_staff_can_convert_accepted_quote_to_order():
    staff = User.objects.create_user(username="staff", password="strongpass123", is_staff=True)
    buyer = User.objects.create_user(username="buyer2", password="strongpass123")
    category = Category.objects.create(name="Bulk Coffee")
    product = Product.objects.create(
        name="Kenya AB",
        category=category,
        description="Export ready",
        status="published",
    )

    client = APIClient()
    client.force_authenticate(user=staff)
    quote_response = client.post(
        "/api/v1/sales/quotes/",
        {
            "customer": buyer.id,
            "status": "accepted",
            "items": [
                {
                    "product": product.id,
                    "product_name": "Kenya AB",
                    "quantity": "5",
                    "unit_price": "120.00",
                }
            ],
        },
        format="json",
    )
    assert quote_response.status_code == 201

    convert_response = client.post(
        f"/api/v1/sales/quotes/{quote_response.data['id']}/convert_to_order/",
        {},
        format="json",
    )
    assert convert_response.status_code == 201
    assert Order.objects.filter(quote_id=quote_response.data["id"]).exists()


@pytest.mark.django_db
def test_sales_endpoints_cover_guest_quote_access_and_staff_management(staff_client):
    category = Category.objects.create(name="Guest Wholesale")
    product = Product.objects.create(
        name="Guest Kenya PB",
        category=category,
        description="Guest quote flow",
        status="published",
    )

    guest_client = APIClient()
    inquiry_response = guest_client.post(
        "/api/v1/sales/inquiries/",
        {
            "full_name": "Guest Buyer",
            "email": "guestbuyer@example.com",
            "company_name": "Guest Distributors",
            "message": "Need a quote",
            "items": [{"product": product.id, "requested_quantity": "15.00"}],
        },
        format="json",
    )
    assert inquiry_response.status_code == 201
    inquiry_id = inquiry_response.data["id"]

    assert staff_client.get("/api/v1/sales/inquiries/").status_code == 200
    assert staff_client.get(f"/api/v1/sales/inquiries/{inquiry_id}/").status_code == 200
    assert staff_client.patch(
        f"/api/v1/sales/inquiries/{inquiry_id}/",
        {"message": "Reviewed by sales"},
        format="json",
    ).status_code == 200

    quote_response = staff_client.post(
        "/api/v1/sales/quotes/",
        {
            "inquiry": inquiry_id,
            "status": "sent",
            "shipping_amount": "20.00",
            "items": [
                {
                    "product": product.id,
                    "product_name": "Guest Kenya PB",
                    "quantity": "15.00",
                    "unit_price": "140.00",
                }
            ],
        },
        format="json",
    )
    assert quote_response.status_code == 201
    quote_id = quote_response.data["id"]
    reference = quote_response.data["reference"]
    token = quote_response.data["guest_access_token"]

    assert staff_client.get("/api/v1/sales/quotes/").status_code == 200
    assert staff_client.get(f"/api/v1/sales/quotes/{quote_id}/").status_code == 200
    assert staff_client.patch(
        f"/api/v1/sales/quotes/{quote_id}/",
        {"notes": "Updated note"},
        format="json",
    ).status_code == 200

    guest_detail = guest_client.get(f"/api/v1/sales/guest-quotes/{reference}/{token}/")
    assert guest_detail.status_code == 200

    guest_accept = guest_client.post(f"/api/v1/sales/guest-quotes/{reference}/{token}/accept/", {}, format="json")
    assert guest_accept.status_code == 200
    assert guest_accept.data["status"] == "accepted"

    convert_response = staff_client.post(
        f"/api/v1/sales/quotes/{quote_id}/convert_to_order/",
        {},
        format="json",
    )
    assert convert_response.status_code == 201

    cleanup_quote = staff_client.post(
        "/api/v1/sales/quotes/",
        {
            "status": "draft",
            "items": [
                {
                    "product": product.id,
                    "product_name": "Draft Quote",
                    "quantity": "1.00",
                    "unit_price": "10.00",
                }
            ],
        },
        format="json",
    )
    assert cleanup_quote.status_code == 201
    assert staff_client.delete(f"/api/v1/sales/quotes/{cleanup_quote.data['id']}/").status_code == 204

    cleanup_inquiry = guest_client.post(
        "/api/v1/sales/inquiries/",
        {
            "full_name": "Delete Inquiry",
            "email": "delete@example.com",
        },
        format="json",
    )
    assert cleanup_inquiry.status_code == 201
    assert staff_client.delete(f"/api/v1/sales/inquiries/{cleanup_inquiry.data['id']}/").status_code == 204
