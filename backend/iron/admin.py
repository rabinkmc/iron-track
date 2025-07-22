from django.contrib import admin

from iron.models import (
    Exercise,
    WorkoutSession,
    WorkoutSessionExercise,
    WorkoutSessionExerciseSet,
)

admin.site.register(Exercise)
admin.site.register(WorkoutSession)
admin.site.register(WorkoutSessionExercise)
admin.site.register(WorkoutSessionExerciseSet)
