from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response

from apps.core.api_mixins import ManagedModelViewSet
from apps.core.permissions import IsStaffOrReadOnly

from .models import Category, Post, Tag
from .selectors import blog_category_queryset, post_queryset_for_user, tag_queryset
from .serializers import BlogCategorySerializer, PostSerializer, TagSerializer
from .services import create_post, update_post


@extend_schema(tags=["Blog"])
class BlogCategoryViewSet(ManagedModelViewSet):
    queryset = Category.objects.all()
    serializer_class = BlogCategorySerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        return blog_category_queryset()


@extend_schema(tags=["Blog"])
class TagViewSet(ManagedModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        return tag_queryset()


@extend_schema(tags=["Blog"])
class PostViewSet(ManagedModelViewSet):
    queryset = Post.objects.select_related("author", "category").prefetch_related("tags")
    serializer_class = PostSerializer
    permission_classes = [IsStaffOrReadOnly]
    lookup_field = "slug"

    def get_queryset(self):
        return post_queryset_for_user(self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = create_post(author=request.user, data=dict(serializer.validated_data))
        return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        serializer = self.get_serializer(post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        post = update_post(post=post, data=dict(serializer.validated_data))
        return Response(PostSerializer(post).data)
