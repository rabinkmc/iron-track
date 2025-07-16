from django.contrib import admin
from django.urls import path, include

urlpatterns = [path("iron/", include("iron.urls"))]
