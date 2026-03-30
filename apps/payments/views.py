from rest_framework import permissions, response, status, viewsets
from rest_framework.views import APIView

from apps.core.permissions import IsOwnerOrStaff, IsStaffUser

from .models import Payment, PaymentAttempt
from .serializers import PaymentAttemptSerializer, PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.prefetch_related("attempts").select_related("customer", "order", "quote")
    serializer_class = PaymentSerializer

    def get_permissions(self):
        if self.action in {"list", "retrieve"}:
            return [permissions.IsAuthenticated(), IsOwnerOrStaff()]
        return [IsStaffUser()]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(customer=self.request.user)


class PaymentAttemptViewSet(viewsets.ModelViewSet):
    queryset = PaymentAttempt.objects.select_related("payment")
    serializer_class = PaymentAttemptSerializer
    permission_classes = [IsStaffUser]


class PaymentWebhookStubView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, provider):
        return response.Response(
            {
                "received": True,
                "provider": provider,
                "payload": request.data,
            },
            status=status.HTTP_202_ACCEPTED,
        )
