from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, InventoryRecordViewSet, ProductViewSet, ProductVariantViewSet, WholesaleOfferViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="catalog-category")
router.register("products", ProductViewSet, basename="catalog-product")
router.register("variants", ProductVariantViewSet, basename="catalog-variant")
router.register("offers", WholesaleOfferViewSet, basename="catalog-offer")
router.register("inventory", InventoryRecordViewSet, basename="catalog-inventory")

urlpatterns = router.urls
