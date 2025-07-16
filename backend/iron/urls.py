from django.urls import include, path
from .views import ExerciseViewSet, WorkoutSessionViewSet
from rest_framework.routers import DefaultRouter

app_name = "iron"
router = DefaultRouter()
router.register("exercise", ExerciseViewSet, basename="exercise")
router.register("session", WorkoutSessionViewSet, basename="session")

urlpatterns = [path("", include(router.urls))]
