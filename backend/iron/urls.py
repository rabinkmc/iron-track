from django.urls import path
from .views import ExerciseView, WorkoutSessionView

urlpatterns = [
    path("exercise/", ExerciseView.as_view(), name="exercise"),
    path("session/", WorkoutSessionView.as_view(), name="workout_session"),
]
