from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from .serializers import RegisterSerializer, UserProfileUpdateSerializer, UserSerializer
from .selectors import get_user_with_profile
from .services import register_user, update_user_profile


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"

    @extend_schema(tags=["Authentication"], request=RegisterSerializer, responses=UserSerializer)
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = register_user(data=dict(serializer.validated_data))
        return Response(
            UserSerializer(get_user_with_profile(user)).data,
            status=status.HTTP_201_CREATED,
        )


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    @extend_schema(tags=["Authentication"], responses=UserSerializer)
    def get(self, request):
        return Response(UserSerializer(get_user_with_profile(request.user)).data)

    @extend_schema(tags=["Authentication"], request=UserProfileUpdateSerializer, responses=UserSerializer)
    def put(self, request):
        serializer = UserProfileUpdateSerializer(
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        user = update_user_profile(
            user=request.user,
            data=dict(serializer.validated_data),
        )
        return Response(UserSerializer(get_user_with_profile(user)).data)


class CustomerTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"

    @extend_schema(tags=["Authentication"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomerTokenRefreshView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"

    @extend_schema(tags=["Authentication"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
