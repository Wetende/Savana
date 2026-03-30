from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

api_root_serializer = inline_serializer(
    name="ApiRootSerializer",
    fields={
        "name": serializers.CharField(),
        "status": serializers.CharField(),
        "message": serializers.CharField(),
        "links": serializers.DictField(child=serializers.URLField()),
    },
)

health_serializer = inline_serializer(
    name="HealthCheckSerializer",
    fields={
        "status": serializers.CharField(),
        "service": serializers.CharField(),
        "version": serializers.CharField(),
    },
)


class ApiRootView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(tags=["System"], responses=api_root_serializer)
    def get(self, request):
        api_root = request.build_absolute_uri("/api/v1/")
        return Response(
            {
                "name": "Coffee Backend",
                "status": "running",
                "message": "The backend is up. Use the links below to explore the API.",
                "links": {
                    "api_root": api_root,
                    "schema": request.build_absolute_uri("/api/schema/"),
                    "swagger": request.build_absolute_uri("/api/docs/swagger/"),
                    "redoc": request.build_absolute_uri("/api/docs/redoc/"),
                    "health": request.build_absolute_uri("/api/v1/health/"),
                    "admin": request.build_absolute_uri("/admin/"),
                    "auth": request.build_absolute_uri("/api/v1/auth/"),
                    "catalog": request.build_absolute_uri("/api/v1/catalog/"),
                    "blog": request.build_absolute_uri("/api/v1/blog/"),
                    "sales": request.build_absolute_uri("/api/v1/sales/"),
                    "orders": request.build_absolute_uri("/api/v1/orders/"),
                    "payments": request.build_absolute_uri("/api/v1/payments/"),
                    "reviews": request.build_absolute_uri("/api/v1/reviews/"),
                    "newsletter": request.build_absolute_uri("/api/v1/newsletter/"),
                },
            }
        )


class HealthCheckView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(tags=["System"], responses=health_serializer)
    def get(self, request):
        return Response(
            {
                "status": "ok",
                "service": "coffee-api",
                "version": "v1",
            }
        )
