from datetime import date
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status

from iron.models import Exercise
from iron.serializers import (
    ExerciseSerializer,
    WorkoutSessionCreateSerializer,
    WorkoutSessionSerializer,
)
from django.shortcuts import get_object_or_404

from iron.services import update_exercise


class ExerciseViewSet(ViewSet):
    def list(self, _):
        ser = ExerciseSerializer(Exercise.objects.all(), many=True)
        return Response(ser.data)

    def retrieve(self, request, pk):
        exercise = get_object_or_404(Exercise, pk=pk)
        exercises = ExerciseSerializer(exercise)
        return Response(exercises.data)

    def create(self, request):
        ser = ExerciseSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=400)
        Exercise.objects.create(**ser.data)
        return Response(status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        exercise = Exercise.objects.filter(pk=pk).first()
        if not exercise:
            return Response({"error": "Exercise not found"}, status=404)
        ser = ExerciseSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        update_exercise(exercise, ser.data)
        return Response(status=200)

    def destroy(self, request, pk):
        exercise = get_object_or_404(Exercise, pk=pk)
        exercise.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WorkoutSessionViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user
        workout_sessions = user.workout_sessions.prefetch_related("exercises").all()
        ser = WorkoutSessionSerializer(workout_sessions, many=True)
        return Response(ser.data)

    def retreive(self, request, pk):
        workout_session = request.user.workout_sessions.filter(pk=pk).first()
        if not workout_session:
            return Response(
                {"error": "Workout session not found"}, status=status.HTTP_404_NOT_FOUND
            )
        ser = WorkoutSessionSerializer(workout_session)
        return Response(ser.data)

    def create(self, request):
        ser = WorkoutSessionCreateSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        today = date.today()
        user = request.user
        workout_session = user.workout_sessions.create(
            date=today, notes=ser.data.get("notes", "")
        )
        data = WorkoutSessionSerializer(workout_session).data
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        workout_session = request.user.workout_sessions.filter(pk=pk).first()
        if not workout_session:
            return Response({"error": "Workout session not found"}, status=404)
        ser = WorkoutSessionSerializer(workout_session, data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=400)
        workout_session.notes = ser.data.get("notes", "")
        workout_session.save()
        return Response(ser.data)
