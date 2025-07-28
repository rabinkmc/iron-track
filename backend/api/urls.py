from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from api.views import CustomTokenObtainPairView, google_login, version


urlpatterns = [
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("google-login/", google_login, name="google_login"),
    path("iron/", include("iron.urls")),
    path("version/", version, name="api_versioning"),
]
