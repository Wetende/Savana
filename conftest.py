import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def staff_user():
    return User.objects.create_user(
        username="staff-user",
        email="staff@example.com",
        password="strongpass123",
        is_staff=True,
    )


@pytest.fixture
def customer_user():
    return User.objects.create_user(
        username="customer-user",
        email="customer@example.com",
        password="strongpass123",
    )


@pytest.fixture
def other_user():
    return User.objects.create_user(
        username="other-user",
        email="other@example.com",
        password="strongpass123",
    )


@pytest.fixture
def staff_client(staff_user):
    client = APIClient()
    client.force_authenticate(user=staff_user)
    return client


@pytest.fixture
def customer_client(customer_user):
    client = APIClient()
    client.force_authenticate(user=customer_user)
    return client


@pytest.fixture
def other_client(other_user):
    client = APIClient()
    client.force_authenticate(user=other_user)
    return client
