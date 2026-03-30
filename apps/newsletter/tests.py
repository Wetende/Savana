import pytest
from rest_framework.test import APIClient

from .models import NewsletterSubscription


@pytest.mark.django_db
def test_public_newsletter_signup():
    client = APIClient()
    response = client.post(
        "/api/v1/newsletter/",
        {
            "email": "subscriber@example.com",
            "full_name": "Newsletter User",
            "source": "footer-form",
        },
        format="json",
    )

    assert response.status_code == 201
    assert NewsletterSubscription.objects.filter(email="subscriber@example.com").exists()


@pytest.mark.django_db
def test_newsletter_endpoints_cover_staff_management(staff_client):
    public_client = APIClient()
    create_response = public_client.post(
        "/api/v1/newsletter/",
        {
            "email": "managed@example.com",
            "full_name": "Managed User",
            "source": "landing-page",
        },
        format="json",
    )
    assert create_response.status_code == 201
    subscription_id = create_response.data["id"]

    assert staff_client.get("/api/v1/newsletter/").status_code == 200
    assert staff_client.get(f"/api/v1/newsletter/{subscription_id}/").status_code == 200
    assert staff_client.put(
        f"/api/v1/newsletter/{subscription_id}/",
        {"status": "unsubscribed"},
        format="json",
    ).status_code == 200
    assert staff_client.delete(f"/api/v1/newsletter/{subscription_id}/").status_code == 204
