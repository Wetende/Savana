import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.catalog.models import Category, Product

from .models import ProductReview

User = get_user_model()


@pytest.mark.django_db
def test_reviews_require_staff_approval_before_public_visibility():
    customer = User.objects.create_user(username="reviewer", password="strongpass123")
    staff = User.objects.create_user(username="moderator", password="strongpass123", is_staff=True)
    category = Category.objects.create(name="Retail")
    product = Product.objects.create(
        name="Kenyan Beans",
        category=category,
        description="Nice beans",
        status="published",
    )

    client = APIClient()
    client.force_authenticate(user=customer)
    create_response = client.post(
        "/api/v1/reviews/",
        {
            "product": product.id,
            "rating": 5,
            "title": "Great coffee",
            "body": "Loved it",
        },
        format="json",
    )
    assert create_response.status_code == 201

    public_client = APIClient()
    public_response = public_client.get("/api/v1/reviews/")
    assert public_response.status_code == 200
    assert public_response.data["results"] == []

    review = ProductReview.objects.get()
    staff_client = APIClient()
    staff_client.force_authenticate(user=staff)
    approve_response = staff_client.post(f"/api/v1/reviews/{review.id}/approve/", {}, format="json")
    assert approve_response.status_code == 200

    visible_response = public_client.get("/api/v1/reviews/")
    assert len(visible_response.data["results"]) == 1


@pytest.mark.django_db
def test_review_endpoints_cover_retrieve_update_and_delete(staff_client, customer_client, other_client):
    category = Category.objects.create(name="Review API")
    product = Product.objects.create(
        name="Reviewable Coffee",
        category=category,
        description="Review coverage",
        status="published",
    )

    create_response = customer_client.post(
        "/api/v1/reviews/",
        {
            "product": product.id,
            "rating": 4,
            "title": "Solid",
            "body": "Good for endpoint coverage",
        },
        format="json",
    )
    assert create_response.status_code == 201
    review_id = create_response.data["id"]

    assert staff_client.get(f"/api/v1/reviews/{review_id}/").status_code == 200
    assert staff_client.put(
        f"/api/v1/reviews/{review_id}/",
        {"title": "Updated by staff"},
        format="json",
    ).status_code == 200
    assert staff_client.post(f"/api/v1/reviews/{review_id}/approve/", {}, format="json").status_code == 200

    public_client = APIClient()
    assert public_client.get(f"/api/v1/reviews/{review_id}/").status_code == 200

    other_review = other_client.post(
        "/api/v1/reviews/",
        {
            "product": product.id,
            "rating": 3,
            "title": "Average",
            "body": "Second review",
        },
        format="json",
    )
    assert other_review.status_code == 201
    assert staff_client.delete(f"/api/v1/reviews/{other_review.data['id']}/").status_code == 204
