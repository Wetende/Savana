import pytest

from apps.catalog.models import Category, Product
from apps.sales.models import Quote, QuoteItem

from .services import create_order_from_quote


@pytest.mark.django_db
def test_create_order_from_quote_service_is_idempotent():
    category = Category.objects.create(name="Order Services")
    product = Product.objects.create(
        name="Order Service Coffee",
        category=category,
        description="Quote conversion",
        status="published",
    )
    quote = Quote.objects.create(status="accepted", shipping_amount="10.00")
    QuoteItem.objects.create(
        quote=quote,
        product=product,
        product_name="Order Service Coffee",
        quantity="2.00",
        unit_price="50.00",
    )

    first_order = create_order_from_quote(quote=quote)
    second_order = create_order_from_quote(quote=quote)

    assert first_order.pk == second_order.pk
    assert first_order.total_amount == first_order.subtotal_amount + first_order.shipping_amount
    quote.refresh_from_db()
    assert quote.status == "converted"
