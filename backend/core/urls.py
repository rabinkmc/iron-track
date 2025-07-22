from django.contrib import admin
from django.http.response import HttpResponse
from django.urls import path, include


def home(request):
    return HttpResponse("Welcome to the Home Page")


urlpatterns = [
    path("", home, name="home"),
    path("api/auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/", include("api.urls")),
    path("admin/", admin.site.urls),
]
