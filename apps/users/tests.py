import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.mark.django_db
def test_register_and_me_flow():
    client = APIClient()

    response = client.post(
        "/api/v1/auth/register/",
        {
            "username": "buyer1",
            "email": "buyer@example.com",
            "password": "strongpass123",
            "profile": {
                "company_name": "Acme Imports",
                "business_type": "Distributor",
            },
        },
        format="json",
    )
    assert response.status_code == 201
    assert User.objects.filter(username="buyer1").exists()

    token_response = client.post(
        "/api/v1/auth/token/",
        {"username": "buyer1", "password": "strongpass123"},
        format="json",
    )
    assert token_response.status_code == 200

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_response.data['access']}")
    me_response = client.get("/api/v1/auth/me/")
    assert me_response.status_code == 200
    assert me_response.data["email"] == "buyer@example.com"

    patch_response = client.patch(
        "/api/v1/auth/me/",
        {
            "first_name": "Updated",
            "profile": {
                "company_name": "Updated Imports",
            },
        },
        format="json",
    )
    assert patch_response.status_code == 200
    assert patch_response.data["first_name"] == "Updated"
    assert patch_response.data["profile"]["company_name"] == "Updated Imports"

    refresh_response = client.post(
        "/api/v1/auth/token/refresh/",
        {"refresh": token_response.data["refresh"]},
        format="json",
    )
    assert refresh_response.status_code == 200
    assert "access" in refresh_response.data
