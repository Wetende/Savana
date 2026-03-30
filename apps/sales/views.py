from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from apps.core.api_mixins import ManagedModelViewSet
from apps.core.permissions import IsStaffUser
from apps.orders.serializers import OrderReadSerializer
from apps.orders.services import create_order_from_quote

from .models import Inquiry, Quote
from .serializers import (
    InquiryReadSerializer,
    InquiryWriteSerializer,
    QuoteAcceptSerializer,
    QuoteReadSerializer,
    QuoteWriteSerializer,
)
from .selectors import get_guest_quote, inquiry_queryset_for_user, quote_queryset_for_user
from .services import accept_quote, create_inquiry, create_quote, update_quote


@extend_schema(tags=["Sales & Quotes"])
class InquiryViewSet(ManagedModelViewSet):
    read_serializer_class = InquiryReadSerializer
    write_serializer_class = InquiryWriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    permission_classes_by_action = {
        "create": [permissions.AllowAny],
        "list": [permissions.IsAuthenticated],
        "retrieve": [permissions.IsAuthenticated],
        "update": [permissions.IsAuthenticated],
        "partial_update": [permissions.IsAuthenticated],
        "destroy": [permissions.IsAuthenticated],
    }
    throttle_classes_by_action = {
        "create": [ScopedRateThrottle],
    }
    throttle_scopes_by_action = {
        "create": "lead-capture",
    }

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Inquiry.objects.none()
        return inquiry_queryset_for_user(self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_write_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        inquiry = create_inquiry(actor=request.user, data=dict(serializer.validated_data))
        return Response(
            self.get_read_serializer(inquiry).data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        inquiry = self.get_object()
        serializer = self.get_write_serializer(inquiry, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(self.get_read_serializer(inquiry).data)


@extend_schema(tags=["Sales & Quotes"])
class QuoteViewSet(ManagedModelViewSet):
    read_serializer_class = QuoteReadSerializer
    write_serializer_class = QuoteWriteSerializer
    permission_classes = [IsStaffUser]
    permission_classes_by_action = {
        "list": [permissions.IsAuthenticated],
        "retrieve": [permissions.IsAuthenticated],
        "accept": [permissions.IsAuthenticated],
        "create": [IsStaffUser],
        "update": [IsStaffUser],
        "partial_update": [IsStaffUser],
        "destroy": [IsStaffUser],
        "convert_to_order": [IsStaffUser],
    }

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Quote.objects.none()
        return quote_queryset_for_user(self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_write_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quote = create_quote(data=dict(serializer.validated_data))
        return Response(
            self.get_read_serializer(quote).data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        quote = self.get_object()
        serializer = self.get_write_serializer(quote, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        quote = update_quote(quote=quote, data=dict(serializer.validated_data))
        return Response(self.get_read_serializer(quote).data)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    @extend_schema(tags=["Sales & Quotes"], request=QuoteAcceptSerializer, responses=QuoteReadSerializer)
    def accept(self, request, pk=None):
        quote = self.get_object()
        serializer = QuoteAcceptSerializer(data=request.data or {"accepted": True})
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data["accepted"]:
            quote = accept_quote(quote=quote)
        return Response(self.get_read_serializer(quote).data)

    @action(detail=True, methods=["post"], permission_classes=[IsStaffUser])
    @extend_schema(tags=["Sales & Quotes"], request=None, responses=OrderReadSerializer)
    def convert_to_order(self, request, pk=None):
        quote = self.get_object()
        order = create_order_from_quote(quote=quote)
        return Response(OrderReadSerializer(order).data, status=status.HTTP_201_CREATED)


class GuestQuoteMixin:
    def get_guest_quote(self, reference, token):
        return get_guest_quote(reference, token)


class GuestQuoteView(GuestQuoteMixin, APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = QuoteReadSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "guest-quote"

    @extend_schema(
        tags=["Sales & Quotes"],
        parameters=[
            OpenApiParameter("reference", str, OpenApiParameter.PATH),
            OpenApiParameter("token", str, OpenApiParameter.PATH),
        ],
        responses=QuoteReadSerializer,
    )
    def get(self, request, reference, token):
        quote = self.get_guest_quote(reference, token)
        return Response(QuoteReadSerializer(quote).data)

    @extend_schema(
        tags=["Sales & Quotes"],
        parameters=[
            OpenApiParameter("reference", str, OpenApiParameter.PATH),
            OpenApiParameter("token", str, OpenApiParameter.PATH),
        ],
        request=QuoteAcceptSerializer,
        responses=QuoteReadSerializer,
    )
    def put(self, request, reference, token):
        quote = self.get_guest_quote(reference, token)
        serializer = QuoteAcceptSerializer(data=request.data or {"accepted": True})
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data["accepted"]:
            quote = accept_quote(quote=quote)
        return Response(QuoteReadSerializer(quote).data)
