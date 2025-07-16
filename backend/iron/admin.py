from django.contrib import admin

from iron.models import (
    Exercise,
    WorkoutSession,
    WorkoutSessionExercise,
)

admin.site.register(Exercise)
admin.site.register(WorkoutSession)
admin.site.register(WorkoutSessionExercise)
