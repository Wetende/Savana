from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.emailing import send_system_email
from apps.core.permissions import IsOwnerOrStaff, IsStaffUser
from apps.orders.serializers import OrderSerializer

from .models import Inquiry, Quote
from .serializers import (
    InquirySerializer,
    QuoteAcceptSerializer,
    QuoteSerializer,
    create_order_from_quote,
)


class InquiryViewSet(viewsets.ModelViewSet):
    queryset = Inquiry.objects.prefetch_related("items").select_related("customer")
    serializer_class = InquirySerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        if self.request.user.is_staff:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsOwnerOrStaff()]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(customer=self.request.user)


class QuoteViewSet(viewsets.ModelViewSet):
    queryset = Quote.objects.prefetch_related("items").select_related("customer", "inquiry")
    serializer_class = QuoteSerializer

    def get_permissions(self):
        if self.action in {"list", "retrieve", "accept"}:
            return [permissions.IsAuthenticated(), IsOwnerOrStaff()]
        return [IsStaffUser()]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(customer=self.request.user)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated, IsOwnerOrStaff])
    def accept(self, request, pk=None):
        quote = self.get_object()
        serializer = QuoteAcceptSerializer(data=request.data or {"accepted": True})
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data["accepted"]:
            quote.status = "accepted"
            quote.accepted_at = timezone.now()
            quote.save(update_fields=["status", "accepted_at"])
            email = quote.customer.email if quote.customer else getattr(quote.inquiry, "email", None)
            if email:
                send_system_email(
                    subject=f"Quote {quote.reference} accepted",
                    message=f"Quote {quote.reference} has been accepted.",
                    recipient_list=[email],
                )
        return Response(QuoteSerializer(quote).data)

    @action(detail=True, methods=["post"], permission_classes=[IsStaffUser])
    def convert_to_order(self, request, pk=None):
        quote = self.get_object()
        order = create_order_from_quote(quote)
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class GuestQuoteMixin:
    def get_guest_quote(self, reference, token):
        return Quote.objects.prefetch_related("items").select_related("customer", "inquiry").get(
            reference=reference,
            guest_access_token=token,
        )


class GuestQuoteDetailView(GuestQuoteMixin, APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, reference, token):
        quote = self.get_guest_quote(reference, token)
        return Response(QuoteSerializer(quote).data)


class GuestQuoteAcceptView(GuestQuoteMixin, APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, reference, token):
        quote = self.get_guest_quote(reference, token)
        if quote.status not in {"accepted", "converted"}:
            quote.status = "accepted"
            quote.accepted_at = timezone.now()
            quote.save(update_fields=["status", "accepted_at"])
            email = quote.customer.email if quote.customer else getattr(quote.inquiry, "email", None)
            if email:
                send_system_email(
                    subject=f"Quote {quote.reference} accepted",
                    message=f"Quote {quote.reference} has been accepted.",
                    recipient_list=[email],
                )
        return Response(QuoteSerializer(quote).data)
