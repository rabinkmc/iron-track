from .views import (
    ExerciseViewSet,
    WorkoutSessionExerciseSetViewSet,
    WorkoutSessionExercisesViewSet,
    WorkoutSessionViewSet,
)
from rest_framework.routers import DefaultRouter

app_name = "iron"
router = DefaultRouter()
router.register("exercise", ExerciseViewSet, basename="exercise")
router.register("session", WorkoutSessionViewSet, basename="session")
router.register(
    "session-exercise",
    WorkoutSessionExercisesViewSet,
    basename="session-exercise",
)
router.register(
    "exercise-set", WorkoutSessionExerciseSetViewSet, basename="exercise-set"
)

urlpatterns = router.urls
