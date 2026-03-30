from rest_framework import permissions, viewsets

from apps.core.permissions import IsOwnerOrStaff, IsStaffUser

from .models import Address, Order
from .serializers import AddressSerializer, OrderSerializer


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.select_related("customer").order_by("-created_at")
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(customer=self.request.user)

    def perform_create(self, serializer):
        customer = None if self.request.user.is_staff else self.request.user
        serializer.save(customer=customer)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("items").select_related(
        "customer",
        "quote",
        "billing_address",
        "shipping_address",
    )
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action in {"list", "retrieve"}:
            return [permissions.IsAuthenticated(), IsOwnerOrStaff()]
        return [IsStaffUser()]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(customer=self.request.user)
