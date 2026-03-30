from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()


def _sync_profile(profile, profile_data):
    for field, value in profile_data.items():
        setattr(profile, field, value)
    profile.save()


@transaction.atomic
def register_user(*, data):
    profile_data = data.pop("profile", {})
    user = User.objects.create_user(
        username=data["username"],
        email=data.get("email", ""),
        first_name=data.get("first_name", ""),
        last_name=data.get("last_name", ""),
        password=data["password"],
    )
    _sync_profile(user.profile, profile_data)
    return user


@transaction.atomic
def update_user_profile(*, user, data):
    profile_data = data.pop("profile", {})
    for field, value in data.items():
        setattr(user, field, value)
    user.save()
    _sync_profile(user.profile, profile_data)
    return user
