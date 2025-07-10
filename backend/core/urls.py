from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/", include("iron.urls")),
    path("admin/", admin.site.urls),
]
