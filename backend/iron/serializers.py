from rest_framework import serializers
from .models import (
    Exercise,
    WorkoutSession,
)


class ExerciseSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    muscle_targeted = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False, allow_blank=True)


class WorkoutSessionSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=WorkoutSession.objects.all(), source="user"
    )
    date = serializers.DateField()
    notes = serializers.CharField(allow_blank=True, required=False)
    exercises = serializers.SerializerMethodField()

    def get_exercises(self, obj):
        return [
            {
                "name": exercise.exercise.name,
                "order": exercise.order,
                "sets": exercise.set,
                "reps": exercise.reps,
                "weight": exercise.weight,
            }
            for exercise in obj.exercises.all()
        ]


class WorkoutSessionExerciseSerializer(serializers.Serializer):
    workout_session = serializers.PrimaryKeyRelatedField(
        queryset=WorkoutSession.objects.all()
    )
    exercise = serializers.PrimaryKeyRelatedField(queryset=Exercise.objects.all())
    order = serializers.IntegerField()
    sets = serializers.IntegerField()
    reps = serializers.IntegerField()
    weight = serializers.IntegerField()
    notes = serializers.CharField(allow_blank=True, required=False)
