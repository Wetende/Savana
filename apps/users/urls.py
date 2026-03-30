from django.urls import path

from .views import CustomerTokenObtainPairView, CustomerTokenRefreshView, MeView, RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("token/", CustomerTokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("token/refresh/", CustomerTokenRefreshView.as_view(), name="token-refresh"),
    path("me/", MeView.as_view(), name="auth-me"),
]
