from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests


from api.serializers import CustomTokenObtainPairSerializer
from django.conf import settings


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@api_view(["GET"])
def version(request):
    """
    Returns the API version as a JSON response.
    """
    from rest_framework.response import Response

    version_info = {
        "version": "1.0.0",
        "status": "dev",
        "release_date": "2023-10-01",
    }
    return Response(version_info, status=status.HTTP_200_OK)


# views.py

User = get_user_model()


class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data.get("id_token")
        if not token:
            return Response({"detail": "No token provided"}, status=400)

        try:
            idinfo = id_token.verify_oauth2_token(
                token, google_requests.Request(), settings.GOOGLE_CLIENT_ID
            )
            email = idinfo["email"]
            user, _ = User.objects.get_or_create(
                email=email, defaults={"username": email}
            )

            # Issue JWT token
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": {"email": user.email, "id": user.id},
                }
            )
        except ValueError:
            return Response({"detail": "Invalid token"}, status=400)
