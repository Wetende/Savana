from django.utils import timezone
from rest_framework import viewsets

from apps.core.permissions import IsStaffOrReadOnly

from .models import Category, Post, Tag
from .serializers import BlogCategorySerializer, PostSerializer, TagSerializer


class BlogCategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = BlogCategorySerializer
    permission_classes = [IsStaffOrReadOnly]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsStaffOrReadOnly]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("author", "category").prefetch_related("tags")
    serializer_class = PostSerializer
    permission_classes = [IsStaffOrReadOnly]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(status="published", published_at__lte=timezone.now())

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
