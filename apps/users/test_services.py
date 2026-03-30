import pytest

from .selectors import get_user_with_profile
from .services import register_user, update_user_profile


@pytest.mark.django_db
def test_user_services_create_and_update_profile_data():
    user = register_user(
        data={
            "username": "service-user",
            "email": "service-user@example.com",
            "password": "strongpass123",
            "profile": {
                "company_name": "Service Imports",
                "business_type": "Distributor",
            },
        }
    )
    user = get_user_with_profile(user)

    assert user.profile.company_name == "Service Imports"

    updated_user = update_user_profile(
        user=user,
        data={
            "first_name": "Updated",
            "profile": {"company_name": "Updated Imports"},
        },
    )
    updated_user = get_user_with_profile(updated_user)

    assert updated_user.first_name == "Updated"
    assert updated_user.profile.company_name == "Updated Imports"
