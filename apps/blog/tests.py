import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APIClient

from .models import Category, Post, Tag

User = get_user_model()


@pytest.mark.django_db
def test_public_blog_only_returns_published_posts():
    author = User.objects.create_user(username="editor", password="strongpass123", is_staff=True)
    Post.objects.create(
        author=author,
        title="Published Story",
        content="Coffee origin story",
        status="published",
        published_at=timezone.now(),
    )
    Post.objects.create(
        author=author,
        title="Draft Story",
        content="Hidden draft",
        status="draft",
    )

    client = APIClient()
    response = client.get("/api/v1/blog/posts/")

    assert response.status_code == 200
    titles = {item["title"] for item in response.data["results"]}
    assert "Published Story" in titles
    assert "Draft Story" not in titles


@pytest.mark.django_db
def test_blog_endpoints_support_public_reads_and_staff_crud(staff_client, staff_user):
    public_client = APIClient()

    category_response = staff_client.post(
        "/api/v1/blog/categories/",
        {"name": "Origin Stories"},
        format="json",
    )
    assert category_response.status_code == 201
    category_id = category_response.data["id"]

    tag_response = staff_client.post(
        "/api/v1/blog/tags/",
        {"name": "Kenya"},
        format="json",
    )
    assert tag_response.status_code == 201
    tag_id = tag_response.data["id"]

    post_response = staff_client.post(
        "/api/v1/blog/posts/",
        {
            "title": "Coffee Journey",
            "summary": "A story of origin.",
            "content": "Long form content",
            "status": "published",
            "category_id": category_id,
            "tag_ids": [tag_id],
        },
        format="json",
    )
    assert post_response.status_code == 201
    slug = post_response.data["slug"]
    post_id = post_response.data["id"]

    assert public_client.get("/api/v1/blog/categories/").status_code == 200
    assert public_client.get(f"/api/v1/blog/categories/{category_id}/").status_code == 200
    assert public_client.get("/api/v1/blog/tags/").status_code == 200
    assert public_client.get(f"/api/v1/blog/tags/{tag_id}/").status_code == 200
    assert public_client.get("/api/v1/blog/posts/").status_code == 200
    assert public_client.get(f"/api/v1/blog/posts/{slug}/").status_code == 200

    assert staff_client.patch(
        f"/api/v1/blog/posts/{slug}/",
        {"summary": "Updated summary"},
        format="json",
    ).status_code == 200

    assert staff_client.delete(f"/api/v1/blog/posts/{slug}/").status_code == 204
    assert staff_client.delete(f"/api/v1/blog/tags/{tag_id}/").status_code == 204
    assert staff_client.delete(f"/api/v1/blog/categories/{category_id}/").status_code == 204
