from django.db import transaction

from .models import ProductReview


@transaction.atomic
def create_review(*, customer, data):
    return ProductReview.objects.create(customer=customer, **data)


@transaction.atomic
def update_review(*, review, data):
    for field, value in data.items():
        setattr(review, field, value)
    review.save()
    return review


@transaction.atomic
def approve_review(*, review, staff_user):
    review.approve(staff_user)
    return review
