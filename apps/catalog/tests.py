import pytest
from rest_framework.test import APIClient

from .models import Category, InventoryRecord, Product, ProductVariant, WholesaleOffer


@pytest.mark.django_db
def test_public_catalog_only_returns_published_products():
    category = Category.objects.create(name="Arabica")
    Product.objects.create(
        name="Published Coffee",
        category=category,
        description="Ready for buyers",
        status="published",
    )
    Product.objects.create(
        name="Draft Coffee",
        category=category,
        description="Hidden",
        status="draft",
    )

    client = APIClient()
    response = client.get("/api/v1/catalog/products/")

    assert response.status_code == 200
    names = {item["name"] for item in response.data["results"]}
    assert "Published Coffee" in names
    assert "Draft Coffee" not in names


@pytest.mark.django_db
def test_catalog_endpoints_support_public_reads_and_staff_crud(staff_client):
    public_client = APIClient()

    create_category = staff_client.post(
        "/api/v1/catalog/categories/",
        {"name": "Special Reserve", "description": "Premium lots"},
        format="json",
    )
    assert create_category.status_code == 201
    category_id = create_category.data["id"]

    create_product = staff_client.post(
        "/api/v1/catalog/products/",
        {
            "name": "Kenya AA Reserve",
            "category_id": category_id,
            "short_description": "Bright acidity",
            "description": "Special export lot",
            "status": "published",
            "is_wholesale_available": True,
            "is_retail_available": False,
        },
        format="json",
    )
    assert create_product.status_code == 201
    product_slug = create_product.data["slug"]
    product_id = create_product.data["id"]

    create_variant = staff_client.post(
        "/api/v1/catalog/variants/",
        {
            "product": product_id,
            "name": "25kg Bag",
            "sku": "AA-25KG",
            "packaging_size": "25.00",
            "packaging_unit": "kg",
            "roast_type": "green",
            "is_active": True,
        },
        format="json",
    )
    assert create_variant.status_code == 201
    variant_id = create_variant.data["id"]

    create_offer = staff_client.post(
        "/api/v1/catalog/offers/",
        {
            "product": product_id,
            "grade": "AA",
            "minimum_order_quantity": "10.00",
            "quantity_unit": "bag",
            "quote_only": True,
            "availability_status": "available",
            "lead_time_days": 14,
            "is_active": True,
        },
        format="json",
    )
    assert create_offer.status_code == 201
    offer_id = create_offer.data["id"]

    create_inventory = staff_client.post(
        "/api/v1/catalog/inventory/",
        {
            "product": product_id,
            "variant": variant_id,
            "quantity_on_hand": "30.00",
            "reserved_quantity": "5.00",
            "low_stock_threshold": "3.00",
            "availability_status": "available",
        },
        format="json",
    )
    assert create_inventory.status_code == 201
    inventory_id = create_inventory.data["id"]

    assert public_client.get("/api/v1/catalog/categories/").status_code == 200
    assert public_client.get(f"/api/v1/catalog/categories/{category_id}/").status_code == 200
    assert public_client.get("/api/v1/catalog/products/").status_code == 200
    assert public_client.get(f"/api/v1/catalog/products/{product_slug}/").status_code == 200
    assert public_client.get("/api/v1/catalog/variants/").status_code == 200
    assert staff_client.get(f"/api/v1/catalog/variants/{variant_id}/").status_code == 200
    assert public_client.get("/api/v1/catalog/offers/").status_code == 200
    assert staff_client.get(f"/api/v1/catalog/offers/{offer_id}/").status_code == 200

    patch_product = staff_client.patch(
        f"/api/v1/catalog/products/{product_slug}/",
        {"short_description": "Updated copy"},
        format="json",
    )
    assert patch_product.status_code == 200

    assert staff_client.get("/api/v1/catalog/inventory/").status_code == 200
    assert staff_client.get(f"/api/v1/catalog/inventory/{inventory_id}/").status_code == 200
    assert staff_client.patch(
        f"/api/v1/catalog/inventory/{inventory_id}/",
        {"reserved_quantity": "7.00"},
        format="json",
    ).status_code == 200

    assert staff_client.delete(f"/api/v1/catalog/inventory/{inventory_id}/").status_code == 204
    assert staff_client.delete(f"/api/v1/catalog/offers/{offer_id}/").status_code == 204
    assert staff_client.delete(f"/api/v1/catalog/variants/{variant_id}/").status_code == 204
    assert staff_client.delete(f"/api/v1/catalog/products/{product_slug}/").status_code == 204
    assert staff_client.delete(f"/api/v1/catalog/categories/{category_id}/").status_code == 204


@pytest.mark.django_db
def test_inventory_supports_multiple_variants_per_product():
    category = Category.objects.create(name="Bulk")
    product = Product.objects.create(
        name="Warehouse Coffee",
        category=category,
        description="Inventory test",
        status="published",
    )
    variant_one = ProductVariant.objects.create(product=product, name="10kg", sku="INV-10")
    variant_two = ProductVariant.objects.create(product=product, name="20kg", sku="INV-20")

    InventoryRecord.objects.create(product=product, variant=variant_one, quantity_on_hand="10.00")
    InventoryRecord.objects.create(product=product, variant=variant_two, quantity_on_hand="20.00")
    InventoryRecord.objects.create(product=product, quantity_on_hand="100.00")

    assert product.inventory_records.count() == 3


@pytest.mark.django_db
def test_public_inventory_endpoint_is_not_available():
    client = APIClient()
    response = client.get("/api/v1/catalog/inventory/")
    assert response.status_code == 403
