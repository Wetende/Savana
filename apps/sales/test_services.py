import pytest
from django.contrib.auth import get_user_model
from django.http import Http404

from apps.catalog.models import Category, Product

from .models import Quote
from .selectors import get_guest_quote
from .services import accept_quote, create_inquiry

User = get_user_model()


@pytest.mark.django_db
def test_create_inquiry_service_assigns_authenticated_customer():
    customer = User.objects.create_user(username="svc-buyer", password="strongpass123")
    category = Category.objects.create(name="Service Sales")
    product = Product.objects.create(
        name="Service Coffee",
        category=category,
        description="Service inquiry",
        status="published",
    )

    inquiry = create_inquiry(
        actor=customer,
        data={
            "full_name": "Service Buyer",
            "email": "servicebuyer@example.com",
            "items": [{"product": product, "requested_quantity": "3.00"}],
        },
    )

    assert inquiry.customer == customer
    assert inquiry.items.count() == 1


@pytest.mark.django_db
def test_accept_quote_service_and_guest_selector_behave_safely():
    quote = Quote.objects.create(status="sent")

    updated_quote = accept_quote(quote=quote)

    assert updated_quote.status == "accepted"
    assert updated_quote.accepted_at is not None

    with pytest.raises(Http404):
        get_guest_quote("missing-ref", quote.guest_access_token)
