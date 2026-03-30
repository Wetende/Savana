from django.contrib.auth import get_user_model

User = get_user_model()


def get_user_with_profile(user):
    return User.objects.select_related("profile").get(pk=user.pk)
