from rest_framework import serializers
from .models import (
    Exercise,
    WorkoutSession,
)
from common.serializers import DynamicFieldsSerializer

"""
I don't want to use serializer to save and update the data, 
but only to validate the data and serialize the response.
"""


class ExerciseSerializer(DynamicFieldsSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    muscle_targeted = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False, allow_blank=True)


class ExerciseCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    muscle_targeted = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False, allow_blank=True)


class WorkoutSessionExerciseSetSerializer(DynamicFieldsSerializer):
    id = serializers.IntegerField(read_only=True)
    session_exercise = serializers.PrimaryKeyRelatedField(
        queryset=WorkoutSession.objects.all()
    )
    reps = serializers.IntegerField()
    weight = serializers.DecimalField(max_digits=10, decimal_places=2)


class WorkoutSessionExerciseSetCreateSerializer(serializers.Serializer):
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


class WorkoutSessionExerciseSerializer(DynamicFieldsSerializer):
    workout_session = serializers.PrimaryKeyRelatedField(
        queryset=WorkoutSession.objects.all()
    )
    exercise = ExerciseSerializer(read_only=True)
    notes = serializers.CharField(allow_blank=True, required=False)
    sets = WorkoutSessionExerciseSetSerializer(
        fields=["id", "reps", "weight"], many=True, read_only=True
    )


class WorkoutSessionExerciseCreateSerializer(serializers.Serializer):
    workout_session = serializers.PrimaryKeyRelatedField(
        queryset=WorkoutSession.objects.all()
    )
    exercise = serializers.PrimaryKeyRelatedField(queryset=Exercise.objects.all())
    notes = serializers.CharField(allow_blank=True, required=False)


class WorkoutSessionSerializer(DynamicFieldsSerializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=WorkoutSession.objects.all())
    date = serializers.DateField()
    notes = serializers.CharField(allow_blank=True, required=False)
    session_exercises = WorkoutSessionExerciseSerializer(
        fields=["exercise", "notes", "sets"], many=True, read_only=True
    )


class WorkoutSessionCreateSerializer(DynamicFieldsSerializer):
    date = serializers.DateField(required=False)
    notes = serializers.CharField(allow_blank=True, required=False)
