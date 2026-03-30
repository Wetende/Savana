from rest_framework import permissions, viewsets

from apps.core.permissions import IsStaffUser

from .models import NewsletterSubscription
from .serializers import NewsletterSubscriptionSerializer


class NewsletterSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = NewsletterSubscription.objects.all()
    serializer_class = NewsletterSubscriptionSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return [IsStaffUser()]
