from rest_framework import serializers
from .models import (
    Exercise,
    WorkoutSession,
)

"""
I don't want to use serializer to save and update the data, 
but only to validate the data and serialize the response.

"""


class ExerciseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    muscle_targeted = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False, allow_blank=True)


class WorkoutSessionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=WorkoutSession.objects.all())
    date = serializers.DateField()
    notes = serializers.CharField(allow_blank=True, required=False)
    exercises = serializers.SerializerMethodField()

    def get_exercises(self, obj):
        return [
            {
                "name": exercise.exercise.name,
                "reps": exercise.reps,
                "weight": exercise.weight,
            }
            for exercise in obj.exercises.all()
        ]


class WorkoutSessionCreateSerializer(serializers.Serializer):
    notes = serializers.CharField(allow_blank=True, required=False)


class WorkoutSessionExerciseSerializer(serializers.Serializer):
    workout_session = serializers.PrimaryKeyRelatedField(
        queryset=WorkoutSession.objects.all()
    )
    exercise = serializers.PrimaryKeyRelatedField(queryset=Exercise.objects.all())
    notes = serializers.CharField(allow_blank=True, required=False)


class WorkoutSessionExerciseSetSerializer(serializers.Serializer):
    session_exercise = serializers.PrimaryKeyRelatedField(
        queryset=WorkoutSession.objects.all()
    )
    reps = serializers.IntegerField()
    weight = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate(self, attrs):
        if attrs["reps"] <= 0 or attrs["weight"] < 0:
            raise serializers.ValidationError(
                "Reps must be greater than 0 and weight cannot be negative."
            )
        return attrs
