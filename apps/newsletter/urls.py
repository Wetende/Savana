from rest_framework.routers import DefaultRouter

from .views import NewsletterSubscriptionViewSet

router = DefaultRouter()
router.register("", NewsletterSubscriptionViewSet, basename="newsletter")

urlpatterns = router.urls
