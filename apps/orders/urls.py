from rest_framework.routers import DefaultRouter

from .views import AddressViewSet, OrderViewSet

router = DefaultRouter()
router.register("addresses", AddressViewSet, basename="orders-address")
router.register("", OrderViewSet, basename="orders-order")

urlpatterns = router.urls
