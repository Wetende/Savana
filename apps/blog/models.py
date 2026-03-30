from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.core.model_mixins import AutoSlugMixin
from apps.core.models import TimeStampedModel


class Category(AutoSlugMixin, TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        self.ensure_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(AutoSlugMixin, TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        self.ensure_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(AutoSlugMixin, TimeStampedModel):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]
    slug_source_field = "title"

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="blog_posts")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="posts", null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    summary = models.TextField(blank=True)
    content = models.TextField()
    featured_image = models.ImageField(upload_to="blog/", blank=True)
    seo_title = models.CharField(max_length=255, blank=True)
    seo_description = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def save(self, *args, **kwargs):
        self.ensure_slug()
        if self.status == "published" and self.published_at is None:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
