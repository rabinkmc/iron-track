from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    authentication_classes,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests


from api.serializers import CustomTokenObtainPairSerializer
from django.conf import settings

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@api_view(["GET"])
def version(request):
    version_info = {
        "version": "0.0.2",
        "status": "dev",
        "release_date": "2023-10-06",
        "description": "dockerized django rest framework api",
    }
    return Response(version_info, status=status.HTTP_200_OK)


@api_view(["POST"])
@authentication_classes([])
def google_login(request):
    token = request.data.get("id_token")
    if not token:
        return Response({"detail": "No token provided"}, status=400)

    try:
        idinfo = id_token.verify_oauth2_token(
            token, google_requests.Request(), settings.GOOGLE_CLIENT_ID
        )
        email = idinfo["email"]
        user, _ = User.objects.get_or_create(email=email, defaults={"username": email})

        # Issue JWT token
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {"email": user.email, "id": user.id},  # type: ignore
            }
        )
    except ValueError:
        return Response({"detail": "Invalid token"}, status=400)
