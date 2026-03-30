import pytest
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_healthcheck_endpoint():
    client = APIClient()
    response = client.get("/api/v1/health/")

    assert response.status_code == 200
    assert response.data["status"] == "ok"


@pytest.mark.django_db
def test_root_endpoint_returns_backend_index():
    client = APIClient()
    response = client.get("/")

    assert response.status_code == 200
    assert response.data["status"] == "running"
    assert "api_root" in response.data["links"]
    assert "swagger" in response.data["links"]


@pytest.mark.django_db
def test_swagger_and_schema_endpoints_are_available():
    client = APIClient()

    schema_response = client.get("/api/schema/")
    assert schema_response.status_code == 200

    docs_short_response = client.get("/docs")
    assert docs_short_response.status_code == 200

    swagger_response = client.get("/api/docs/swagger/")
    assert swagger_response.status_code == 200

    redoc_response = client.get("/api/docs/redoc/")
    assert redoc_response.status_code == 200

    health_short_response = client.get("/health")
    assert health_short_response.status_code == 200
    assert health_short_response.data["status"] == "ok"


@pytest.mark.django_db
def test_public_and_authenticated_endpoint_permissions(customer_client, customer_user):
    public_client = APIClient()

    assert public_client.get("/api/v1/catalog/products/").status_code == status.HTTP_200_OK
    assert public_client.get("/api/v1/blog/posts/").status_code == status.HTTP_200_OK
    assert public_client.post(
        "/api/v1/newsletter/",
        {"email": "permissions@example.com"},
        format="json",
    ).status_code == status.HTTP_201_CREATED
    assert public_client.post(
        "/api/v1/sales/inquiries/",
        {"full_name": "Public Buyer", "email": "publicbuyer@example.com"},
        format="json",
    ).status_code == status.HTTP_201_CREATED

    assert public_client.get("/api/v1/auth/me/").status_code in {
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
    }
    assert public_client.get("/api/v1/orders/").status_code in {
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
    }
    assert public_client.get("/api/v1/payments/").status_code in {
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
    }

    assert customer_client.get("/api/v1/auth/me/").status_code == status.HTTP_200_OK
    assert customer_client.post(
        "/api/v1/catalog/categories/",
        {"name": "Blocked Category"},
        format="json",
    ).status_code == status.HTTP_403_FORBIDDEN
    assert customer_client.patch("/api/v1/auth/me/", {}, format="json").status_code == status.HTTP_405_METHOD_NOT_ALLOWED
