from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view

from api.serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@api_view(["GET"])
def api_versioning(request):
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
