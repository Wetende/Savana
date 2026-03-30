from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.api_mixins import ManagedModelViewSet
from apps.core.permissions import IsStaffUser

from .models import ProductReview
from .serializers import ProductReviewSerializer
from .selectors import review_queryset_for_user
from .services import approve_review, create_review, update_review


@extend_schema(tags=["Reviews"])
class ProductReviewViewSet(ManagedModelViewSet):
    queryset = ProductReview.objects.none()
    read_serializer_class = ProductReviewSerializer
    write_serializer_class = ProductReviewSerializer
    permission_classes = [IsStaffUser]
    permission_classes_by_action = {
        "list": [permissions.AllowAny],
        "retrieve": [permissions.AllowAny],
        "create": [permissions.IsAuthenticated],
        "update": [IsStaffUser],
        "partial_update": [IsStaffUser],
        "destroy": [IsStaffUser],
        "approve": [IsStaffUser],
    }

    def get_queryset(self):
        return review_queryset_for_user(self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = create_review(customer=request.user, data=dict(serializer.validated_data))
        return Response(self.get_serializer(review).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        review = self.get_object()
        serializer = self.get_serializer(review, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        review = update_review(review=review, data=dict(serializer.validated_data))
        return Response(self.get_serializer(review).data)

    @action(detail=True, methods=["post"], permission_classes=[IsStaffUser])
    @extend_schema(tags=["Reviews"], responses=ProductReviewSerializer)
    def approve(self, request, pk=None):
        review = self.get_object()
        review = approve_review(review=review, staff_user=request.user)
        return Response(ProductReviewSerializer(review).data, status=status.HTTP_200_OK)
