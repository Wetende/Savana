from rest_framework.routers import DefaultRouter

from .views import ProductReviewViewSet

router = DefaultRouter()
router.register("", ProductReviewViewSet, basename="reviews")

urlpatterns = router.urls
