from django.urls import path
from .views import lift_list

urlpatterns = [path("lift/", lift_list)]
