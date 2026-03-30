from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.permissions import IsStaffOrReadOnly, IsStaffUser

from .models import ProductReview
from .serializers import ProductReviewSerializer


class ProductReviewViewSet(viewsets.ModelViewSet):
    queryset = ProductReview.objects.select_related("product", "customer", "approved_by")
    serializer_class = ProductReviewSerializer

    def get_permissions(self):
        if self.action in {"list", "retrieve"}:
            return [permissions.AllowAny()]
        if self.action == "create":
            return [permissions.IsAuthenticated()]
        return [IsStaffUser()]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(status="approved")

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    @action(detail=True, methods=["post"], permission_classes=[IsStaffUser])
    def approve(self, request, pk=None):
        review = self.get_object()
        review.approve(request.user)
        return Response(ProductReviewSerializer(review).data, status=status.HTTP_200_OK)
