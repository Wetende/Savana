from django.utils import timezone

from .models import Category, Post, Tag


def blog_category_queryset():
    return Category.objects.order_by("name")


def tag_queryset():
    return Tag.objects.order_by("name")


def post_queryset_for_user(user):
    queryset = Post.objects.select_related("author", "category").prefetch_related("tags")
    if user.is_staff:
        return queryset
    return queryset.filter(status="published", published_at__lte=timezone.now())
