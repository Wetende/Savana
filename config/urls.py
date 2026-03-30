from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from apps.core.views import ApiRootView, HealthCheckView

urlpatterns = [
    path("", ApiRootView.as_view(), name="project-root"),
    path("health", HealthCheckView.as_view(), name="health-short"),
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui-short",
    ),
    path(
        "api/docs/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/docs/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("api/v1/", include("apps.core.urls")),
    path("api/v1/auth/", include("apps.users.urls")),
    path("api/v1/catalog/", include("apps.catalog.urls")),
    path("api/v1/blog/", include("apps.blog.urls")),
    path("api/v1/sales/", include("apps.sales.urls")),
    path("api/v1/orders/", include("apps.orders.urls")),
    path("api/v1/payments/", include("apps.payments.urls")),
    path("api/v1/reviews/", include("apps.reviews.urls")),
    path("api/v1/newsletter/", include("apps.newsletter.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
