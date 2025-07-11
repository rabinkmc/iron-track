from django.contrib.auth import get_user_model
from django.db import models
from common.models import BaseModel

User = get_user_model()


class Exercise(BaseModel):
    name = models.CharField(max_length=100)
    muscle_targeted = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class WorkoutSplit(BaseModel):
    name = models.CharField(max_length=100)
    # Number of distinct workout days in the split (e.g., 3-day split)
    length = models.IntegerField()


class WorkoutSplitDay(BaseModel):
    split = models.ForeignKey(
        WorkoutSplit, on_delete=models.CASCADE, related_name="days"
    )
    day_number = models.IntegerField()
    name = models.CharField(max_length=100)


class WorkoutSplitDayExercise(BaseModel):
    workout_day = models.ForeignKey(WorkoutSplitDay, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    order = models.IntegerField()  # exercise order within the day


class WorkoutSession(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="workout_sessions"
    )
    date = models.DateField()
    split_day = models.ForeignKey(
        WorkoutSplitDay, on_delete=models.CASCADE, related_name="sessions"
    )

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.split_day.name}"


class WorkoutSessionExercise(BaseModel):
    workout_session = models.ForeignKey(
        WorkoutSession, on_delete=models.CASCADE, related_name="exercises"
    )
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.PositiveSmallIntegerField()
    reps = models.PositiveSmallIntegerField()
    weight = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.workout_session} - {self.exercise.name}"
