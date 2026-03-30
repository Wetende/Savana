from django.db import transaction

from .models import Post


@transaction.atomic
def create_post(*, author, data):
    tags = data.pop("tags", [])
    post = Post.objects.create(author=author, **data)
    if tags:
        post.tags.set(tags)
    return post


@transaction.atomic
def update_post(*, post, data):
    tags = data.pop("tags", None)
    for field, value in data.items():
        setattr(post, field, value)
    post.save()
    if tags is not None:
        post.tags.set(tags)
    return post
