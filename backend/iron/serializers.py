from rest_framework import serializers
from .models import (
    Exercise,
    WorkoutSplit,
    WorkoutSplitDay,
    WorkoutSession,
)


class ExerciseSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    muscle_targeted = serializers.CharField(max_length=100)


class WorkoutSplitSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    length = serializers.IntegerField()


class WorkoutSplitDaySerializer(serializers.Serializer):
    split = serializers.PrimaryKeyRelatedField(queryset=WorkoutSplit.objects.all())
    name = serializers.CharField(max_length=100)


class WorkoutSessionSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=WorkoutSession.objects.all(), source="user"
    )
    date = serializers.DateField()
    split_day = serializers.PrimaryKeyRelatedField(
        queryset=WorkoutSplitDay.objects.all()
    )
    notes = serializers.CharField(allow_blank=True, required=False)


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
