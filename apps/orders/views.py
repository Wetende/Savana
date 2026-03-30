from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.response import Response

from apps.core.api_mixins import ManagedModelViewSet
from apps.core.permissions import IsStaffUser

from .models import Address, Order
from .selectors import address_queryset_for_user, order_queryset_for_user
from .serializers import AddressSerializer, OrderReadSerializer, OrderWriteSerializer
from .services import create_order, update_order


@extend_schema(tags=["Orders & Shipping"])
class AddressViewSet(ManagedModelViewSet):
    queryset = Address.objects.none()
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return address_queryset_for_user(self.request.user)

    def perform_create(self, serializer):
        customer = None if self.request.user.is_staff else self.request.user
        serializer.save(customer=customer)


@extend_schema(tags=["Orders & Shipping"])
class OrderViewSet(ManagedModelViewSet):
    queryset = Order.objects.none()
    read_serializer_class = OrderReadSerializer
    write_serializer_class = OrderWriteSerializer
    permission_classes = [IsStaffUser]
    permission_classes_by_action = {
        "list": [permissions.IsAuthenticated],
        "retrieve": [permissions.IsAuthenticated],
        "create": [IsStaffUser],
        "update": [IsStaffUser],
        "partial_update": [IsStaffUser],
        "destroy": [IsStaffUser],
    }

    def get_queryset(self):
        return order_queryset_for_user(self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_write_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = create_order(data=dict(serializer.validated_data))
        return Response(
            self.get_read_serializer(order).data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        serializer = self.get_write_serializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        order = update_order(order=order, data=dict(serializer.validated_data))
        return Response(self.get_read_serializer(order).data)
