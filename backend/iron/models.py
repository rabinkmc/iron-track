from django.contrib.auth import get_user_model
from django.db import models
from common.models import BaseModel

User = get_user_model()

"""
objective: to allow users to see their workout history, including exercises performed, sets, reps, and weights.
Also, they can know which workout they have in the future.


first let's just try to make sure we can track the exercises they do. 
"""


class Exercise(BaseModel):
    name = models.CharField(max_length=100)
    muscle_targeted = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class WorkoutSession(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="workout_sessions"
    )
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)


class WorkoutSessionExercise(BaseModel):
    workout_session = models.ForeignKey(
        WorkoutSession, on_delete=models.CASCADE, related_name="exercises"
    )
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    order = models.IntegerField()
    sets = models.PositiveSmallIntegerField()
    reps = models.PositiveSmallIntegerField()
    weight = models.PositiveSmallIntegerField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.workout_session} - {self.exercise.name}"
