from django.utils.text import slugify


def build_unique_slug(model_class, raw_value, *, field_name="slug", instance=None):
    base_slug = slugify(raw_value) or "item"
    slug = base_slug
    index = 2

    queryset = model_class.objects.all()
    if instance and instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    while queryset.filter(**{field_name: slug}).exists():
        slug = f"{base_slug}-{index}"
        index += 1

    return slug
