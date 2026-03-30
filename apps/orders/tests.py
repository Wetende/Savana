import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.catalog.models import Category, Product

from .models import Order

User = get_user_model()


@pytest.mark.django_db
def test_customer_can_only_see_own_orders():
    customer = User.objects.create_user(username="cust1", password="strongpass123")
    other = User.objects.create_user(username="cust2", password="strongpass123")
    Order.objects.create(customer=customer, status="pending")
    Order.objects.create(customer=other, status="pending")

    client = APIClient()
    client.force_authenticate(user=customer)
    response = client.get("/api/v1/orders/")

    assert response.status_code == 200
    assert len(response.data["results"]) == 1


@pytest.mark.django_db
def test_order_endpoints_support_address_crud_staff_order_crud_and_total_recalculation(
    staff_client,
    customer_client,
    customer_user,
):
    category = Category.objects.create(name="Orders")
    product = Product.objects.create(
        name="Order Coffee",
        category=category,
        description="Order flow",
        status="published",
    )

    address_response = customer_client.post(
        "/api/v1/orders/addresses/",
        {
            "full_name": "Customer User",
            "company_name": "Buyer LLC",
            "email": customer_user.email,
            "line1": "123 Main St",
            "city": "Dallas",
            "state": "TX",
            "postal_code": "75001",
            "country": "US",
        },
        format="json",
    )
    assert address_response.status_code == 201
    address_id = address_response.data["id"]

    assert customer_client.get("/api/v1/orders/addresses/").status_code == 200
    assert customer_client.get(f"/api/v1/orders/addresses/{address_id}/").status_code == 200
    assert customer_client.put(
        f"/api/v1/orders/addresses/{address_id}/",
        {"city": "Austin"},
        format="json",
    ).status_code == 200

    order_response = staff_client.post(
        "/api/v1/orders/",
        {
            "customer": customer_user.id,
            "shipping_address_id": address_id,
            "billing_address_id": address_id,
            "tax_amount": "5.00",
            "shipping_amount": "10.00",
            "discount_amount": "2.00",
            "items": [
                {
                    "product": product.id,
                    "product_name": "Order Coffee",
                    "quantity": "2.00",
                    "unit_price": "50.00",
                }
            ],
        },
        format="json",
    )
    assert order_response.status_code == 201
    order_id = order_response.data["id"]
    assert order_response.data["subtotal_amount"] == "100.00"
    assert order_response.data["total_amount"] == "113.00"

    assert customer_client.get("/api/v1/orders/").status_code == 200
    assert customer_client.get(f"/api/v1/orders/{order_id}/").status_code == 200
    assert staff_client.get(f"/api/v1/orders/{order_id}/").status_code == 200

    update_response = staff_client.put(
        f"/api/v1/orders/{order_id}/",
        {
            "shipping_amount": "15.00",
            "items": [
                {
                    "product": product.id,
                    "product_name": "Order Coffee",
                    "quantity": "3.00",
                    "unit_price": "50.00",
                }
            ],
        },
        format="json",
    )
    assert update_response.status_code == 200
    assert update_response.data["subtotal_amount"] == "150.00"
    assert update_response.data["total_amount"] == "168.00"

    cleanup_order = staff_client.post(
        "/api/v1/orders/",
        {
            "customer": customer_user.id,
            "items": [
                {
                    "product": product.id,
                    "product_name": "Delete Me",
                    "quantity": "1.00",
                    "unit_price": "10.00",
                }
            ],
        },
        format="json",
    )
    assert cleanup_order.status_code == 201
    assert staff_client.delete(f"/api/v1/orders/{cleanup_order.data['id']}/").status_code == 204
    assert customer_client.delete(f"/api/v1/orders/addresses/{address_id}/").status_code == 204
