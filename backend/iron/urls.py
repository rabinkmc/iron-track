from django.urls import path
from .views import ExerciseView, WorkoutSessionView

app_name = "iron"

urlpatterns = [
    path("exercise/", ExerciseView.as_view(), name="exercise"),
    path("session/", WorkoutSessionView.as_view(), name="session"),
]
